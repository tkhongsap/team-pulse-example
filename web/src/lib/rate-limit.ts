// In-memory rate limiter per user per day
// Resets at midnight Bangkok time (UTC+7)

const DAILY_LIMIT = 100;
const BANGKOK_OFFSET_MS = 7 * 60 * 60 * 1000;

interface UserUsage {
  count: number;
  resetDate: string; // YYYY-MM-DD in Bangkok time
}

const usage = new Map<string, UserUsage>();

function getBangkokDate(): string {
  const now = new Date(Date.now() + BANGKOK_OFFSET_MS);
  return now.toISOString().split("T")[0];
}

export function checkRateLimit(userId: string): {
  allowed: boolean;
  remaining: number;
  limit: number;
} {
  const today = getBangkokDate();
  const userUsage = usage.get(userId);

  // Reset if new day
  if (!userUsage || userUsage.resetDate !== today) {
    usage.set(userId, { count: 0, resetDate: today });
  }

  const current = usage.get(userId)!;

  if (current.count >= DAILY_LIMIT) {
    return {
      allowed: false,
      remaining: 0,
      limit: DAILY_LIMIT,
    };
  }

  return {
    allowed: true,
    remaining: DAILY_LIMIT - current.count,
    limit: DAILY_LIMIT,
  };
}

export function incrementUsage(userId: string): void {
  const today = getBangkokDate();
  const userUsage = usage.get(userId);

  if (!userUsage || userUsage.resetDate !== today) {
    usage.set(userId, { count: 1, resetDate: today });
  } else {
    userUsage.count++;
  }
}

export function getUsage(userId: string): { used: number; limit: number } {
  const today = getBangkokDate();
  const userUsage = usage.get(userId);

  if (!userUsage || userUsage.resetDate !== today) {
    return { used: 0, limit: DAILY_LIMIT };
  }

  return { used: userUsage.count, limit: DAILY_LIMIT };
}
