from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

import requests


def main() -> int:
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not api_url:
        print("ERROR: API_URL is not set (expected from VANGUARD_API_URL secret).", file=sys.stderr)
        return 1

    if not api_key:
        print("ERROR: API_KEY is not set (expected from VANGUARD_API_KEY secret).", file=sys.stderr)
        return 1

    if not openai_key:
        print("WARNING: OPENAI_API_KEY is not set; backend judge may fail if it requires it.", file=sys.stderr)

    run_endpoint = api_url.rstrip("/") + "/v1/evals/run"

    payload: Dict[str, Any] = {
        "prompt": "You are a helpful, concise assistant.",
        "target_model": "stub-ci-model",
        "pass_threshold": 0.75,
        "test_cases": [
            {
                "input": "Hello",
                "expected_output": "Input: Hello",
            },
            {
                "input": "What is 2+2?",
                "expected_output": "Input: What is 2+2?",
            },
            {
                "input": "Summarize: GitHub Actions",
                "expected_output": "Input: Summarize: GitHub Actions",
            },
        ],
    }

    print(f"Calling eval API at {run_endpoint}")

    try:
        resp = requests.post(
            run_endpoint,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                # X-Project-Id is optional; use a static one for CI context.
                "X-Project-Id": "ci-pipeline",
            },
            data=json.dumps(payload),
            timeout=60,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: request to eval API failed: {exc}", file=sys.stderr)
        return 1

    print(f"HTTP {resp.status_code}")
    try:
        body = resp.json()
    except Exception:  # noqa: BLE001
        print("ERROR: could not parse JSON response:", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        return 1

    print("Response JSON:")
    print(json.dumps(body, indent=2))

    if resp.status_code >= 400:
        print("ERROR: eval API returned error status.", file=sys.stderr)
        return 1

    overall_pass = body.get("overall_pass")
    print(f"overall_pass = {overall_pass}")

    if overall_pass is not True:
        print("CI gate FAILED: overall_pass is not true", file=sys.stderr)
        return 1

    print("CI gate PASSED: evaluation succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
