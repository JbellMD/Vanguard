import "./globals.css";
import type { ReactNode } from "react";
import Link from "next/link";

export const metadata = {
  title: "Vanguard AI Eval Dashboard",
  description: "Inspect AI evaluation runs and results.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="container-page">
        <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
          <div className="page-inner flex items-center justify-between py-4">
            <Link href="/" className="text-lg font-semibold tracking-tight">
              Vanguard Eval
            </Link>
            <nav className="flex gap-4 text-sm text-slate-300">
              <Link href="/runs" className="hover:text-white">
                Runs
              </Link>
            </nav>
          </div>
        </header>
        <main className="page-inner flex-1 w-full">{children}</main>
      </body>
    </html>
  );
}
