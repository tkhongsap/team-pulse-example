import { NextResponse } from "next/server";

const ASK_SERVER_URL = process.env.ASK_SERVER_URL || "http://localhost:3001";

export async function POST(request: Request) {
  const body = await request.json();
  const { question, sessionId } = body as {
    question?: string;
    sessionId?: string;
  };

  if (!question?.trim()) {
    return NextResponse.json({ error: "Missing question" }, { status: 400 });
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

    // Forward SSE stream
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    });
  } catch {
    return NextResponse.json(
      { error: "Ask server not available. Start it with: python3 scripts/ask_server.py" },
      { status: 503 }
    );
  }
}
