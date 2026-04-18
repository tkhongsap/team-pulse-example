import { NextResponse } from "next/server";
import { resolveReport } from "@/lib/wiki";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ date: string; type: string }> }
) {
  const { date, type } = await params;
  const report = resolveReport(date, type);

  if (!report) {
    return NextResponse.json(
      { error: "Report not found" },
      { status: 404 }
    );
  }

  return NextResponse.json({
    content: report.content,
    date: report.requestedDate,
    resolvedDate: report.resolvedDate,
    type: report.type,
    title: report.title,
    tags: report.tags,
    sources: report.sources,
    created: report.created ?? null,
    updated: report.updated ?? null,
    isFallback: report.isFallback,
    ageDays: report.ageDays,
    ageLabel: report.ageLabel,
  });
}
