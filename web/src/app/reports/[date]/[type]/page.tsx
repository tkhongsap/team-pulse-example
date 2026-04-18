import Link from "next/link";
import { notFound } from "next/navigation";
import { getLatestReportByType, readMarkdownFile } from "@/lib/wiki";
import { MarkdownRenderer } from "@/components/markdown-renderer";

interface ReportPageProps {
  params: Promise<{ date: string; type: string }>;
}

export default async function ReportPage({ params }: ReportPageProps) {
  const { date, type } = await params;

  // Handle "today" shortcut
  const resolvedDate =
    date === "today"
      ? new Date().toISOString().split("T")[0]
      : date;

  const filePath = `wiki/reports/${resolvedDate}-${type}.md`;
  const requestedContent = readMarkdownFile(filePath);
  const fallbackReport =
    date === "today" && !requestedContent ? getLatestReportByType(type) : null;
  const content = requestedContent ?? fallbackReport?.content ?? null;

  if (!content && date !== "today") {
    notFound();
  }

  const title = type
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
  const displayedDate = fallbackReport?.date ?? resolvedDate;
  const generatorType =
    type === "morning-briefing"
      ? "morning"
      : type === "eod-summary"
        ? "eod"
        : type === "team-dashboard"
          ? "dashboard"
          : null;

  return (
    <div className="max-w-4xl mx-auto px-6 py-6">
      <div className="flex items-center gap-3 mb-6">
        <Link
          href="/"
          className="text-sm text-muted-foreground hover:text-foreground"
        >
          &larr; Back to Chat
        </Link>
        <span className="text-sm text-muted-foreground">|</span>
        <span className="text-sm font-medium">
          {title} &mdash; {displayedDate}
        </span>
      </div>

      {fallbackReport && (
        <div className="mb-6 rounded-lg border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
          No {title} report for today yet. Showing latest available from{" "}
          <span className="font-medium text-foreground">{fallbackReport.date}</span>.
        </div>
      )}

      {content ? (
        <MarkdownRenderer content={content} />
      ) : (
        <div className="rounded-lg border border-dashed border-border bg-muted/30 px-6 py-8">
          <h1 className="mb-2 text-xl font-semibold">{title} not available yet</h1>
          <p className="mb-3 text-sm text-muted-foreground">
            There is no {title.toLowerCase()} report available yet. Generate one with
            the existing report pipeline and refresh this page.
          </p>
          {generatorType && (
            <code className="block rounded bg-muted px-3 py-2 text-sm">
              python scripts/generate_report.py --type {generatorType} --date{" "}
              {resolvedDate}
            </code>
          )}
        </div>
      )}
    </div>
  );
}
