import type { ReactNode } from "react";
import clsx from "clsx";

interface BadgeProps {
  children: ReactNode;
  variant?: "success" | "danger" | "default";
}

export function Badge({ children, variant = "default" }: BadgeProps) {
  const base = "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium";
  const styles = {
    success: "bg-emerald-500/10 text-emerald-300 border border-emerald-500/40",
    danger: "bg-rose-500/10 text-rose-300 border border-rose-500/40",
    default: "bg-slate-700/60 text-slate-200 border border-slate-600/60",
  }[variant];

  return <span className={clsx(base, styles)}>{children}</span>;
}
