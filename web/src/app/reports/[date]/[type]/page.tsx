import Link from "next/link";
import { notFound } from "next/navigation";

import { formatIsoDate, getBangkokTodayDate } from "@/lib/date";
import { resolveReport } from "@/lib/wiki";
import { MarkdownRenderer } from "@/components/markdown-renderer";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface ReportPageProps {
  params: Promise<{ date: string; type: string }>;
}

function formatReportType(type: string) {
  return type
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function getGeneratorType(type: string) {
  if (type === "morning-briefing") return "morning";
  if (type === "eod-summary") return "eod";
  if (type === "team-dashboard") return "dashboard";
  return null;
}

function getFreshnessLabel(ageDays: number, isFallback: boolean) {
  if (!isFallback && ageDays === 0) {
    return "Fresh today";
  }

  if (ageDays <= 1) {
    return "Recent";
  }

  return "Stale";
}

function getFreshnessClasses(ageDays: number, isFallback: boolean) {
  if (!isFallback && ageDays === 0) {
    return "border-emerald-300/70 bg-emerald-50 text-emerald-800 dark:border-emerald-700/60 dark:bg-emerald-950/20 dark:text-emerald-200";
  }

  if (ageDays <= 1) {
    return "border-sky-300/70 bg-sky-50 text-sky-800 dark:border-sky-700/60 dark:bg-sky-950/20 dark:text-sky-200";
  }

  return "border-amber-300/70 bg-amber-50 text-amber-900 dark:border-amber-700/60 dark:bg-amber-950/20 dark:text-amber-200";
}

export default async function ReportPage({ params }: ReportPageProps) {
  const { date, type } = await params;
  const report = resolveReport(date, type);
  const reportTypeLabel = formatReportType(type);
  const generatorType = getGeneratorType(type);

  if (!report && date !== "today") {
    notFound();
  }

  if (!report) {
    const requestedDate = formatIsoDate(getBangkokTodayDate());

    return (
      <div className="max-w-5xl mx-auto px-6 py-6">
        <div className="flex items-center gap-3 mb-6">
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-foreground"
          >
            &larr; Back to Chat
          </Link>
          <span className="text-sm text-muted-foreground">|</span>
          <span className="text-sm font-medium">{reportTypeLabel}</span>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{reportTypeLabel} not available yet</CardTitle>
            <CardDescription>
              No report is available for {requestedDate}. Generate one with the
              existing report pipeline and refresh this page.
            </CardDescription>
          </CardHeader>
          {generatorType && (
            <CardContent>
              <code className="block rounded bg-muted px-3 py-2 text-sm">
                python scripts/generate_report.py --type {generatorType} --date{" "}
                {getBangkokTodayDate()}
              </code>
            </CardContent>
          )}
        </Card>
      </div>
    );
  }

  const requestedDateLabel = formatIsoDate(report.requestedDate);
  const resolvedDateLabel = formatIsoDate(report.resolvedDate);
  const freshnessLabel = getFreshnessLabel(report.ageDays, report.isFallback);
  const freshnessClasses = getFreshnessClasses(report.ageDays, report.isFallback);

  return (
    <div className="max-w-5xl mx-auto px-6 py-6">
      <div className="flex flex-wrap items-center gap-3 mb-6">
        <Link
          href="/"
          className="text-sm text-muted-foreground hover:text-foreground"
        >
          &larr; Back to Chat
        </Link>
        <span className="text-sm text-muted-foreground">|</span>
        <span className="text-sm font-medium">{report.title}</span>
      </div>

      <div className="grid gap-4 mb-6 lg:grid-cols-[1.4fr_1fr]">
        <Card className={`ring-1 ${freshnessClasses}`}>
          <CardHeader>
            <CardTitle>
              {report.isFallback
                ? "Today’s report is not available yet"
                : "Freshness and availability"}
            </CardTitle>
            <CardDescription className="text-current/80">
              {report.isFallback
                ? `Requested ${requestedDateLabel}. Showing the latest available ${reportTypeLabel.toLowerCase()} from ${resolvedDateLabel}.`
                : `Viewing the report generated for ${resolvedDateLabel}.`}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">{reportTypeLabel}</Badge>
              <Badge variant="outline" className="border-current/25 text-current">
                {freshnessLabel}
              </Badge>
              <Badge variant="outline" className="border-current/25 text-current">
                {report.ageLabel}
              </Badge>
            </div>

            <dl className="grid gap-2 text-sm sm:grid-cols-2">
              <div>
                <dt className="text-current/70">Requested date</dt>
                <dd className="font-medium">{requestedDateLabel}</dd>
              </div>
              <div>
                <dt className="text-current/70">Resolved date</dt>
                <dd className="font-medium">{resolvedDateLabel}</dd>
              </div>
              <div>
                <dt className="text-current/70">Report age</dt>
                <dd className="font-medium">{report.ageLabel}</dd>
              </div>
              <div>
                <dt className="text-current/70">Status</dt>
                <dd className="font-medium">
                  {report.isFallback ? "Latest available fallback" : "Current report"}
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Report metadata</CardTitle>
            <CardDescription>
              Parsed from frontmatter instead of rendered in the report body.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {(report.tags.length > 0 ? report.tags : ["report"]).map((tag) => (
                <Badge key={tag} variant="outline">
                  {tag}
                </Badge>
              ))}
            </div>

            <dl className="grid gap-2 text-sm">
              {report.updated && (
                <div className="flex items-center justify-between gap-4">
                  <dt className="text-muted-foreground">Updated</dt>
                  <dd className="font-medium">{report.updated}</dd>
                </div>
              )}
              {report.created && (
                <div className="flex items-center justify-between gap-4">
                  <dt className="text-muted-foreground">Created</dt>
                  <dd className="font-medium">{report.created}</dd>
                </div>
              )}
              <div className="flex items-center justify-between gap-4">
                <dt className="text-muted-foreground">Sources</dt>
                <dd className="font-medium">{report.sources.length}</dd>
              </div>
            </dl>

            {report.sources.length > 0 && (
              <div>
                <p className="mb-2 text-sm font-medium">Source files</p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  {report.sources.map((source) => (
                    <li key={source} className="rounded-md bg-muted px-3 py-2 font-mono text-xs">
                      {source}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <MarkdownRenderer content={report.content} />
    </div>
  );
}
