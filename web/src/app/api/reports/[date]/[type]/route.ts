import { NextResponse } from "next/server";
import { readMarkdownFile } from "@/lib/wiki";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ date: string; type: string }> }
) {
  const { date, type } = await params;
  const filePath = `wiki/reports/${date}-${type}.md`;
  const content = readMarkdownFile(filePath);

  if (!content) {
    return NextResponse.json(
      { error: "Report not found" },
      { status: 404 }
    );
  }

  return NextResponse.json({ content, date, type });
}
