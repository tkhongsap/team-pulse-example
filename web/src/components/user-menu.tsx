"use client";

import { useSession, signOut } from "next-auth/react";
import { useState } from "react";

export function UserMenu() {
  const { data: session } = useSession();
  const [open, setOpen] = useState(false);

  if (!session?.user) {
    return null;
  }

  const name = session.user.name || "User";
  const image = session.user.image;

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 p-1.5 rounded-md hover:bg-muted transition-colors"
      >
        {image ? (
          <img
            src={image}
            alt={name}
            className="w-6 h-6 rounded-full"
          />
        ) : (
          <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center text-xs font-medium">
            {name.charAt(0)}
          </div>
        )}
        <span className="text-sm hidden sm:inline">{name}</span>
        <svg
          className="w-3 h-3"
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

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute right-0 mt-1 w-48 rounded-md border border-border bg-popover shadow-lg z-50">
            <div className="px-3 py-2 border-b border-border">
              <p className="text-sm font-medium">{name}</p>
              {session.user.email && (
                <p className="text-xs text-muted-foreground">
                  {session.user.email}
                </p>
              )}
            </div>
            <button
              onClick={() => signOut()}
              className="w-full text-left px-3 py-2 text-sm hover:bg-muted transition-colors"
            >
              Sign out
            </button>
          </div>
        </>
      )}
    </div>
  );
}
