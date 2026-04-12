import fs from "fs";
import path from "path";
import matter from "gray-matter";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const OUTPUTS_DIR = path.join(PROJECT_ROOT, "outputs");
const REPORTS_DIR = path.join(PROJECT_ROOT, "wiki", "reports");

const MORNING_BRIEFING_QUESTION =
  "Give me today's morning briefing — top priorities and action items";
const WEEKLY_SUMMARY_QUESTION =
  "Give me a weekly team health summary for management";

export interface FastAskAnswer {
  text: string;
  sources: string[];
  strategy: "cache" | "static";
}

export function normalizeQuestion(question: string): string {
  return question
    .normalize("NFKC")
    .replace(/[—–]/g, "-")
    .replace(/[’]/g, "'")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function listMarkdownFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((file) => file.endsWith(".md"))
    .sort((a, b) => b.localeCompare(a));
}

function parseMarkdownFile(fullPath: string): { content: string; data: Record<string, unknown> } | null {
  if (!fs.existsSync(fullPath)) return null;
  const raw = fs.readFileSync(fullPath, "utf-8");
  const parsed = matter(raw);
  return {
    content: parsed.content.trim(),
    data: parsed.data as Record<string, unknown>,
  };
}

function normalizeSources(value: unknown): string[] {
  const sources = Array.isArray(value)
    ? value.filter((source): source is string => typeof source === "string")
    : [];

  return sources;
}

function getLatestMorningBriefing(): FastAskAnswer | null {
  const reportFile = listMarkdownFiles(REPORTS_DIR).find((file) =>
    file.endsWith("-morning-briefing.md")
  );

  if (!reportFile) return null;

  const parsed = parseMarkdownFile(path.join(REPORTS_DIR, reportFile));
  if (!parsed) return null;

  return {
    text: parsed.content,
    sources: [`wiki/reports/${reportFile}`],
    strategy: "static",
  };
}

function getLatestWeeklySummary(): FastAskAnswer | null {
  const outputFile = listMarkdownFiles(OUTPUTS_DIR).find((file) =>
    file.endsWith("-weekly-team-health-summary.md")
  );

  if (!outputFile) return null;

  const parsed = parseMarkdownFile(path.join(OUTPUTS_DIR, outputFile));
  if (!parsed) return null;

  return {
    text: parsed.content,
    sources: normalizeSources(parsed.data.consulted),
    strategy: "static",
  };
}

function getStaticPromptAnswer(normalizedQuestion: string): FastAskAnswer | null {
  if (normalizedQuestion === normalizeQuestion(MORNING_BRIEFING_QUESTION)) {
    return getLatestMorningBriefing();
  }

  if (normalizedQuestion === normalizeQuestion(WEEKLY_SUMMARY_QUESTION)) {
    return getLatestWeeklySummary();
  }

  return null;
}

function getCachedOutputAnswer(normalizedQuestion: string): FastAskAnswer | null {
  for (const file of listMarkdownFiles(OUTPUTS_DIR)) {
    const parsed = parseMarkdownFile(path.join(OUTPUTS_DIR, file));
    if (!parsed) continue;

    const cachedQuestion =
      typeof parsed.data.question === "string" ? parsed.data.question : "";
    if (normalizeQuestion(cachedQuestion) !== normalizedQuestion) {
      continue;
    }

    return {
      text: parsed.content,
      sources: normalizeSources(parsed.data.consulted),
      strategy: "cache",
    };
  }

  return null;
}

export function getFastAskAnswer(question: string): FastAskAnswer | null {
  const normalizedQuestion = normalizeQuestion(question);
  return (
    getCachedOutputAnswer(normalizedQuestion) ??
    getStaticPromptAnswer(normalizedQuestion)
  );
}
