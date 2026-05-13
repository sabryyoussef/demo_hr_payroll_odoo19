# ALLNETWORKS HR, Payroll and Accounting Demo

Production-grade Odoo 19 Enterprise demo module for a complete HR, attendance, payroll, banking, accounting, Knowledge and AI-assisted employee policy presentation.

This repository is designed as a live presentation asset. It includes a realistic company dataset, a 3+ hour demo playbook, screenshot gallery, online HTML presentation, Playwright capture tooling, Knowledge base content and an Ask Knowledge AI workflow.

## Presentation Story

**From Employees to Payroll to Accounting in One Live Odoo Story**

ALLNETWORKS Caribbean Holdings Ltd is a medium-size regional operations company with office staff, warehouse workers, field teams, support shifts, sales commissions, interns, fixed-term staff and managers. The demo shows how Odoo connects:

- HR master data
- contracts and employee categories
- training and certifications
- attendance and work entries
- time off and accruals
- payroll batches and payslips
- sporadic payments and deductions
- employee expenses
- salary bank transfers
- accounting entries and reconciliation
- employee Knowledge base questions

The goal is to prove that Odoo can handle the full payroll operation without spreadsheets: HR owns employee data, managers control exceptions, payroll calculates pay, finance sends salary transfers, and accounting closes the month.

## Demo Scale

| Area | Demo volume |
| --- | ---: |
| Active employees | 97 |
| Departments | 9 |
| Attendance records | 7,098 |
| Time off records | 60 |
| Payslips | 278 |
| Payroll batches | 4 |
| Bank transfers | 4 |
| Employee expenses | 18 |
| Training sessions | 14 |
| Training attendance lines | 177 |
| Demo scenarios | 80 |
| HR/payroll/accounting entries | 15 |
| Knowledge articles | 68 |
| Ask Knowledge AI sample questions | 10 |
| Presentation screenshots | 28 |

## What The Module Creates

- Company: `ALLNETWORKS Caribbean Holdings Ltd`
- 9 departments: Executive and Administration, HR, Finance and Accounting, Sales, Customer Support, Operations, Warehouse and Logistics, IT and Systems, Temporary and Interns
- Realistic employees with hierarchy, employee categories, positions, contract types and schedules
- Contract templates for monthly, bi-weekly, commission, remote, intern, fixed-term and seasonal cases
- Payroll structures, salary rules and input types for overtime, bonus, commission, loan, absence, retroactive adjustment and allowances
- Three months of attendance data with late check-ins, overtime, weekend work, night shift and missing check-outs
- Leave allocations, accrual plans and requests across annual, sick, casual, unpaid and emergency leave
- Monthly and bi-weekly payroll batches with payslips
- Employee expenses in draft, submitted, approved and refused states
- Salary bank transfers and reconciliation records
- HR/payroll/accounting journal entries including Salaries journal data
- Operations dashboard, mass operations, demo scenario catalog and reports
- Knowledge base handbook with policy, holidays, payroll, expenses, benefits, training, IT security, finance and employee FAQ articles
- Ask Knowledge AI screen with AI agent integration and Knowledge-search fallback

## Presentation Journey

1. **HR Foundation**: employees, departments, jobs, contracts, training and certifications.
2. **Workforce Activity**: attendance, time off, accruals and work entries that feed payroll.
3. **Payroll Execution**: batches, payslips, salary rules, inputs and mass operations.
4. **Finance Handoff**: expenses, bank transfers, payment files and reconciliation.
5. **Accounting Close**: Salaries journal, HR accounting entries, journal items and chart of accounts.
6. **Employee Self-Service**: Knowledge articles and Ask Knowledge AI questions.

## Main Odoo Menus

Open:

```text
Payroll Demo Enterprise
```

Key entries:

- `Operations Dashboard`
- `Operations > Contract Templates`
- `Operations > Bank Transfers`
- `Operations > Employee Expenses`
- `Operations > Accrual Plans`
- `Operations > Mass Operations`
- `Operations > Training & Certifications`
- `Operations > Attendance Records`
- `Operations > Ask Knowledge AI`
- `Reports > Demo Scenarios`
- `Reports > Department Payroll Summary`
- `Reports > Payroll Reconciliation`
- `Reports > Accounting Entries`

Knowledge content is available from:

```text
Knowledge > Articles > ALLNETWORKS Employee Knowledge Base
```

## Online Presentation

The interactive HTML presentation is included at:

```text
docs/online_presentation/index.html
```

It provides:

- attractive presentation landing page
- screen cards grouped by business area
- screenshot popup previews
- live Odoo screen links
- full-tab fallback for browsers that block Odoo iframe embedding

## Screenshot Gallery

