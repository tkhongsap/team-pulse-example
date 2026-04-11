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
});
