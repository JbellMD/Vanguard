from __future__ import annotations

from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session

from ...database import get_session
from ...services.eval_runner import EvalRunner, DEFAULT_PASS_THRESHOLD


router = APIRouter()


class EvalTestCase(BaseModel):
    input: str = Field(..., description="Input prompt or message for the model")
    expected_output: str | None = Field(
        default=None,
        description="Optional expected output used by simple heuristics.",
    )
    metadata: Dict[str, Any] | None = Field(
        default=None,
        description="Optional metadata for this test case (e.g., tags, scenario).",
    )


class EvalRunRequest(BaseModel):
    prompt: str = Field(..., description="System prompt / instructions for the model.")
    target_model: str = Field(..., description="Identifier of the target model under test.")
    pass_threshold: float = Field(
        default=DEFAULT_PASS_THRESHOLD,
        ge=0.0,
        le=1.0,
        description="Minimum combined score required to mark a test as passed.",
    )
    test_cases: List[EvalTestCase]


class EvalRunResponse(BaseModel):
    run_id: str
    overall_pass: bool
    average_score: float
    total_cases: int
    passed_cases: int
    pass_threshold: float
    results: List[Dict[str, Any]]


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
