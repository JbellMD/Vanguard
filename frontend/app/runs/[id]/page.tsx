import { notFound } from "next/navigation";
import { fetchRun } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TBody, THead, TH, TR, TD } from "@/components/ui/table";

export const dynamic = "force-dynamic";

interface RunDetailPageProps {
  params: { id: string };
}

export default async function RunDetailPage({ params }: RunDetailPageProps) {
  const { id } = params;

  try {
    const run = await fetchRun(id);

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-2">
          <h1 className="text-2xl font-semibold tracking-tight text-white">Run details</h1>
          <Badge variant={run.overall_pass ? "success" : "danger"}>
            {run.overall_pass ? "OVERALL PASS" : "OVERALL FAIL"}
          </Badge>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-1 gap-4 text-sm md:grid-cols-3">
              <div>
                <dt className="text-slate-400">Run ID</dt>
                <dd className="font-mono text-xs text-slate-200 break-all">{run.id}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Model</dt>
                <dd className="text-slate-200">{run.target_model}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Created</dt>
                <dd className="text-slate-200">{new Date(run.created_at).toLocaleString()}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Cases</dt>
                <dd className="text-slate-200">
                  {run.passed_cases} / {run.total_cases} passed
                </dd>
              </div>
              <div>
                <dt className="text-slate-400">Average score</dt>
                <dd className="text-slate-200">{run.average_score.toFixed(2)}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Pass threshold</dt>
                <dd className="text-slate-200">{run.pass_threshold.toFixed(2)}</dd>
              </div>
            </dl>
            <div className="mt-4">
              <h2 className="text-sm font-semibold text-slate-100 mb-1">Prompt</h2>
              <pre className="whitespace-pre-wrap rounded-md bg-slate-950/60 p-3 text-xs text-slate-200 border border-slate-800">
                {run.prompt}
              </pre>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Test results</CardTitle>
          </CardHeader>
          <CardContent>
            {run.results.length === 0 ? (
              <p className="text-sm text-slate-400">No results recorded for this run.</p>
            ) : (
              <Table>
                <THead>
                  <TR>
                    <TH>Input</TH>
                    <TH>Expected</TH>
                    <TH>Model output</TH>
                    <TH>Score</TH>
                    <TH>Result</TH>
                    <TH>Judge reasoning</TH>
                  </TR>
                </THead>
                <TBody>
                  {run.results.map((r) => (
                    <TR key={r.test_case_id} className="align-top">
                      <TD>
                        <div className="max-w-xs text-xs text-slate-100 whitespace-pre-wrap">
                          {r.input_text}
                        </div>
                      </TD>
                      <TD>
                        <div className="max-w-xs text-xs text-slate-300 whitespace-pre-wrap">
                          {r.expected_output ?? "—"}
                        </div>
                      </TD>
                      <TD>
                        <div className="max-w-xs text-xs text-slate-200 whitespace-pre-wrap">
                          {r.model_output}
                        </div>
                      </TD>
                      <TD className="text-xs">
                        {r.combined_score.toFixed(2)}
                      </TD>
                      <TD>
                        <Badge variant={r.passed ? "success" : "danger"}>
                          {r.passed ? "PASS" : "FAIL"}
                        </Badge>
                      </TD>
                      <TD>
                        <div className="max-w-xs text-xs text-slate-300 whitespace-pre-wrap line-clamp-4">
                          {r.judge_reasoning}
                        </div>
                      </TD>
                    </TR>
                  ))}
                </TBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>
    );
  } catch (e) {
    notFound();
  }
}
