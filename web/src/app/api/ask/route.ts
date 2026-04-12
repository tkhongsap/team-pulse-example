import { NextResponse } from "next/server";
import { getServerSession, type Session } from "next-auth";
import { authOptions } from "@/lib/auth";
import { checkRateLimit, incrementUsage } from "@/lib/rate-limit";
import { getFastAskAnswer } from "@/lib/ask-fast-path";

const ASK_SERVER_URL = process.env.ASK_SERVER_URL || "http://localhost:3001";

function resolveUserId(session: Session | null, request: Request): string {
  const user = session?.user as (Session["user"] & { id?: string }) | undefined;

  if (user) {
    return user.id || user.email || "anonymous";
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

  const fastAnswer = getFastAskAnswer(question);

  // Increment usage before making the request
  incrementUsage(userId);

  if (fastAnswer) {
    return NextResponse.json(
      {
        text: fastAnswer.text,
        sources: fastAnswer.sources,
        sessionId: sessionId || null,
        strategy: fastAnswer.strategy,
      },
      {
        headers: {
          "X-RateLimit-Remaining": String(remaining - 1),
          "X-RateLimit-Limit": "100",
        },
      }
    );
  }

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
