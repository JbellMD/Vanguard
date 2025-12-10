import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={`rounded-xl border border-slate-800 bg-slate-900/60 shadow-sm ${className ?? ""}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children }: { children: ReactNode }) {
  return <div className="border-b border-slate-800 px-4 py-3 flex items-center justify-between gap-2">{children}</div>;
}

export function CardTitle({ children }: { children: ReactNode }) {
  return <h2 className="text-sm font-semibold text-slate-100">{children}</h2>;
}

export function CardContent({ children }: { children: ReactNode }) {
  return <div className="px-4 py-4">{children}</div>;
}
