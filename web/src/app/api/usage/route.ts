import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { getUsage } from "@/lib/rate-limit";

export async function GET(request: Request) {
  const session = await getServerSession(authOptions);

  let userId: string;
  if (session?.user) {
    userId = (session.user as Record<string, unknown>).id as string || session.user.email || "anonymous";
  } else {
    const clientId = request.headers.get("X-Team-Pulse-Id");
    userId = clientId ? `anon:${clientId}` : "anon:shared";
  }

  const { used, limit } = getUsage(userId);
  return NextResponse.json({ used, limit });
}
