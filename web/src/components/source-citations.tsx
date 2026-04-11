"use client";

import Link from "next/link";

interface SourceCitationsProps {
  sources: string[];
}

export function SourceCitations({ sources }: SourceCitationsProps) {
  if (sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-border/50">
      <p className="text-xs text-muted-foreground mb-1.5">Sources</p>
      <div className="flex flex-wrap gap-1.5">
        {sources.map((source) => {
          // wiki/contributors/garrytan.md → /wiki/contributors/garrytan
          const href = "/" + source.replace(".md", "");
          const label = source.split("/").pop()?.replace(".md", "") || source;

          return (
            <Link
              key={source}
              href={href}
              className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-muted text-muted-foreground hover:bg-primary/10 hover:text-primary border border-border/50 transition-colors"
            >
              {label}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
