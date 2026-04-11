import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { checkRateLimit, incrementUsage } from "@/lib/rate-limit";

const ASK_SERVER_URL = process.env.ASK_SERVER_URL || "http://localhost:3001";

function resolveUserId(session: Awaited<ReturnType<typeof getServerSession>>, request: Request): string {
  if (session?.user) {
    return (session.user as Record<string, unknown>).id as string || session.user.email || "anonymous";
  }
  const clientId = request.headers.get("X-Team-Pulse-Id");
  return clientId ? `anon:${clientId}` : "anon:shared";
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  const userId = resolveUserId(session, request);

  // Check rate limit
  const { allowed, remaining } = checkRateLimit(userId);
  if (!allowed) {
    return NextResponse.json(
      { error: "Daily query limit reached. Resets at midnight Bangkok time." },
      {
        status: 429,
        headers: { "X-RateLimit-Remaining": "0", "X-RateLimit-Limit": "100" },
      }
    );
  }

  const body = await request.json();
  const { question, sessionId } = body as {
    question?: string;
    sessionId?: string;
  };

  if (!question?.trim()) {
    return NextResponse.json({ error: "Missing question" }, { status: 400 });
  }

  // Increment usage before making the request
  incrementUsage(userId);

  try {
    const response = await fetch(`${ASK_SERVER_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, sessionId }),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Ask server error" },
        { status: response.status }
      );
    }

    // Forward SSE stream with rate limit headers
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
        "X-RateLimit-Remaining": String(remaining - 1),
        "X-RateLimit-Limit": "100",
      },
    });
  } catch {
    return NextResponse.json(
      { error: "Ask server not available. Start it with: python3 scripts/ask_server.py" },
      { status: 503 }
    );
  }
}
