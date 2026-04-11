"use client";

import { useState } from "react";
import { Header } from "./header";
import { Sidebar } from "./sidebar";

interface AppShellProps {
  contributors: string[];
  projects: string[];
  patterns: string[];
  connections: string[];
  reportDates: { date: string; types: string[] }[];
  children: React.ReactNode;
}

export function AppShell({
  contributors,
  projects,
  patterns,
  connections,
  reportDates,
  children,
}: AppShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar
        contributors={contributors}
        projects={projects}
        patterns={patterns}
        connections={connections}
        reportDates={reportDates}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <div className="flex flex-col flex-1 min-w-0">
        <Header onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
