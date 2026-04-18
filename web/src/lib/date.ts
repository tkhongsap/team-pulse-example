export const TEAM_PULSE_TIMEZONE = "Asia/Bangkok";

function getDatePartsInTimeZone(
  date: Date,
  timeZone: string = TEAM_PULSE_TIMEZONE
) {
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  const parts = formatter.formatToParts(date);
  const values = Object.fromEntries(
    parts
      .filter((part) => part.type !== "literal")
      .map((part) => [part.type, part.value])
  ) as Record<"year" | "month" | "day", string>;

  return {
    year: values.year,
    month: values.month,
    day: values.day,
  };
}

function parseIsoDate(date: string) {
  const [year, month, day] = date.split("-").map(Number);
  return { year, month, day };
}

function isoDateToUtcMs(date: string) {
  const { year, month, day } = parseIsoDate(date);
  return Date.UTC(year, month - 1, day);
}

export function getBangkokTodayDate(now: Date = new Date()) {
  const { year, month, day } = getDatePartsInTimeZone(now);
  return `${year}-${month}-${day}`;
}

export function formatBangkokCalendarDate(now: Date = new Date()) {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: TEAM_PULSE_TIMEZONE,
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(now);
}

export function formatIsoDate(date: string) {
  const { year, month, day } = parseIsoDate(date);

  return new Intl.DateTimeFormat("en-US", {
    timeZone: TEAM_PULSE_TIMEZONE,
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(Date.UTC(year, month - 1, day, 12)));
}

export function differenceInCalendarDays(laterDate: string, earlierDate: string) {
  const msPerDay = 24 * 60 * 60 * 1000;
  return Math.floor((isoDateToUtcMs(laterDate) - isoDateToUtcMs(earlierDate)) / msPerDay);
}

export function getReportAgeDays(
  reportDate: string,
  referenceDate: string = getBangkokTodayDate()
) {
  return Math.max(0, differenceInCalendarDays(referenceDate, reportDate));
}

export function formatReportAge(
  reportDate: string,
  referenceDate: string = getBangkokTodayDate()
) {
  const ageDays = getReportAgeDays(reportDate, referenceDate);

  if (ageDays === 0) {
    return "Today";
  }

  if (ageDays === 1) {
    return "1 day old";
  }

  return `${ageDays} days old`;
}
