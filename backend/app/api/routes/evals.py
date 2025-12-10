from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...database import get_session
from ...models import TestRun, TestCase, EvalResult
from ..schemas import (
    EvalRunRequest,
    EvalRunResponse,
    EvalRunListResponse,
    EvalRunDetailResponse,
    EvalRunSummary,
    EvalResultItem,
)
from ...services.eval_runner import EvalRunner


router = APIRouter()


@router.post("/run", response_model=EvalRunResponse)
def run_eval(
    payload: EvalRunRequest,
    session: Session = Depends(get_session),
) -> EvalRunResponse:
    runner = EvalRunner()
    result = runner.run_eval(
        session,
        prompt=payload.prompt,
        target_model=payload.target_model,
        test_cases=[tc.model_dump() for tc in payload.test_cases],
        pass_threshold=payload.pass_threshold,
    )
    return EvalRunResponse(**result)


@router.get("/runs", response_model=EvalRunListResponse)
def list_runs(
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None,
    overall_pass: Optional[bool] = None,
    session: Session = Depends(get_session),
) -> EvalRunListResponse:
    statement = select(TestRun)

    if status is not None:
        statement = statement.where(TestRun.status == status)
    if overall_pass is not None:
        statement = statement.where(TestRun.overall_pass == overall_pass)

    statement = statement.order_by(TestRun.created_at.desc())
    all_runs: List[TestRun] = session.exec(statement).all()

    total = len(all_runs)
    window = all_runs[offset : offset + limit]

    items: List[EvalRunSummary] = []
    for run in window:
        items.append(
            EvalRunSummary(
                id=str(run.id),
                created_at=run.created_at.isoformat() if run.created_at else "",
                status=run.status,
                target_model=run.target_model,
                total_cases=run.total_cases,
                passed_cases=run.passed_cases,
                average_score=run.average_score,
                overall_pass=run.overall_pass,
            )
        )

    return EvalRunListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/runs/{run_id}", response_model=EvalRunDetailResponse)
def get_run_detail(
    run_id: str,
    session: Session = Depends(get_session),
) -> EvalRunDetailResponse:
    run = session.get(TestRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # Ensure relationships are loaded
    session.refresh(run)

    results: List[EvalResultItem] = []

    for case in run.cases:
        session.refresh(case)
        result: Optional[EvalResult] = case.eval_result
        if not result:
            continue

        results.append(
            EvalResultItem(
                test_case_id=str(case.id),
                input_text=case.input_text,
                expected_output=case.expected_output,
                model_output=result.model_output_text,
                heuristic_score=result.heuristic_score,
                judge_score=result.judge_score,
                combined_score=result.combined_score,
                passed=result.passed,
                judge_reasoning=result.judge_reasoning,
            )
        )

    return EvalRunDetailResponse(
        id=str(run.id),
        created_at=run.created_at.isoformat() if run.created_at else "",
        status=run.status,
        target_model=run.target_model,
        prompt=run.prompt,
        total_cases=run.total_cases,
        passed_cases=run.passed_cases,
        average_score=run.average_score,
        overall_pass=run.overall_pass,
        pass_threshold=run.pass_threshold,
        results=results,
    )
