import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight text-white">Vanguard AI Eval Platform</h1>
      <p className="text-sm text-slate-300 max-w-2xl">
        Run automated evaluations for prompts and models, combining heuristic checks with LLM-based judging.
      </p>
      <Card>
        <CardHeader>
          <CardTitle>Evaluation Runs</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-300 mb-4">
            Inspect recent evaluation runs and drill into individual test results.
          </p>
          <Link
            href="/runs"
            className="inline-flex items-center rounded-md bg-emerald-500 px-4 py-2 text-sm font-medium text-emerald-950 shadow hover:bg-emerald-400"
          >
            View Evaluation Runs
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
