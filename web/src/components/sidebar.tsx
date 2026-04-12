"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSyncExternalStore } from "react";
import { Button } from "@/components/ui/button";

interface SidebarProps {
  contributors: string[];
  projects: string[];
  patterns: string[];
  connections: string[];
  reportDates: { date: string; types: string[] }[];
  open: boolean;
  onClose: () => void;
}

function getSectionSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

const SIDEBAR_SECTION_STORAGE_EVENT = "team-pulse-sidebar-storage";

function readSectionOpenState(storageKey: string, defaultOpen: boolean): boolean {
  if (typeof window === "undefined") {
    return defaultOpen;
  }

  const storedValue = window.localStorage.getItem(storageKey);
  if (storedValue === "true") return true;
  if (storedValue === "false") return false;
  return defaultOpen;
}

function subscribeToSectionState(
  storageKey: string,
  onStoreChange: () => void
): () => void {
  if (typeof window === "undefined") {
    return () => {};
  }

  const handleChange = (event: Event) => {
    if (event instanceof StorageEvent && event.key && event.key !== storageKey) {
      return;
    }
    onStoreChange();
  };

  window.addEventListener("storage", handleChange);
  window.addEventListener(SIDEBAR_SECTION_STORAGE_EVENT, handleChange);
  queueMicrotask(onStoreChange);

  return () => {
    window.removeEventListener("storage", handleChange);
    window.removeEventListener(SIDEBAR_SECTION_STORAGE_EVENT, handleChange);
  };
}

function writeSectionOpenState(storageKey: string, isOpen: boolean): void {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(storageKey, String(isOpen));
  window.dispatchEvent(new Event(SIDEBAR_SECTION_STORAGE_EVENT));
}

function SidebarSection({
  title,
  defaultOpen = false,
  children,
}: {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const sectionSlug = getSectionSlug(title);
  const panelId = `sidebar-section-${sectionSlug}`;
  const storageKey = `team-pulse-sidebar:${sectionSlug}`;
  const isOpen = useSyncExternalStore(
    (onStoreChange) => subscribeToSectionState(storageKey, onStoreChange),
    () => readSectionOpenState(storageKey, defaultOpen),
    () => defaultOpen
  );

  return (
    <div>
      <button
        type="button"
        onClick={() => writeSectionOpenState(storageKey, !isOpen)}
        aria-expanded={isOpen}
        aria-controls={panelId}
        title={`${isOpen ? "Collapse" : "Expand"} ${title}`}
        className="flex w-full cursor-pointer items-center justify-between px-3 py-2 text-xs font-medium uppercase tracking-wider text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30 focus-visible:ring-offset-2 focus-visible:ring-offset-sidebar"
      >
        {title}
        <svg
          className={`w-3 h-3 transition-transform ${isOpen ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <div id={panelId} hidden={!isOpen} className="pb-2">
        {children}
      </div>
    </div>
  );
}

function SidebarLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      className={`block px-3 py-1.5 mx-2 rounded-md text-sm truncate ${
        isActive
          ? "bg-primary/10 text-primary font-medium"
          : "text-muted-foreground hover:bg-muted hover:text-foreground"
      }`}
    >
      {children}
    </Link>
  );
}

function formatReportType(type: string): string {
  return type
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export function Sidebar({
  contributors,
  projects,
  patterns,
  connections,
  reportDates,
  open,
  onClose,
}: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 left-0 z-50 h-full w-[280px] border-r border-border bg-sidebar flex flex-col overflow-y-auto transition-transform lg:static lg:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* New Chat button */}
        <div className="p-3">
          <Link href="/">
            <Button variant="outline" className="w-full justify-start">
              + New Chat
            </Button>
          </Link>
        </div>

        {/* Quick Actions */}
        <SidebarSection title="Quick Actions" defaultOpen>
          <SidebarLink href="/">New Chat</SidebarLink>
          <SidebarLink href="/reports/today/morning-briefing">
            Morning Briefing
          </SidebarLink>
          <SidebarLink href="/reports/today/eod-summary">
            EOD Summary
          </SidebarLink>
          <SidebarLink href="/reports/today/team-dashboard">
            Team Dashboard
          </SidebarLink>
        </SidebarSection>

        {/* Reports Archive */}
        <SidebarSection title="Reports Archive" defaultOpen={false}>
          {reportDates.length === 0 && (
            <p className="px-3 text-xs text-muted-foreground">
              No reports yet
            </p>
          )}
          {reportDates.map(({ date, types }) => (
            <div key={date}>
              <p className="px-3 py-1 text-xs font-medium text-muted-foreground">
                {date}
              </p>
              {types.map((type) => (
                <SidebarLink key={type} href={`/reports/${date}/${type}`}>
                  {formatReportType(type)}
                </SidebarLink>
              ))}
            </div>
          ))}
        </SidebarSection>

        {/* Wiki Browser */}
        <SidebarSection title="Wiki Browser" defaultOpen={false}>
          {contributors.length > 0 && (
            <div className="mb-2">
              <p className="px-3 py-1 text-xs font-medium text-muted-foreground">
                Contributors
              </p>
              {contributors.map((name) => (
                <SidebarLink key={name} href={`/wiki/contributors/${name}`}>
                  {name}
                </SidebarLink>
              ))}
            </div>
          )}
          {projects.length > 0 && (
            <div className="mb-2">
              <p className="px-3 py-1 text-xs font-medium text-muted-foreground">
                Projects
              </p>
              {projects.map((name) => (
                <SidebarLink key={name} href={`/wiki/projects/${name}`}>
                  {name}
                </SidebarLink>
              ))}
            </div>
          )}
          {patterns.length > 0 && (
            <div className="mb-2">
              <p className="px-3 py-1 text-xs font-medium text-muted-foreground">
                Patterns
              </p>
              {patterns.map((name) => (
                <SidebarLink key={name} href={`/wiki/patterns/${name}`}>
                  {name}
                </SidebarLink>
              ))}
            </div>
          )}
          {connections.length > 0 && (
            <div className="mb-2">
              <p className="px-3 py-1 text-xs font-medium text-muted-foreground">
                Connections
              </p>
              {connections.map((name) => (
                <SidebarLink key={name} href={`/wiki/connections/${name}`}>
                  {name}
                </SidebarLink>
              ))}
            </div>
          )}
        </SidebarSection>
      </aside>
    </>
  );
}
