import type { ReactNode } from "react";

export function Table({ children }: { children: ReactNode }) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="min-w-full divide-y divide-slate-800 bg-slate-950/40 text-sm">
        {children}
      </table>
    </div>
  );
}

export function THead({ children }: { children: ReactNode }) {
  return <thead className="bg-slate-900/70 text-xs uppercase tracking-wide text-slate-400">{children}</thead>;
}

export function TBody({ children }: { children: ReactNode }) {
  return <tbody className="divide-y divide-slate-800">{children}</tbody>;
}

export function TR({ children, className }: { children: ReactNode; className?: string }) {
  return <tr className={className}>{children}</tr>;
}

export function TH({ children }: { children: ReactNode }) {
  return <th className="px-4 py-3 text-left font-medium">{children}</th>;
}

export function TD({ children }: { children: ReactNode }) {
  return <td className="px-4 py-3 align-top text-slate-200">{children}</td>;
}
