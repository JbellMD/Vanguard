from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..services.eval_runner import DEFAULT_PASS_THRESHOLD


# Request / response schemas for eval runs


class EvalTestCase(BaseModel):
    input: str = Field(..., description="Input prompt or message for the model")
    expected_output: Optional[str] = Field(
        default=None,
        description="Optional expected output used by simple heuristics.",
    )
    metadata: Optional[Dict[str, Any]] = Field(
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


class EvalRunResultItem(BaseModel):
    test_case_id: str
    input: str
    expected_output: Optional[str]
    model_output: str
    heuristic_score: float
    judge_score: float
    combined_score: float
    passed: bool
    judge_reasoning: str


class EvalRunResponse(BaseModel):
    run_id: str
    overall_pass: bool
    average_score: float
    total_cases: int
    passed_cases: int
    pass_threshold: float
    results: List[EvalRunResultItem]


# Listing / summary schemas


class EvalRunSummary(BaseModel):
    id: str
    created_at: str
    status: str
    target_model: str
    total_cases: int
    passed_cases: int
    average_score: float
    overall_pass: bool


class EvalRunListResponse(BaseModel):
    items: List[EvalRunSummary]
    total: int
    limit: int
    offset: int


# Detailed run view


class EvalResultItem(BaseModel):
    test_case_id: str
    input_text: str
    expected_output: Optional[str]
    model_output: str
    heuristic_score: float
    judge_score: float
    combined_score: float
    passed: bool
    judge_reasoning: str


class EvalRunDetailResponse(BaseModel):
    id: str
    created_at: str
    status: str
    target_model: str
    prompt: str
    total_cases: int
    passed_cases: int
    average_score: float
    overall_pass: bool
    pass_threshold: float
    results: List[EvalResultItem]


class ErrorResponse(BaseModel):
    detail: str
