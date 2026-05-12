import re
import time
from datetime import datetime
from pathlib import Path

import psycopg2
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8072"
DB_NAME = "allnetwork"
LOGIN = "admin"
PASSWORD = "admin"
COMPANY_NAME = "ALLNETWORKS Caribbean Holdings Ltd"
ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "docs" / "scenario_screenshots"


SCREENS = [
    {
        "slug": "01_operations_dashboard",
        "title": "Operations Dashboard",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_dashboard",
        "view_type": "form",
    },
    {"slug": "02_employees_all", "title": "All Employees", "model": "hr.employee", "view_type": "list"},
    {"slug": "03_departments", "title": "Departments", "model": "hr.department", "view_type": "list"},
    {"slug": "04_job_positions", "title": "Job Positions", "model": "hr.job", "view_type": "list"},
    {
        "slug": "05_contract_templates",
        "title": "Contract Templates",
        "action_xmlid": "hr.action_hr_contract_templates",
        "model": "hr.version",
        "view_type": "list",
    },
    {
        "slug": "06_training_sessions",
        "title": "Training Sessions",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_training",
        "view_type": "list",
    },
    {
        "slug": "07_training_attendance",
        "title": "Training Attendance Records",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_training_attendance",
        "view_type": "list",
    },
    {"slug": "08_attendances_all", "title": "All Attendances", "model": "hr.attendance", "view_type": "list"},
    {"slug": "09_time_off_all", "title": "All Time Off", "model": "hr.leave", "view_type": "list"},
    {
        "slug": "10_accrual_plans",
        "title": "Accrual Plans",
        "action_xmlid": "hr_holidays.open_view_accrual_plans",
        "model": "hr.leave.accrual.plan",
        "view_type": "list",
    },
    {"slug": "11_work_entries", "title": "Work Entries", "model": "hr.work.entry", "view_type": "list"},
    {"slug": "12_payroll_batches", "title": "Payroll Batches", "model": "hr.payslip.run", "view_type": "list"},
    {"slug": "13_payslips_all", "title": "All Payslips", "model": "hr.payslip", "view_type": "list"},
    {
        "slug": "14_salary_structures",
        "title": "Salary Structures",
        "model": "hr.payroll.structure",
        "view_type": "list",
    },
    {"slug": "15_salary_rules", "title": "Salary Rules", "model": "hr.salary.rule", "view_type": "list"},
    {
        "slug": "16_other_input_types",
        "title": "Other Input Types",
        "model": "hr.payslip.input.type",
        "view_type": "list",
    },
    {
        "slug": "17_mass_operations",
        "title": "Mass Operations",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_mass_operation",
        "view_type": "list",
    },
    {
        "slug": "18_employee_expenses",
        "title": "Employee Expenses",
        "action_xmlid": "hr_expense.action_hr_expense_account",
        "model": "hr.expense",
        "view_type": "list",
    },
    {
        "slug": "19_bank_transfers",
        "title": "Bank Transfers",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_bank_transfer",
        "view_type": "list",
    },
    {
        "slug": "20_demo_scenarios",
        "title": "Demo Scenarios",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_scenario",
        "view_type": "list",
    },
    {
        "slug": "21_department_payroll_summary",
        "title": "Department Payroll Summary",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_department_summary",
        "view_type": "list",
    },
    {
        "slug": "22_payroll_reconciliation",
        "title": "Payroll Reconciliation",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_reconciliation",
        "view_type": "list",
    },
    {
        "slug": "23_accounting_dashboard",
        "title": "Accounting Dashboard",
        "action_xmlid": "account.open_account_journal_dashboard_kanban",
        "model": "account.journal",
        "view_type": "kanban",
    },
    {
        "slug": "24_hr_payroll_accounting_entries",
        "title": "HR Payroll Accounting Entries",
        "action_xmlid": "hr_payroll_demo_enterprise.action_hr_payroll_demo_accounting_entries",
        "view_type": "list",
    },
    {"slug": "25_all_journal_entries", "title": "All Journal Entries", "model": "account.move", "view_type": "list"},
    {
        "slug": "26_journal_items",
        "title": "Journal Items",
        "action_xmlid": "account.action_account_moves_all",
        "model": "account.move.line",
        "view_type": "list",
    },
    {"slug": "27_journals", "title": "Journals", "model": "account.journal", "view_type": "list"},
    {"slug": "28_chart_of_accounts", "title": "Chart of Accounts", "model": "account.account", "view_type": "list"},
]


def connect_db():
    return psycopg2.connect(dbname=DB_NAME, user="odoo19", password="odoo19", host="127.0.0.1", port="5432")


