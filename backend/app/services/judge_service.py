from __future__ import annotations

import os
from typing import Tuple

from openai import OpenAI


GRADING_PROMPT = """You are an expert evaluator for an AI-powered product.
You are given:
- The original system prompt or instructions.
- A test input.
- The model's output.
- (Optionally) an expected or reference output.

Your job is to:
1. Decide how well the model output follows the instructions and satisfies the user intent.
2. Consider both correctness and helpfulness.
3. Return:
   - A numeric score between 0.0 and 1.0 (1.0 is perfect).
   - A short explanation of your reasoning.

Be strict but fair. Minor issues should reduce the score slightly; major failures should produce a low score.
"""


class JudgeService:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is required for JudgeService")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def score_output(
        self,
        system_prompt: str,
        test_input: str,
        model_output: str,
        expected_output: str | None = None,
    ) -> Tuple[float, str]:
        """Call the LLM judge and return (score, reasoning).

        Score is expected to be between 0.0 and 1.0; we clamp to this range defensively.
        """
        user_content = [
            {"type": "text", "text": f"System prompt / instructions:\n{system_prompt}"},
            {"type": "text", "text": f"Test input:\n{test_input}"},
            {"type": "text", "text": f"Model output:\n{model_output}"},
        ]
        if expected_output is not None:
            user_content.append({"type": "text", "text": f"Expected / reference output:\n{expected_output}"})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": GRADING_PROMPT},
                {
                    "role": "user",
                    "content": user_content,
                },
                {
                    "role": "system",
                    "content": (
                        "Respond strictly in JSON with keys 'score' (float 0-1) and 'reason' (string). "
                        "Example: {\"score\": 0.82, \"reason\": \"...\"}"
                    ),
                },
            ],
            temperature=0.0,
        )

        content = response.choices[0].message.content or "{}"

        # Very small and safe JSON parsing without external deps
        import json

        try:
            data = json.loads(content)
            raw_score = float(data.get("score", 0.0))
            reason = str(data.get("reason", "No reasoning provided"))
        except Exception:
            raw_score = 0.0
            reason = f"Failed to parse judge response: {content!r}"

        score = max(0.0, min(1.0, raw_score))
        return score, reason
