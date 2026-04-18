import fs from "fs";
import path from "path";
import matter from "gray-matter";

import { formatReportAge, getBangkokTodayDate, getReportAgeDays } from "@/lib/date";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const WIKI_DIR = path.join(PROJECT_ROOT, "wiki");
const REPORTS_DIR = path.join(WIKI_DIR, "reports");

interface MarkdownData {
  title?: string;
  tags?: string[];
  sources?: string[];
  created?: string | Date;
  updated?: string | Date;
}

interface ReportFile {
  date: string;
  type: string;
  content: string;
  filePath: string;
  title: string;
  tags: string[];
  sources: string[];
  created?: string;
  updated?: string;
}

export interface ReportDocument extends ReportFile {
  requestedDate: string;
  resolvedDate: string;
  isFallback: boolean;
  ageDays: number;
  ageLabel: string;
}

export function getWikiArticles(category: string): string[] {
  const dir = path.join(WIKI_DIR, category);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .map((f) => f.replace(".md", ""))
    .sort();
}

export function getReportDates(): { date: string; types: string[] }[] {
  if (!fs.existsSync(REPORTS_DIR)) return [];

  const files = fs.readdirSync(REPORTS_DIR).filter((f) => f.endsWith(".md"));
  const dateMap = new Map<string, string[]>();

  for (const file of files) {
    // Parse: 2026-04-11-morning-briefing.md → date=2026-04-11, type=morning-briefing
    const match = file.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.md$/);
    if (match) {
      const [, date, type] = match;
      if (!dateMap.has(date)) dateMap.set(date, []);
      dateMap.get(date)!.push(type);
    }
  }

  return Array.from(dateMap.entries())
    .map(([date, types]) => ({ date, types: types.sort() }))
    .sort((a, b) => b.date.localeCompare(a.date));
}

function formatReportType(type: string) {
  return type
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function normalizeStringArray(value: unknown) {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is string => typeof item === "string");
}

function normalizeDateValue(value: unknown) {
  if (typeof value === "string") return value;
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return undefined;
}

function parseReportFile(filePath: string): ReportFile | null {
  const fileName = path.basename(filePath);
  const match = fileName.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.md$/);
  if (!match) return null;

  const [, date, type] = match;
  const raw = fs.readFileSync(filePath, "utf-8");
  const parsed = matter(raw);
  const metadata = parsed.data as MarkdownData;
  const title = metadata.title || `${formatReportType(type)} — ${date}`;

  return {
    date,
    type,
    content: parsed.content.trim(),
    filePath,
    title,
    tags: normalizeStringArray(metadata.tags),
    sources: normalizeStringArray(metadata.sources),
    created: normalizeDateValue(metadata.created),
    updated: normalizeDateValue(metadata.updated),
  };
}

function getReportByFileName(fileName: string): ReportFile | null {
  const filePath = path.join(REPORTS_DIR, fileName);
  if (!fs.existsSync(filePath)) return null;
  return parseReportFile(filePath);
}

export function getLatestReportByType(type: string): ReportFile | null {
  if (!fs.existsSync(REPORTS_DIR)) return null;

  const matchingFiles = fs
    .readdirSync(REPORTS_DIR)
    .filter((file) => file.endsWith(`-${type}.md`))
    .sort()
    .reverse();

  for (const file of matchingFiles) {
    const report = getReportByFileName(file);
    if (report) return report;
  }

  return null;
}

export function getReportByDateAndType(date: string, type: string): ReportFile | null {
  return getReportByFileName(`${date}-${type}.md`);
}

export function resolveReport(date: string, type: string): ReportDocument | null {
  const today = getBangkokTodayDate();
  const requestedDate = date === "today" ? today : date;
  const directReport = getReportByDateAndType(requestedDate, type);
  const report = directReport ?? (date === "today" ? getLatestReportByType(type) : null);

  if (!report) {
    return null;
  }

  const resolvedDate = report.date;
  const ageDays = getReportAgeDays(resolvedDate, today);

  return {
    ...report,
    requestedDate,
    resolvedDate,
    isFallback: resolvedDate !== requestedDate,
    ageDays,
    ageLabel: formatReportAge(resolvedDate, today),
  };
}

export function readMarkdownFile(filePath: string): string | null {
  const fullPath = path.join(PROJECT_ROOT, filePath);
  if (!fs.existsSync(fullPath)) return null;
  return fs.readFileSync(fullPath, "utf-8");
}
