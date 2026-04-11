const STORAGE_KEY = "teamPulseAnonymousId";

export function getAnonymousId(): string {
  if (typeof window === "undefined") return "server";

  let id = localStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}
