import { defineConfig, devices } from "@playwright/test";
import { baseURL, localTLS } from "./e2e/environment";
export default defineConfig({
  testDir: "./e2e",
  timeout: 120_000,
  workers: 1,
  use: {
    baseURL,
    ignoreHTTPSErrors: localTLS,
    timezoneId: process.env.E2E_TIMEZONE || "Asia/Ho_Chi_Minh",
    channel: "chrome",
    trace: "retain-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    {
      name: "mobile",
      use: { ...devices["iPhone 13"], defaultBrowserType: "chromium" },
    },
  ],
});
