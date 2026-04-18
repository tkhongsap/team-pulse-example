import fs from "fs";
import path from "path";

const PROJECT_ROOT = path.resolve(process.cwd(), "..");
const WIKI_DIR = path.join(PROJECT_ROOT, "wiki");
const REPORTS_DIR = path.join(WIKI_DIR, "reports");

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

export interface LatestReport {
  date: string;
  type: string;
  content: string;
  filePath: string;
}

export function getLatestReportByType(type: string): LatestReport | null {
  if (!fs.existsSync(REPORTS_DIR)) return null;

  const matchingFiles = fs
    .readdirSync(REPORTS_DIR)
    .filter((file) => file.endsWith(`-${type}.md`))
    .sort()
    .reverse();

  for (const file of matchingFiles) {
    const match = file.match(/^(\d{4}-\d{2}-\d{2})-(.+)\.md$/);
    if (!match) continue;

    const [, date, matchedType] = match;
    const filePath = path.join(REPORTS_DIR, file);

    return {
      date,
      type: matchedType,
      content: fs.readFileSync(filePath, "utf-8"),
      filePath,
    };
  }

  return null;
}

export function readMarkdownFile(filePath: string): string | null {
  const fullPath = path.join(PROJECT_ROOT, filePath);
  if (!fs.existsSync(fullPath)) return null;
  return fs.readFileSync(fullPath, "utf-8");
}
