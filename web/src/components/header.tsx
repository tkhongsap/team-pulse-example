"use client";

import { ThemeToggle } from "./theme-toggle";
import { UsageCounter } from "./usage-counter";
import { formatBangkokCalendarDate } from "@/lib/date";

interface HeaderProps {
  onToggleSidebar: () => void;
}

export function Header({ onToggleSidebar }: HeaderProps) {
  const today = formatBangkokCalendarDate();

  return (
    <header className="h-14 border-b border-border bg-background flex items-center px-4 shrink-0">
      <button
        onClick={onToggleSidebar}
        className="lg:hidden mr-3 p-1.5 rounded-md hover:bg-muted"
        aria-label="Toggle sidebar"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      <div className="flex items-center gap-2">
        <span className="text-lg font-semibold">Team Pulse</span>
      </div>

      <div className="flex-1 text-center text-sm text-muted-foreground">
        {today}
      </div>

      <div className="flex items-center gap-3">
        <UsageCounter />
        <ThemeToggle />
      </div>
    </header>
  );
}
