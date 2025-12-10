import Link from "next/link";
import { fetchRuns } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TBody, THead, TH, TR, TD } from "@/components/ui/table";

export const dynamic = "force-dynamic";

export default async function RunsPage() {
  const runs = await fetchRuns();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-2">
        <h1 className="text-2xl font-semibold tracking-tight text-white">Evaluation Runs</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent runs</CardTitle>
        </CardHeader>
        <CardContent>
          {runs.length === 0 ? (
            <p className="text-sm text-slate-400">No runs yet. Trigger an evaluation via the API.</p>
          ) : (
            <Table>
              <THead>
                <TR>
                  <TH>Created</TH>
                  <TH>Model</TH>
                  <TH>Cases</TH>
                  <TH>Passed</TH>
                  <TH>Average score</TH>
                  <TH>Status</TH>
                </TR>
              </THead>
              <TBody>
                {runs.map((run) => {
                  const created = new Date(run.created_at).toLocaleString();
                  return (
                    <TR
                      key={run.id}
                      className="hover:bg-slate-900/60 transition-colors cursor-pointer"
                    >
                      <TD className="whitespace-nowrap">
                        <Link href={`/runs/${run.id}`} className="text-emerald-300 hover:underline">
                          {created}
                        </Link>
                      </TD>
                      <TD className="whitespace-nowrap text-slate-200">{run.target_model}</TD>
                      <TD>{run.total_cases}</TD>
                      <TD>
                        {run.passed_cases} / {run.total_cases}
                      </TD>
                      <TD>{run.average_score.toFixed(2)}</TD>
                      <TD>
                        <Badge variant={run.overall_pass ? "success" : "danger"}>
                          {run.overall_pass ? "PASS" : "FAIL"}
                        </Badge>
                      </TD>
                    </TR>
                  );
                })}
              </TBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