All screenshots were captured with visible Odoo search filters removed.

### 01. Operations Dashboard

Executive control center for employee count, attendance alerts, payroll batches, draft payslips, bank transfers and monthly payroll totals.

![Operations Dashboard](docs/scenario_screenshots/20260513_110401/01_operations_dashboard-operations-dashboard.png)

### 02. All Employees

Full employee population across office, sales, support, operations, warehouse, IT, fixed-term and intern categories.

![All Employees](docs/scenario_screenshots/20260513_110401/02_employees_all-all-employees.png)

### 03. Departments

Nine-department company structure used for managers, reporting, payroll cost analysis and approvals.

![Departments](docs/scenario_screenshots/20260513_110401/03_departments-departments.png)

### 04. Job Positions

Role catalog for executives, HR, finance, sales, support, field operations, warehouse logistics and IT.

![Job Positions](docs/scenario_screenshots/20260513_110401/04_job_positions-job-positions.png)

### 05. Contract Templates

Reusable contract templates for monthly salary, commission, shift, bi-weekly, remote, fixed-term, intern and seasonal cases.

![Contract Templates](docs/scenario_screenshots/20260513_110401/05_contract_templates-contract-templates.png)

### 06. Training Sessions

Training and certification sessions covering induction, safety, AML, payroll system training, customer service and IT security.

![Training Sessions](docs/scenario_screenshots/20260513_110401/06_training_sessions-training-sessions.png)

### 07. Training Attendance Records

Participant attendance, status, score and certification evidence for HR compliance and operational readiness.

![Training Attendance Records](docs/scenario_screenshots/20260513_110401/07_training_attendance-training-attendance-records.png)

### 08. All Attendances

Attendance history for office, support shift, field, warehouse day shift, warehouse night shift and remote employees.

![All Attendances](docs/scenario_screenshots/20260513_110401/08_attendances_all-all-attendances.png)

### 09. All Time Off

Approved, pending and refused leave cases across annual, sick, casual, unpaid and emergency leave types.

![All Time Off](docs/scenario_screenshots/20260513_110401/09_time_off_all-all-time-off.png)

### 10. Accrual Plans

Leave accrual policies for standard annual leave, sick leave, hourly worked-time, probation and interns.

![Accrual Plans](docs/scenario_screenshots/20260513_110401/10_accrual_plans-accrual-plans.png)

### 11. Work Entries

The bridge between schedules, attendance, time off and payroll calculation before payslips are finalized.

![Work Entries](docs/scenario_screenshots/20260513_110401/11_work_entries-work-entries.png)

### 12. Payroll Batches

Monthly and bi-weekly payroll batches used to organize payslips by period and workforce type.

![Payroll Batches](docs/scenario_screenshots/20260513_110401/12_payroll_batches-payroll-batches.png)

### 13. All Payslips

Payslip population showing payroll outcomes, wage calculations, inputs, deductions and employee net pay.

![All Payslips](docs/scenario_screenshots/20260513_110401/13_payslips_all-all-payslips.png)

### 14. Salary Structures

Payroll structure configuration for regular employees and workers with different payroll schedules.

![Salary Structures](docs/scenario_screenshots/20260513_110401/14_salary_structures-salary-structures.png)

### 15. Salary Rules

Rules for base pay, allowances, overtime, bonus, commission, retroactive adjustment, loan recovery and absence penalty.

![Salary Rules](docs/scenario_screenshots/20260513_110401/15_salary_rules-salary-rules.png)

### 16. Other Input Types

Controlled sporadic inputs such as `OVERTIME`, `BONUS`, `COMMISSION`, `LOAN`, `ABSENCE`, `RETRO`, `TRANSPORT` and `HOUSING`.

![Other Input Types](docs/scenario_screenshots/20260513_110401/16_other_input_types-other-input-types.png)

### 17. Mass Operations

Batch operations for employee updates, attendance adjustment, leave approval, payslip generation, payslip approval and bank transfers.

![Mass Operations](docs/scenario_screenshots/20260513_110401/17_mass_operations-mass-operations.png)

### 18. Employee Expenses

Employee-paid, company-paid, submitted, approved and refused expense cases that complete the employee finance workflow.

![Employee Expenses](docs/scenario_screenshots/20260513_110401/18_employee_expenses-employee-expenses.png)

### 19. Bank Transfers

Payroll-to-bank handoff showing payment lines, employee bank accounts, payment file preview, approval and reconciliation status.

![Bank Transfers](docs/scenario_screenshots/20260513_110401/19_bank_transfers-bank-transfers.png)

### 20. Demo Scenarios

Scenario catalog for quickly jumping into payroll, leave, attendance, accounting and reporting stories during the presentation.

