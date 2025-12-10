from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Relationship


class EvalResult(SQLModel, table=True):
    __tablename__ = "eval_results"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    test_case_id: uuid.UUID = Field(foreign_key="test_cases.id", index=True)

    model_output_text: str
    heuristic_score: float
    judge_score: float
    combined_score: float
    passed: bool = Field(default=False, index=True)
    judge_reasoning: str

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class TestCase(SQLModel, table=True):
    __tablename__ = "test_cases"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    run_id: uuid.UUID = Field(foreign_key="test_runs.id", index=True)

    input_text: str
    expected_output: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    eval_result: Optional[EvalResult] = Relationship(back_populates="test_case")


class TestRun(SQLModel, table=True):
    __tablename__ = "test_runs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    status: str = Field(default="pending", index=True)

    target_model: str
    prompt: str

    total_cases: int = 0
    passed_cases: int = 0
    average_score: float = 0.0
    overall_pass: bool = Field(default=False, index=True)
    pass_threshold: float = 0.75

    cases: List[TestCase] = Relationship(back_populates="run")


TestCase.run = Relationship(back_populates="cases", sa_relationship_kwargs={"lazy": "selectin"})
EvalResult.test_case = Relationship(back_populates="eval_result")
