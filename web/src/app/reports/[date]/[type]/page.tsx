import Link from "next/link";
import { notFound } from "next/navigation";
import { readMarkdownFile } from "@/lib/wiki";
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
  const content = readMarkdownFile(filePath);

  if (!content) {
    notFound();
  }

  const title = type
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");

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
          {title} &mdash; {resolvedDate}
        </span>
      </div>
      <MarkdownRenderer content={content} />
    </div>
  );
}