def resolve_company_id(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM res_company WHERE name = %s LIMIT 1", [COMPANY_NAME])
        row = cur.fetchone()
        if not row:
            raise RuntimeError(f"Company not found: {COMPANY_NAME}")
        return row[0]


def resolve_xmlid(conn, xmlid):
    module, name = xmlid.split(".", 1)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT model, res_id FROM ir_model_data WHERE module = %s AND name = %s LIMIT 1",
            [module, name],
        )
        return cur.fetchone()


def resolve_action(conn, screen):
    if screen.get("action_xmlid"):
        row = resolve_xmlid(conn, screen["action_xmlid"])
        if row:
            return row[1]
    model = screen.get("model")
    if not model:
        return None
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
              FROM ir_act_window
             WHERE res_model = %s
          ORDER BY usage = 'menu' DESC, id
             LIMIT 1
            """,
            [model],
        )
        row = cur.fetchone()
        return row[0] if row else None


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def login(page):
    page.goto(f"{BASE_URL}/web/login?db={DB_NAME}", wait_until="domcontentloaded")
    if page.locator(".o_web_client").count():
        return
    page.fill("input[name='login']", LOGIN)
    page.fill("input[name='password']", PASSWORD)
    page.click("form[action*='/web/login'] button[type='submit'], .oe_login_form button[type='submit']")
    page.wait_for_selector(".o_web_client", timeout=60000)


def wait_for_odoo(page):
    page.wait_for_selector(".o_action_manager", timeout=60000)
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1200)


def clear_view_filters(page):
    # Remove Odoo search facets such as Favorites, My records, default date ranges, or dashboard filters.
    for _ in range(20):
        remove_buttons = page.locator(
            ".o_searchview_facet .o_facet_remove, "
            ".o_searchview_facet .fa-times, "
            ".o_searchview_facet .oi-close"
        )
        count = remove_buttons.count()
        if not count:
            break
        remove_buttons.first.click()
        page.wait_for_timeout(250)

    search_inputs = page.locator(".o_searchview_input")
    if search_inputs.count():
        search_inputs.first.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.press("Enter")
        page.wait_for_timeout(800)


def switch_to_requested_view(page, view_type):
    if view_type not in {"list", "kanban", "form"}:
        return
    selectors = {
        "list": "button.o_switch_view.o_list, button[aria-label='List']",
        "kanban": "button.o_switch_view.o_kanban, button[aria-label='Kanban']",
        "form": "button.o_switch_view.o_form, button[aria-label='Form']",
    }
    button = page.locator(selectors[view_type])
    if button.count():
        try:
            button.first.click()
            page.wait_for_timeout(800)
        except Exception:
            pass


def capture_screen(page, screen, action_id, company_id, output_dir):
    params = [f"cids={company_id}"]
    if action_id:
        params.append(f"action={action_id}")
    if screen.get("model"):
        params.append(f"model={screen['model']}")
    if screen.get("view_type"):
        params.append(f"view_type={screen['view_type']}")
    page.goto(f"{BASE_URL}/web#{'&'.join(params)}", wait_until="domcontentloaded")
    wait_for_odoo(page)
    clear_view_filters(page)
    switch_to_requested_view(page, screen.get("view_type"))
    clear_view_filters(page)
    page.wait_for_timeout(1000)

    filename = f"{screen['slug']}-{slugify(screen['title'])}.png"
    path = output_dir / filename
    page.screenshot(path=str(path), full_page=True)
    return path


def main():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    run_dir = SCREENSHOT_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    conn = connect_db()
    company_id = resolve_company_id(conn)
    resolved = [(screen, resolve_action(conn, screen)) for screen in SCREENS]
    conn.close()

    captures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            device_scale_factor=1,
            ignore_https_errors=True,
        )
        page = context.new_page()
        login(page)

        for index, (screen, action_id) in enumerate(resolved, start=1):
            if not action_id and screen.get("action_xmlid"):
                print(f"[skip] {screen['title']}: action not found")
                continue
            start = time.time()
            try:
                path = capture_screen(page, screen, action_id, company_id, run_dir)
                captures.append((screen["title"], path.name))
                print(f"[{index:02d}] captured {screen['title']} -> {path.name} ({time.time() - start:.1f}s)")
            except Exception as exc:
                print(f"[{index:02d}] failed {screen['title']}: {exc}")

        context.close()
        browser.close()

    index_md = run_dir / "SCREENSHOT_INDEX.md"
    index_md.write_text(
        "\n".join(
            [
                "# Scenario Screenshot Index",
                "",
                f"Captured from `{BASE_URL}` database `{DB_NAME}`.",
                "",
                "All visible search facets were removed before each screenshot.",
                "",
                *[f"- `{filename}` - {title}" for title, filename in captures],
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Saved {len(captures)} screenshots to {run_dir}")
    print(f"Index: {index_md}")


if __name__ == "__main__":
    main()
