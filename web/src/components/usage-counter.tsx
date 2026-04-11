"use client";

import { useEffect, useState } from "react";
import { getAnonymousId } from "@/lib/anonymous-id";

export function UsageCounter() {
  const [used, setUsed] = useState(0);
  const [limit, setLimit] = useState(100);

  useEffect(() => {
    async function fetchUsage() {
      try {
        const res = await fetch("/api/usage", {
          headers: { "X-Team-Pulse-Id": getAnonymousId() },
        });
        if (res.ok) {
          const data = await res.json();
          setUsed(data.used);
          setLimit(data.limit);
        }
      } catch {
        // Silently fail
      }
    }

    fetchUsage();
    const interval = setInterval(fetchUsage, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <span className="text-xs text-muted-foreground hidden sm:inline">
      {used}/{limit} queries
    </span>
  );
}
