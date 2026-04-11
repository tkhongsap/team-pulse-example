import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: "http://localhost:3000",
    headless: true,
  },
  webServer: [
    {
      command: "python3 ../scripts/stub_ask_server.py --port 3999",
      url: "http://localhost:3999",
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "ASK_SERVER_URL=http://localhost:3999 npm run dev",
      url: "http://localhost:3000",
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
  ],
});
