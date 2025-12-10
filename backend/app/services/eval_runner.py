from __future__ import annotations

from typing import List, Dict, Any

from sqlmodel import Session

from ..models import TestRun, TestCase, EvalResult
from .judge_service import JudgeService


DEFAULT_PASS_THRESHOLD = 0.75


def call_target_model_stub(prompt: str, test_input: str, target_model: str) -> str:
    """Stub for the target model call.

    In production this would call your actual model endpoint (OpenAI, Anthropic,
    internal HTTP service, etc.). For the MVP we just echo the input in a simple
    templated way so the pipeline is fully runnable.
    """
    return f"[model={target_model}] Prompt: {prompt}\nInput: {test_input}"


class EvalRunner:
    def __init__(self, judge_service: JudgeService | None = None) -> None:
        self.judge_service = judge_service or JudgeService()

    def run_eval(
        self,
        session: Session,
        *,
        prompt: str,
        target_model: str,
        test_cases: List[Dict[str, Any]],
        pass_threshold: float = DEFAULT_PASS_THRESHOLD,
    ) -> Dict[str, Any]:
        run = TestRun(
            target_model=target_model,
            prompt=prompt,
            status="running",
            pass_threshold=pass_threshold,
        )
        session.add(run)
        session.commit()
        session.refresh(run)

        passed_cases = 0
        total_score = 0.0
        detailed_results: List[Dict[str, Any]] = []

        for case_payload in test_cases:
            input_text = str(case_payload.get("input"))
            expected_output = case_payload.get("expected_output")
            metadata = case_payload.get("metadata")

            case = TestCase(
                run_id=run.id,
                input_text=input_text,
                expected_output=expected_output,
                metadata=metadata,
            )
            session.add(case)
            session.commit()
            session.refresh(case)

            model_output = call_target_model_stub(prompt, input_text, target_model)

            heuristic_score = self._heuristic_score(model_output, expected_output)
            judge_score, reasoning = self.judge_service.score_output(
                system_prompt=prompt,
                test_input=input_text,
                model_output=model_output,
                expected_output=expected_output,
            )
            combined_score = 0.5 * heuristic_score + 0.5 * judge_score
            passed = combined_score >= pass_threshold

            result = EvalResult(
                test_case_id=case.id,
                model_output=model_output,
                heuristic_score=heuristic_score,
                judge_score=judge_score,
                combined_score=combined_score,
                passed=passed,
                judge_reasoning=reasoning,
            )
            session.add(result)
            session.commit()

            passed_cases += 1 if passed else 0
            total_score += combined_score

            detailed_results.append(
                {
                    "test_case_id": str(case.id),
                    "input": input_text,
                    "expected_output": expected_output,
                    "model_output": model_output,
                    "heuristic_score": heuristic_score,
                    "judge_score": judge_score,
                    "combined_score": combined_score,
                    "passed": passed,
                    "judge_reasoning": reasoning,
                }
            )

        run.total_cases = len(test_cases)
        run.passed_cases = passed_cases
        run.average_score = total_score / run.total_cases if run.total_cases else 0.0
        run.overall_pass = run.average_score >= pass_threshold
        run.status = "completed"

        session.add(run)
        session.commit()
        session.refresh(run)

        return {
            "run_id": str(run.id),
            "overall_pass": run.overall_pass,
            "average_score": run.average_score,
            "total_cases": run.total_cases,
            "passed_cases": run.passed_cases,
            "pass_threshold": run.pass_threshold,
            "results": detailed_results,
        }

    @staticmethod
    def _heuristic_score(model_output: str, expected_output: str | None) -> float:
        """Very simple heuristic for MVP.

        If expected_output is provided, returns 1.0 if it is a substring of the
        model output (case-insensitive), else 0.0. If no expected_output is
        provided, always returns 0.5.
        """
        if not expected_output:
            return 0.5
        return 1.0 if expected_output.lower() in model_output.lower() else 0.0
