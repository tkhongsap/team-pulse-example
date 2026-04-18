import { test, expect } from "@playwright/test";

test.describe("Team Pulse app", () => {
  test("home page loads without login", async ({ page }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: "Team Pulse" })
    ).toBeVisible();
  });

  test("chat round-trip via stub server", async ({ page }) => {
    await page.goto("/");

    await page.getByText("Who needs help?").click();

    const sendBtn = page.getByRole("button", { name: "Send" });
    await expect(sendBtn).toBeEnabled({ timeout: 5_000 });
    await sendBtn.click();

    // The user question should appear
    await expect(
      page.getByText("highest burnout risk", { exact: false })
    ).toBeVisible({ timeout: 5_000 });

    // The stub server returns sources: ["wiki/index.md"]
    // which renders a source citation link
    await expect(page.getByRole("link", { name: "index" })).toBeVisible({
      timeout: 15_000,
    });
  });

  test("usage counter is visible", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText(/\d+\/100 queries/)).toBeVisible();
  });

  test("/login redirects to home", async ({ page }) => {
    await page.goto("/login");
    await page.waitForURL("/");
    await expect(
      page.getByRole("heading", { name: "Team Pulse" })
    ).toBeVisible();
  });

  test("report page strips frontmatter and shows metadata summary", async ({
    page,
  }) => {
    await page.goto("/reports/2026-04-16/eod-summary");

    await expect(
      page.getByText("Parsed from frontmatter instead of rendered in the report body.")
    ).toBeVisible();
    await expect(page.getByText("Report metadata")).toBeVisible();
    await expect(page.locator("body")).not.toContainText(
      'title: "End-of-Day Summary'
    );
    await expect(page.locator("body")).toContainText("End-of-Day Summary — 2026-04-16");
    await expect(page.locator("body")).toContainText("Report age");
    await expect(page.locator("body")).toContainText("Source files");
  });

  test("report API returns parsed metadata and stripped markdown", async ({
    request,
  }) => {
    const response = await request.get("/api/reports/2026-04-16/eod-summary");
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    expect(data.title).toContain("End-of-Day Summary");
    expect(data.tags).toContain("report");
    expect(data.sources.length).toBeGreaterThan(0);
    expect(data.resolvedDate).toBe("2026-04-16");
    expect(data.isFallback).toBe(false);
    expect(data.content).toContain("# End-of-Day Summary");
    expect(data.content).not.toContain('title: "End-of-Day Summary');
  });
});
