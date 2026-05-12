// Playwright walkthrough for HR Payroll Demo Enterprise.
//
// Environment:
//   ODOO_URL=http://127.0.0.1:8069
//   ODOO_DB=your_db
//   ODOO_LOGIN=admin
//   ODOO_PASSWORD=admin
//
// Run:
//   npx playwright test hr_payroll_demo_walkthrough.spec.js

const { test, expect } = require("@playwright/test");
const fs = require("fs");
const path = require("path");

const BASE = (process.env.ODOO_URL || "http://127.0.0.1:8069").replace(/\/$/, "");
const DB = process.env.ODOO_DB || "";
const LOGIN = process.env.ODOO_LOGIN || "admin";
const PASSWORD = process.env.ODOO_PASSWORD || "admin";
const OUT = path.resolve(__dirname, "..", "screenshots");

async function login(page) {
  const url = DB ? `${BASE}/web/login?db=${encodeURIComponent(DB)}` : `${BASE}/web/login`;
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.locator("#login").fill(LOGIN);
  await page.locator("#password").fill(PASSWORD);
  await page.getByRole("button", { name: "Log in" }).click();
  await page.waitForURL(/\/odoo/, { timeout: 120000 });
}

async function snap(page, name) {
  fs.mkdirSync(OUT, { recursive: true });
  await page.screenshot({ path: path.join(OUT, name), fullPage: true });
}

test("HR payroll demo flow", async ({ page }) => {
  await login(page);
  await snap(page, "01_home.png");

  await page.goto(`${BASE}/odoo/action-hr_payroll_demo_enterprise.action_hr_payroll_demo_dashboard`);
  await expect(page.getByText("ALLNETWORKS Payroll Operations Dashboard")).toBeVisible({ timeout: 60000 });
  await snap(page, "02_dashboard.png");

  await page.getByRole("button", { name: "Validate Attendance" }).click();
  await snap(page, "03_attendance_mass_operation.png");

  await page.goto(`${BASE}/odoo/action-hr_payroll_demo_enterprise.action_hr_payroll_demo_mass_operation`);
  await snap(page, "04_mass_operations.png");

  await page.goto(`${BASE}/odoo/action-hr_payroll_demo_enterprise.action_hr_payroll_demo_bank_transfer`);
  await snap(page, "05_bank_transfers.png");

  await page.goto(`${BASE}/odoo/action-hr_payroll_demo_enterprise.action_hr_payroll_demo_department_summary`);
  await snap(page, "06_department_summary.png");

  await page.goto(`${BASE}/odoo/action-hr_payroll_demo_enterprise.action_hr_payroll_demo_reconciliation`);
  await snap(page, "07_reconciliation.png");
});