![Demo Scenarios](docs/scenario_screenshots/20260513_110401/20_demo_scenarios-demo-scenarios.png)

### 21. Department Payroll Summary

Management report for department payroll totals, overtime, attendance violations, leave load and transfer amounts.

![Department Payroll Summary](docs/scenario_screenshots/20260513_110401/21_department_payroll_summary-department-payroll-summary.png)

### 22. Payroll Reconciliation

Finance review of matched salary transfers, differences, exceptions and reconciliation notes.

![Payroll Reconciliation](docs/scenario_screenshots/20260513_110401/22_payroll_reconciliation-payroll-reconciliation.png)

### 23. Accounting Dashboard

Accounting control board with Salaries, HR Payroll Accounting and Salary Bank journals visible for the payroll close story.

![Accounting Dashboard](docs/scenario_screenshots/20260513_110401/23_accounting_dashboard-accounting-dashboard.png)

### 24. HR Payroll Accounting Entries

Curated HR, payroll, expense, bank, accrual, loan, retroactive and reconciliation journal entries.

![HR Payroll Accounting Entries](docs/scenario_screenshots/20260513_110401/24_hr_payroll_accounting_entries-hr-payroll-accounting-entries.png)

### 25. All Journal Entries

Native accounting journal entry list for posted and draft moves across the company.

![All Journal Entries](docs/scenario_screenshots/20260513_110401/25_all_journal_entries-all-journal-entries.png)

### 26. Journal Items

Detailed debit and credit lines for payroll expenses, payroll payable, salary bank, leave liability and expense reimbursements.

![Journal Items](docs/scenario_screenshots/20260513_110401/26_journal_items-journal-items.png)

### 27. Journals

Journal configuration for Salaries, HR Payroll Accounting, Salary Bank, sales, purchases and miscellaneous operations.

![Journals](docs/scenario_screenshots/20260513_110401/27_journals-journals.png)

### 28. Chart of Accounts

Payroll-related accounts for salary expense, overtime, bonus, employer cost, payroll payable, leave liability and bank clearing.

![Chart of Accounts](docs/scenario_screenshots/20260513_110401/28_chart_of_accounts-chart-of-accounts.png)

## Knowledge And AI

The module creates a searchable Knowledge base:

```text
ALLNETWORKS Employee Knowledge Base
```

It includes policy and FAQ articles for:

- company handbook
- holidays and attendance
- overtime and night shifts
- time off and accruals
- payroll and payslips
- expenses and reimbursements
- benefits and employee support
- training and certifications
- IT security and data protection
- finance, banking and accounting
- manager approval playbooks
- employee FAQs

The Ask screen is available at:

```text
Payroll Demo Enterprise > Operations > Ask Knowledge AI
```

It uses an `ai.agent` connected to the Knowledge base when AI provider credentials are configured. If a provider/token is unavailable, it falls back to deterministic Knowledge search so the demo remains usable.

## Installation

This repository is Odoo.sh-friendly: the repository root contains the addon directory:

```text
hr_payroll_demo_enterprise/
```

For local development, add the parent folder to `addons_path`, update apps, then install:

```text
hr_payroll_demo_enterprise
```

The module post-init hook seeds the complete dataset automatically.

## Dependencies

This module uses the real Odoo 19 Enterprise stack:

- `hr_payroll_account`
- `account`
- `hr_attendance`
- `hr_holidays`
- `hr_skills`
- `hr_expense`
- `ai_knowledge`

## Documentation

- [Three Hour Demo Playbook](docs/THREE_HOUR_HR_PAYROLL_ACCOUNTING_DEMO_PLAYBOOK.md)
- [100 Employee HR, Payroll and Accounting Use Cases](docs/100_EMPLOYEE_HR_PAYROLL_ACCOUNTING_USE_CASES.md)
- [Demo Scenarios Guide](docs/DEMO_SCENARIOS_GUIDE.md)
- [Functional Workflow Guide](docs/FUNCTIONAL_WORKFLOW_GUIDE.md)
- [User Walkthrough](docs/USER_WALKTHROUGH.md)
- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Screenshot Index](docs/scenario_screenshots/20260513_110401/SCREENSHOT_INDEX.md)
- [Online Presentation HTML](docs/online_presentation/index.html)

## Demo Message

> Odoo can handle medium-size payroll operations efficiently, with dashboards, mass actions, payroll batches, banking handoff, Knowledge self-service, AI-assisted policy questions and accounting reconciliation in one realistic operational company.

## Important Notes

- This is a demo module. Do not install it in a production customer database.
- Data is generated with stable external IDs through the post-init hook.
- The generated dataset is intentionally interconnected for presentation value.
- Screenshots are included for presentation and documentation purposes.
