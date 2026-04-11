"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";

export function UsageCounter() {
  const { data: session } = useSession();
  const [used, setUsed] = useState(0);
  const [limit, setLimit] = useState(100);

  useEffect(() => {
    if (!session) return;

    async function fetchUsage() {
      try {
        const res = await fetch("/api/usage");
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
    // Refresh every 30 seconds
    const interval = setInterval(fetchUsage, 30000);
    return () => clearInterval(interval);
  }, [session]);

  if (!session) return null;

  return (
    <span className="text-xs text-muted-foreground hidden sm:inline">
      {used}/{limit} queries
    </span>
  );
}
