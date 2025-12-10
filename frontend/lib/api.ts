const BASE_URL = "http://localhost:8000";

export interface TestRunSummary {
  id: string;
  created_at: string;
  status: string;
  target_model: string;
  total_cases: number;
  passed_cases: number;
  average_score: number;
  overall_pass: boolean;
}

export interface EvalResultItem {
  test_case_id: string;
  input_text: string;
  expected_output?: string | null;
  model_output: string;
  heuristic_score: number;
  judge_score: number;
  combined_score: number;
  passed: boolean;
  judge_reasoning: string;
}

export interface EvalRunDetail {
  id: string;
  created_at: string;
  status: string;
  target_model: string;
  prompt: string;
  total_cases: number;
  passed_cases: number;
  average_score: number;
  overall_pass: boolean;
  pass_threshold: number;
  results: EvalResultItem[];
}

export async function fetchRuns(): Promise<TestRunSummary[]> {
  const res = await fetch(`${BASE_URL}/v1/evals/runs`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch runs: ${res.status}`);
  }
  const data = await res.json();
  return data.runs ?? [];
}

export async function fetchRun(runId: string): Promise<EvalRunDetail> {
  const res = await fetch(`${BASE_URL}/v1/evals/runs/${runId}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch run ${runId}: ${res.status}`);
  }
  return res.json();
}
