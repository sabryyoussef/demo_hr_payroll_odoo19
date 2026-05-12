# Three Hour HR, Payroll and Accounting Demo Playbook

Company: `ALLNETWORKS Caribbean Holdings Ltd`

Module: `hr_payroll_demo_enterprise`

Purpose: run a complete Odoo 19 demo that shows how employee data, HR operations, attendance, work entries, time off, payroll, expenses, banking and accounting work together in one realistic company cycle.

This playbook is designed for a presentation longer than 3 hours. It is not a feature checklist. It is a business story: HR maintains people and contracts, managers control attendance and leave, payroll calculates and validates pay, finance pays employees, and accounting reconciles and audits the result.

## Demo Data Available

Use the current demo database as a realistic operating company.

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
| Demo scenario records | 80 |
| HR/payroll/accounting entries | 15 |
| Native `Salaries` journal entries | 4 |

Core departments:

- Executive and Administration
- Human Resources
- Finance and Accounting
- Sales
- Customer Support
- Operations
- Warehouse and Logistics
- IT and Systems
- Temporary and Interns

Employee categories to show in filters, employee forms and reporting:

- Full-time salaried
- Hourly operations
- Warehouse bi-weekly
- Sales commission
- Managers
- Fixed-term contract
- Interns
- Remote and hybrid
- Sporadic one-time bonus
- Sporadic exceptional commission
- Sporadic overtime payout
- Sporadic temporary allowance
- Sporadic retroactive adjustment
- Sporadic deduction or recovery
- Sporadic final payoff

## Presenter Setup

Before starting:

1. Switch to company `ALLNETWORKS Caribbean Holdings Ltd`.
2. Open `Payroll Demo Enterprise > Operations Dashboard`.
3. Keep browser tabs ready for `Employees`, `Payroll`, `Time Off`, `Attendances`, `Expenses`, `Accounting`, and the custom `Payroll Demo Enterprise` menu.
4. If a menu looks empty, confirm the active company first.
5. Do not create many new records during the main demo. Prefer opening seeded records, duplicating only when you want to show creation.

Recommended presenter roles:

- HR Manager: owns employees, contracts, skills, training, time off policy and mass HR updates.
- Department Manager: reviews attendance, overtime, leave requests and team cost.
- Payroll Officer: generates work entries, reviews payslips, inputs sporadic payments and validates payroll batches.
- Finance Officer: prepares expenses, bank transfers and payment exceptions.
- Accountant: reviews journals, salary entries, expense entries, accruals and reconciliation.
- Executive: reviews dashboards and management reports.

## 3+ Hour Agenda

| Time | Segment | Main screens |
| ---: | --- | --- |
| 0:00-0:10 | Executive story and company context | Operations Dashboard, Demo Scenarios |
| 0:10-0:30 | Organization and employee master data | Employees, Departments, Jobs, Employee Categories |
| 0:30-0:50 | Contracts, templates and employment scenarios | Contract Templates, Employee form, Salary/Contract tab |
| 0:50-1:10 | Skills, certifications and training attendance | Skills, Resume, Training & Certifications, Attendance Records |
| 1:10-1:35 | Attendance, schedules and exceptions | Attendances, Attendance Alerts, Mass Operations |
| 1:35-2:00 | Time off, accruals and work entries | Time Off, Accrual Plans, Work Entries |
| 2:00-2:35 | Payroll batches, payslips and sporadic inputs | Payroll Batches, Payslips, Salary Rules, Demo Scenarios |
| 2:35-2:55 | Expenses and reimbursements | Employee Expenses, Accounting Entries |
| 2:55-3:15 | Banking and salary transfer operations | Bank Transfers, Salary Bank journal |
| 3:15-3:40 | Accounting dashboard, journals and reconciliation | Accounting Dashboard, Salaries journal, HR Accounting Entries |
| 3:40-4:00 | Reports, audit, mass operations and wrap-up | Department Summary, Payroll Reconciliation, Scenario catalog |

If the audience asks many questions, pause after each major segment and use the scenario catalog at the end as optional deep-dive material.

## Navigation Map

Custom demo screens:

- `Payroll Demo Enterprise > Operations Dashboard`
- `Payroll Demo Enterprise > Operations > Contract Templates`
- `Payroll Demo Enterprise > Operations > Bank Transfers`
- `Payroll Demo Enterprise > Operations > Employee Expenses`
- `Payroll Demo Enterprise > Operations > Accrual Plans`
- `Payroll Demo Enterprise > Operations > Mass Operations`
- `Payroll Demo Enterprise > Operations > Training & Certifications`
- `Payroll Demo Enterprise > Operations > Attendance Records`
- `Payroll Demo Enterprise > Reports > Demo Scenarios`
- `Payroll Demo Enterprise > Reports > Department Payroll Summary`
- `Payroll Demo Enterprise > Reports > Payroll Reconciliation`
- `Payroll Demo Enterprise > Reports > Accounting Entries`

Native Odoo screens to include:

- `Employees > Employees`
- `Employees > Departments`
- `Employees > Configuration > Job Positions`
- `Employees > Configuration > Employee Tags`
- `Attendances > Attendances`
- `Time Off > Time Off`
- `Time Off > Approvals`
- `Time Off > Configuration > Time Off Types`
- `Payroll > Payslips`
- `Payroll > Batches`
- `Payroll > Work Entries`
- `Payroll > Configuration > Salary Structures`
- `Payroll > Configuration > Salary Rules`
- `Payroll > Configuration > Other Input Types`
- `Expenses > Expenses`
- `Accounting > Dashboard`
- `Accounting > Accounting > Journal Entries`
- `Accounting > Accounting > Journal Items`
- `Accounting > Configuration > Journals`
- `Accounting > Configuration > Chart of Accounts`
- `Accounting > Reporting`

## Opening Script

Say:

"ALLNETWORKS Caribbean Holdings is a medium-size company with office employees, warehouse workers, field operations, support shifts, sales commissions, interns and fixed-term staff. The demo shows a realistic payroll month: HR maintains people, attendance and leave create work entries, payroll calculates payslips, finance pays employees, and accounting posts and reconciles the result."

Open:

```text
Payroll Demo Enterprise > Operations Dashboard
```

Show:

- Employee count and department count.
- Open leave count.
- Attendance alerts.
- Payroll batches and draft payslips.
- Pending bank transfers.
- Monthly net payroll amount.

Explain:

"This dashboard is the operational control center. It is not replacing Odoo HR or Accounting. It links the most important screens so the presenter can move through the story with fewer clicks."

## Segment 1 - Company and Organization

### Scenario 1.1 - Executive Organization Overview

Screen:

```text
Employees > Departments
```

Story:

The company has nine departments and a manager hierarchy. Open the department list and group or filter by company.

Demo steps:

1. Open the department list.
2. Show the executive, HR, finance, sales, support, operations, warehouse, IT and temporary departments.
3. Open `Warehouse and Logistics`.
4. Show manager and employees.
5. Explain that department assignment drives reporting and payroll cost grouping.

Expected result:

The audience sees a full organization, not isolated employee examples.

### Scenario 1.2 - Job Positions and Workforce Mix

Screen:

```text
Employees > Configuration > Job Positions
```

Story:

The demo includes office jobs, sales roles, support roles, field roles and warehouse jobs.

Demo steps:

1. Search for `Warehouse`.
2. Open a warehouse job such as `Picker`, `Driver` or `Forklift Operator`.
3. Search for `Sales`.
4. Open a sales role and compare it with a support or finance role.

Expected result:

Odoo can separate staffing, payroll policy and reporting by job and department.

### Scenario 1.3 - Employee Categories

Screen:

```text
Employees > Employees
```

Story:

Employee tags/categories help HR and payroll quickly identify payroll treatment.

Demo steps:

1. Open employee list.
2. Add filter or group by tags/categories if available in the view.
3. Show full-time salaried, hourly operations, warehouse bi-weekly, sales commission and sporadic categories.
4. Open a sales employee with commission category.
5. Open a warehouse employee with bi-weekly/hourly category.

Expected result:

The audience sees how categories support fast filtering and payroll control.

## Segment 2 - Employee Master Data

### Scenario 2.1 - Employee Profile From HR View

Screen:

```text
Payroll Demo Enterprise > Operations Dashboard > Employees
```

Story:

HR opens employees directly from the operations dashboard.

Demo steps:

1. Click the dashboard employees smart action.
2. Open an employee from Sales or Warehouse.
3. Show work email, work phone, department, job, manager and work location.
4. Show private/contact information only if appropriate for the audience.

Expected result:

The employee profile becomes the center of the HR story.

### Scenario 2.2 - Manager Hierarchy

Screen:

```text
Employees > Employees
```

Story:

Approvals and reporting depend on manager relationships.

Demo steps:

1. Open a support agent.
2. Show the manager.
3. Navigate to the manager record.
4. Show team members from the manager's department.

Expected result:

The audience understands why employee hierarchy matters for time off and attendance review.

### Scenario 2.3 - Work Location and Remote Work

Screen:

```text
Employees > Employees
```

Story:

Different employees work in headquarters, warehouse, field service and remote/hybrid locations.

Demo steps:

1. Search employees by IT or field operations.
2. Open a remote/hybrid employee.
3. Show the work location and schedule.
4. Explain that location supports attendance, reporting and policy differences.

Expected result:

Remote and field employees are handled without creating separate spreadsheets.

### Scenario 2.4 - Banking Data Readiness

Screen:

```text
Employees > Employees
```

Story:

Payroll cannot be sent to the bank unless employee bank data is ready.

Demo steps:

1. Open an employee that has a bank account.
2. Show bank account information.
3. Explain that the bank transfer workflow checks missing bank accounts.
4. Later, open `Bank Transfers` and show line status.

Expected result:

The audience sees why HR data quality affects finance.

## Segment 3 - Contracts and Templates

### Scenario 3.1 - Contract Template Library

Screen:

```text
Payroll Demo Enterprise > Operations > Contract Templates
```

Story:

HR does not need to manually invent a contract each time. Templates cover the main workforce types.

Show templates:

- `Executive Leadership - Monthly Salary`
- `HR & Payroll Specialist - Monthly Salary`
- `Finance Accountant - Monthly Salary`
- `Sales Representative - Monthly + Commission`
- `Customer Support Agent - Shift Schedule`
- `Field Technician - Bi-weekly Attendance`
- `Warehouse Day Shift - Bi-weekly Hourly`
- `Warehouse Night Shift - Premium Hourly`
- `IT Systems Analyst - Remote Hybrid`
- `Fixed-term Project Contractor`
- `Part-time Internship - Training Plan`
- `Seasonal Warehouse Peak Staffing`

Demo steps:

1. Open the contract template list.
2. Open the sales commission template.
3. Show department, job, contract type, schedule, wage and payroll structure.
4. Open the warehouse night shift template.
5. Compare it with the executive monthly template.

Expected result:

The audience sees that Odoo supports different contract patterns in one company.

### Scenario 3.2 - Monthly Salaried Employee

Screen:

```text
Employees > Employees
```

Story:

Full-time office employees are paid monthly with standard structure and allowances.

Demo steps:

1. Open a finance or HR employee.
2. Show department, job and contract/salary information.
3. Open related payslip later to show monthly salary.

Expected result:

Monthly payroll is clearly separated from bi-weekly and hourly payroll.

### Scenario 3.3 - Bi-weekly Warehouse Worker

Screen:

```text
Employees > Employees
```

Story:

Warehouse workers are paid bi-weekly and are more attendance-sensitive.

Demo steps:

1. Open a warehouse employee.
2. Show work schedule and contract wage.
3. Open attendance records for this employee.
4. Later show the bi-weekly payroll batch.

Expected result:

Odoo handles payroll calendars beyond monthly payroll.

### Scenario 3.4 - Sales Commission Employee

Screen:

```text
Employees > Employees
```

Story:

Sales employees can receive base pay plus commission inputs.

Demo steps:

1. Open a sales employee.
2. Show sales commission category.
3. Open current payslip and show `COMMISSION` input.
4. Show accounting impact in payroll accrual.

Expected result:

Sporadic commission is visible in payroll and accounting.

### Scenario 3.5 - Fixed-Term and Seasonal Contracts

Screen:

```text
Payroll Demo Enterprise > Operations > Contract Templates
```

Story:

The company hires fixed-term contractors and seasonal warehouse workers.

Demo steps:

1. Open `Fixed-term Project Contractor`.
2. Open `Seasonal Warehouse Peak Staffing`.
3. Explain contract end date, renewal and final payoff cases.
4. Link this to final payroll and accrual scenarios.

Expected result:

HR can manage temporary labor without losing payroll compliance.

## Segment 4 - Skills, Certifications and Training

### Scenario 4.1 - Skills and Resume Evidence

Screen:

```text
Employees > Employees
```

Story:

Certifications are visible on employee records and support compliance audits.

Demo steps:

1. Open a warehouse or operations employee.
2. Show resume/certification lines if available.
3. Show skills or certification entries.
4. Explain compliance requirements for forklift, first aid, payroll and safety roles.

Expected result:

Employee records are useful beyond payroll.

### Scenario 4.2 - Training Session Overview

Screen:

```text
Payroll Demo Enterprise > Operations > Training & Certifications
```

Story:

HR tracks internal training, compliance workshops and certification preparation.

Demo sessions to show:

- `Company Induction & Culture Orientation`
- `Workplace Safety & Compliance Workshop`
- `Anti-Money Laundering (AML) Compliance Briefing`
- `Odoo Payroll & HR System Training`
- `Customer Service Excellence Programme`
- `IT Security Awareness & Data Protection`
- `Forklift Operator Recertification`
- `First Aid & CPR Certification`

Demo steps:

1. Open the training session list.
2. Group by training type or status.
3. Open a completed session.
4. Show participants, attendance count, pass rate and certification status.

Expected result:

The audience sees training attendance as structured data, not an offline spreadsheet.

### Scenario 4.3 - Training Attendance Detail

Screen:

```text
Payroll Demo Enterprise > Operations > Attendance Records
```

Story:

Training attendance records show who attended, who missed, and who passed.

Demo steps:

1. Open attendance records.
2. Group by session.
3. Filter by absent or failed statuses if available.
4. Open one line and show employee, score and certification.

Expected result:

Compliance training can be reviewed employee by employee.

### Scenario 4.4 - Compliance Gap Discussion

Screen:

```text
Training & Certifications
```

Story:

Managers need to know which operational employees need recertification.

Demo steps:

1. Open forklift or safety training.
2. Show participants and scores.
3. Discuss how HR can follow up with activities or a next training session.

Expected result:

Training data connects HR compliance with operational risk.

## Segment 5 - Attendance, Schedules and Exceptions

### Scenario 5.1 - Attendance Alert Control Center

Screen:

```text
Payroll Demo Enterprise > Operations Dashboard > Attendance Alerts
```

Story:

Before payroll, HR must review missing check-outs and excessive working hours.

Demo steps:

1. Click `Attendance Alerts`.
2. Show missing check-out records.
3. Show long worked-hours records.
4. Open one attendance record.
5. Explain how corrections prevent payroll errors.

Expected result:

Attendance exceptions are visible before payroll is calculated.

### Scenario 5.2 - Native Attendance List

Screen:

```text
Attendances > Attendances
```

Story:

Managers can search and group attendance by employee, department and date.

Demo steps:

1. Open attendance list.
2. Group by employee.
3. Filter a warehouse or support employee.
4. Show three months of attendance history.

Expected result:

Odoo holds attendance detail for audit and payroll review.

### Scenario 5.3 - Missing Check-Out Correction

Screen:

```text
Payroll Demo Enterprise > Operations > Mass Operations
```

Story:

HR should not fix missing check-outs one by one during payroll cutoff.

Demo steps:

1. Create or open a mass operation.
2. Select `Batch Attendance Adjustment`.
3. Execute.
4. Read the result summary.

Expected result:

The operation reviews multiple attendance alerts and adjusts missing check-outs.

### Scenario 5.4 - Overtime Review

Screen:

```text
Attendances > Attendances
```

Story:

Overtime must be reviewed before it becomes a payroll input.

Demo steps:

1. Filter attendance where worked hours are greater than 10.
2. Open a field or warehouse employee record.
3. Discuss manager approval.
4. Later show `OVERTIME` input on the payslip.

Expected result:

The overtime amount has an operational reason.

### Scenario 5.5 - Night Shift and Cross-Day Work

Screen:

```text
Employees > Employees
```

Story:

Night shift work creates cross-day attendance and premium payroll cases.

Demo steps:

1. Open a warehouse night shift employee.
2. Show work schedule.
3. Open attendance entries around night shift dates.
4. Explain premium or overtime calculation.

Expected result:

The audience sees that Odoo can handle non-office schedules.

### Scenario 5.6 - Remote and Field Attendance

Screen:

```text
Attendances > Attendances
```

Story:

Remote IT and field operations employees have different attendance patterns.

Demo steps:

1. Filter by IT or Operations department.
2. Open remote/flexible schedule employees.
3. Compare with warehouse fixed shift attendance.

Expected result:

Different work patterns are controlled in one system.

## Segment 6 - Time Off, Accruals and Work Entries

### Scenario 6.1 - Time Off Type Policy

Screen:

```text
Time Off > Configuration > Time Off Types
```

Story:

Leave types define approvals and payroll behavior.

Demo types:

- Annual Leave
- Sick Leave
- Casual Leave
- Unpaid Leave
- Emergency Leave

Demo steps:

1. Open time off types.
2. Show paid leave versus unpaid leave.
3. Explain manager and HR validation levels.

Expected result:

Leave rules are configured, not handled manually.

### Scenario 6.2 - Employee Leave Requests

Screen:

```text
Time Off > Time Off
```

Story:

The demo includes approved, pending and refused leave cases.

Demo steps:

1. Open time off list.
2. Group by status.
3. Open an annual leave request.
4. Open an unpaid leave request.
5. Open a refused request.

Expected result:

The audience sees how status affects payroll.

### Scenario 6.3 - Bulk Leave Approval

Screen:

```text
Payroll Demo Enterprise > Operations > Mass Operations
```

Story:

Managers can approve multiple leave requests before payroll cutoff.

Demo steps:

1. Create or open `Bulk Leave Approval`.
2. Execute the operation.
3. Read affected employee count and summary.
4. Return to Time Off list and show the updated status.

Expected result:

Mass approvals reduce manual clicking.

### Scenario 6.4 - Accrual Plans

Screen:

```text
Payroll Demo Enterprise > Operations > Accrual Plans
```

Story:

Leave balances are accrued based on policy.

Demo plans:

- `ALLNETWORKS Standard Annual Leave Accrual`
- `ALLNETWORKS Sick Leave Monthly Accrual`
- `ALLNETWORKS Hourly Worked-Time Accrual`
- `ALLNETWORKS Probation Slow-Start Accrual`
- `ALLNETWORKS Intern Fixed-Term Accrual`

Demo steps:

1. Open the accrual plan list.
2. Open standard annual leave.
3. Show levels and timing.
4. Open hourly worked-time accrual.
5. Discuss warehouse/hourly employees.

Expected result:

Leave balances are governed by policy and employee type.

### Scenario 6.5 - Work Entries

Screen:

```text
Payroll > Work Entries
```

Story:

Work entries are the bridge between schedules, attendance, leave and payroll.

Demo steps:

1. Open work entries.
2. Filter by current payroll month.
3. Group by employee or work entry type.
4. Show attendance, leave and unpaid leave entries if available.
5. Explain that payroll uses this data before payslip calculation.

Expected result:

The audience understands why attendance and time off must be ready before payroll.

### Scenario 6.6 - Unpaid Leave Deduction

Screen:

```text
Time Off > Time Off
Payroll > Payslips
```

Story:

Unpaid leave reduces payroll and creates an accounting impact.

Demo steps:

1. Open an unpaid leave record.
2. Note the employee and dates.
3. Open the employee's payslip.
4. Show deduction or worked days impact.
5. Later show accounting payroll accrual.

Expected result:

Time Off is connected to payroll, not only calendar absence.

## Segment 7 - Payroll Configuration

### Scenario 7.1 - Salary Structures

Screen:

```text
Payroll > Configuration > Salary Structures
```

Story:

Salary structures define how different populations are paid.

Demo steps:

1. Open salary structures.
2. Show regular employee structure.
3. Show worker/bi-weekly structure.
4. Open rules linked to allowances and deductions.

Expected result:

Payroll is controlled by reusable configuration.

### Scenario 7.2 - Salary Rules

Screen:

```text
Payroll > Configuration > Salary Rules
```

Story:

The demo includes payroll rules for normal and sporadic cases.

Rules to discuss:

- Basic salary
- Net salary
- Housing allowance
- Transportation allowance
- Overtime
- Bonus
- Sales commission
- Retroactive adjustment
- Loan deduction
- Absence or late penalty

Demo steps:

1. Search for `OVERTIME`.
2. Search for `COMMISSION`.
3. Search for `LOAN`.
4. Explain how input amounts are pulled into payslips.

Expected result:

The audience sees how payroll calculation can stay standardized while handling exceptions.

### Scenario 7.3 - Other Input Types

Screen:

```text
Payroll > Configuration > Other Input Types
```

Story:

Sporadic pay and deductions enter payroll through controlled input types.

Input types:

- `OVERTIME`
- `BONUS`
- `COMMISSION`
- `LOAN`
- `ABSENCE`
- `RETRO`
- `TRANSPORT`
- `HOUSING`

Demo steps:

1. Open other input types.
2. Show codes and linked structures.
3. Explain that users do not type arbitrary labels into payslips.

Expected result:

Payroll exceptions remain auditable.

## Segment 8 - Payroll Execution

### Scenario 8.1 - Payroll Batches

Screen:

```text
Payroll Demo Enterprise > Operations Dashboard > Payroll Batches
```

Story:

Payroll is run in batches by period and workforce type.

Demo steps:

1. Open payroll batches from dashboard.
2. Show monthly payroll batches.
3. Show bi-weekly operations payroll.
4. Open a batch and review payslips.

Expected result:

The audience sees payroll at company and batch level.

### Scenario 8.2 - Monthly Payroll

Screen:

```text
Payroll > Batches
```

Story:

Office, HR, finance, sales and IT employees are paid monthly.

Demo steps:

1. Open a monthly batch.
2. Review slip count and period.
3. Open a payslip.
4. Show worked days, inputs, salary lines and net wage.

Expected result:

Monthly payroll can be reviewed and validated in one place.

### Scenario 8.3 - Bi-weekly Payroll

Screen:

```text
Payroll > Batches
```

Story:

Warehouse and operations workers have a different payroll cycle.

Demo steps:

1. Open `ALLNETWORKS Bi-weekly Operations Payroll`.
2. Show included employees.
3. Open a warehouse employee payslip.
4. Discuss attendance-driven pay and overtime.

Expected result:

The demo proves multiple payroll calendars are supported.

### Scenario 8.4 - Payslip Detail

Screen:

```text
Payroll > Payslips
```

Story:

Payroll officers inspect specific payslips before validation.

Demo steps:

1. Open a payslip from sales, warehouse or support.
2. Show employee, period, batch and structure.
3. Show worked days.
4. Show salary computation lines.
5. Show other inputs.
6. Show net wage.

Expected result:

Payslip calculation is transparent and auditable.

### Scenario 8.5 - Sporadic Commission

Screen:

```text
Payroll > Payslips
Payroll Demo Enterprise > Reports > Demo Scenarios
```

Story:

A sales employee receives an exceptional commission for a large deal.

Demo steps:

1. Search Demo Scenarios for `Sporadic` or `COMMISSION`.
2. Open the related employee.
3. Open that employee's current payslip.
4. Show `COMMISSION` input.
5. Show resulting net wage.

Expected result:

One-off commission is handled without changing base salary.

### Scenario 8.6 - Sporadic Bonus

Screen:

```text
Payroll > Payslips
```

Story:

A manager or high performer receives a one-time bonus.

Demo steps:

1. Search payslips with `BONUS` input.
2. Open payslip.
3. Show bonus input and salary rule result.
4. Explain approval/audit trail.

Expected result:

The bonus is visible in payroll and accounting.

### Scenario 8.7 - Sporadic Overtime

Screen:

```text
Attendances > Attendances
Payroll > Payslips
```

Story:

Emergency coverage or weekend installation causes overtime payout.

Demo steps:

1. Show long attendance records.
2. Open the related employee's payslip.
3. Show `OVERTIME` input.
4. Link the payroll input back to operational cause.

Expected result:

Overtime is justified by attendance data.

### Scenario 8.8 - Sporadic Allowance

Screen:

```text
Payroll > Payslips
```

Story:

A temporary transportation or field allowance is paid for a limited case.

Demo steps:

1. Open a payslip with allowance input.
2. Show `TRANSPORT` or allowance line.
3. Explain that the employee wage remains unchanged.

Expected result:

Temporary allowances do not require contract changes.

### Scenario 8.9 - Retroactive Adjustment

Screen:

```text
Payroll > Payslips
Accounting > Journal Entries
```

Story:

A salary change was approved late and must be corrected in the current period.

Demo steps:

1. Open a payslip with `RETRO` input.
2. Show the input amount.
3. Open accounting entry for retroactive adjustment.
4. Discuss audit review.

Expected result:

Retroactive corrections are visible and controlled.

### Scenario 8.10 - Loan or Advance Recovery

Screen:

```text
Payroll > Payslips
Accounting > Journal Entries
```

Story:

Employee loan installments or salary advances reduce net pay.

Demo steps:

1. Open a payslip with `LOAN` input.
2. Show deduction line.
3. Open accounting entry for loan recovery.
4. Explain liability clearing.

Expected result:

Employee receivables can be recovered through payroll.

### Scenario 8.11 - Absence or Late Penalty

Screen:

```text
Time Off > Time Off
Payroll > Payslips
```

Story:

Late attendance or unpaid absence creates a payroll deduction.

Demo steps:

1. Show attendance or unpaid leave case.
2. Open affected payslip.
3. Show `ABSENCE` input or deduction.
4. Explain manager review before validation.

Expected result:

Attendance policy becomes payroll action.

### Scenario 8.12 - Batch Payslip Generation

Screen:

```text
Payroll Demo Enterprise > Operations > Mass Operations
```

Story:

Payroll can generate payslips for many employees in one operation.

Demo steps:

1. Create a mass operation.
2. Select `Batch Payslip Generation`.
3. Select a department if you want a smaller run.
4. Execute.
5. Open the result and review the created batch.

Expected result:

The process avoids manual payslip creation.

### Scenario 8.13 - Batch Payslip Approval

Screen:

```text
Payroll Demo Enterprise > Operations > Mass Operations
```

Story:

Validated payslips can be approved in bulk after exceptions are resolved.

Demo steps:

1. Open or create `Batch Payslip Approval`.
2. Execute.
3. Review summary showing validated slips and remaining corrections.

Expected result:

Payroll close is faster and more controlled.

## Segment 9 - Expenses and Reimbursements

### Scenario 9.1 - Expense Inbox

Screen:

```text
Payroll Demo Enterprise > Operations > Employee Expenses
```

Story:

Employee expenses are related to HR and payroll because they affect employee payments and finance workload.

Demo steps:

1. Open employee expenses.
2. Group by status.
3. Show draft, submitted, approved and refused records.
4. Open an approved employee-paid expense.

Expected result:

Expenses are tracked separately from salary but visible in the employee financial workflow.

### Scenario 9.2 - Employee-Paid Reimbursement

Screen:

```text
Expenses > Expenses
Accounting > Journal Entries
```

Story:

An employee pays a business cost and needs reimbursement.

Demo steps:

1. Open an approved expense paid by employee.
2. Show employee, category and amount.
3. Open related accounting entry from `Payroll Demo Enterprise > Reports > Accounting Entries`.
4. Show debit to expense and credit to employee payable.

Expected result:

Expense reimbursement is accounted separately from payroll salary.

### Scenario 9.3 - Company-Paid Expense

Screen:

```text
Expenses > Expenses
```

Story:

Some costs are company-paid and should not reimburse the employee.

Demo steps:

1. Open a company-paid expense.
2. Show payment mode.
3. Explain how finance treats it differently from employee-paid expense.

Expected result:

Payment mode controls accounting behavior.

### Scenario 9.4 - Refused Expense

Screen:

```text
Expenses > Expenses
```

Story:

Not every submitted expense should be approved.

Demo steps:

1. Filter refused expenses.
2. Open the refused record.
3. Explain policy enforcement and audit trail.

Expected result:

Odoo supports control, not only data capture.

## Segment 10 - Banking and Salary Transfers

### Scenario 10.1 - Bank Transfer List

Screen:

```text
Payroll Demo Enterprise > Operations > Bank Transfers
```

Story:

Finance converts validated payroll into bank transfer batches.

Demo steps:

1. Open bank transfers.
2. Group by state.
3. Show generated, approved and reconciled transfers.
4. Open the latest transfer.

Expected result:

Payroll payment is a controlled workflow.

### Scenario 10.2 - Generate Transfer From Payroll Batch

Screen:

```text
Bank Transfers
```

Story:

The system builds payment lines from payslips.

Demo steps:

1. Open a draft/generated transfer.
2. Show selected payroll batch.
3. Show employee payment lines.
4. Show bank account, amount and status.
5. Show payment file preview.

Expected result:

Finance does not retype salary amounts.

### Scenario 10.3 - Missing Bank Account Control

Screen:

```text
Bank Transfers
Employees > Employees
```

Story:

If an employee lacks bank data, salary transfer should be blocked or flagged.

Demo steps:

1. Show transfer line statuses.
2. Discuss `missing_bank` status if available.
3. Open employee record to correct bank account.
4. Return to transfer.

Expected result:

HR master data quality protects payment operations.

### Scenario 10.4 - Approve and Send to Bank

Screen:

```text
Bank Transfers
```

Story:

Salary payment moves through generated, approved and sent states.

Demo steps:

1. Open a generated transfer.
2. Click approve if appropriate for demo.
3. Show state change.
4. Discuss send-to-bank step and payment file preview.

Expected result:

The audience sees a realistic payment approval workflow.

### Scenario 10.5 - Reconciled Salary Transfer

Screen:

```text
Bank Transfers
Payroll Demo Enterprise > Reports > Payroll Reconciliation
```

Story:

Finance marks salary payment as reconciled after matching the bank statement.

Demo steps:

1. Open reconciled bank transfer.
2. Show reconciliation note.
3. Open Payroll Reconciliation report.
4. Show matched transfer and any differences.

Expected result:

The payroll lifecycle ends with reconciliation, not payslip validation.

### Scenario 10.6 - Rejected Salary Payment

Screen:

```text
Payroll Demo Enterprise > Reports > Accounting Entries
```

Story:

One bank transfer can be rejected and must be reviewed.

Demo steps:

1. Open accounting entries.
2. Search for rejected salary payment.
3. Show payable remains open or bank clearing is reversed.
4. Explain finance reissue process.

Expected result:

Payment exceptions are visible in accounting.

## Segment 11 - Accounting Dashboard and Journals

### Scenario 11.1 - Accounting Dashboard Overview

Screen:

```text
Accounting > Dashboard
```

Story:

Accounting sees payroll and salary journals alongside normal finance journals.

Demo steps:

1. Open Accounting dashboard.
2. Show `Salaries` journal.
3. Show `ALLNETWORKS HR & Payroll Accounting`.
4. Show `ALLNETWORKS Salary Bank`.
5. Explain that payroll creates accounting entries and payment entries.

Expected result:

The Accounting dashboard is not empty for salaries.

### Scenario 11.2 - Native Salaries Journal

Screen:

```text
Accounting > Dashboard > Salaries
```

Story:

The native Odoo payroll accounting journal contains salary entries for dashboard visibility.

Demo steps:

1. Open the `Salaries` journal.
2. Show the 4 salary-related entries.
3. Show 3 posted entries and 1 draft adjustment.
4. Open one entry and review debit/credit balance.

Expected result:

Salaries are visible in the dashboard and balanced in accounting.

### Scenario 11.3 - HR and Payroll Accounting Entries

Screen:

```text
Payroll Demo Enterprise > Reports > Accounting Entries
```

Story:

The demo includes payroll, expense, leave, loan, retroactive and reconciliation journal entries.

Demo steps:

1. Open custom Accounting Entries report.
2. Show 15 HR/payroll/accounting entries.
3. Group by state.
4. Open a posted payroll accrual.
5. Open a draft payroll budget review.

Expected result:

The audience sees both operational and financial sides.

### Scenario 11.4 - Payroll Accrual Entry

Screen:

```text
Accounting > Accounting > Journal Entries
```

Story:

At month end, payroll expenses are accrued before bank payment.

Demo steps:

1. Search for monthly payroll accrual.
2. Open journal entry.
3. Show salary expense, bonus, overtime, allowances, employer cost and payroll payable lines.
4. Confirm debit equals credit.

Expected result:

Payroll cost is recognized in accounting.

### Scenario 11.5 - Salary Bank Payment Entry

Screen:

```text
Accounting > Dashboard > ALLNETWORKS Salary Bank
```

Story:

Salary bank payment clears payroll payable against bank.

Demo steps:

1. Open salary bank journal.
2. Open salary payment batch entry.
3. Show debit payroll payable and credit bank.
4. Link it back to bank transfer.

Expected result:

Finance sees how payroll payment affects bank accounting.

### Scenario 11.6 - Expense Reimbursement Entry

Screen:

```text
Payroll Demo Enterprise > Reports > Accounting Entries
```

Story:

Employee expense reimbursement posts expense and payable/bank lines.

Demo steps:

1. Search for employee expense reimbursement.
2. Open entry.
3. Show employee expense account and payable/bank clearing.

Expected result:

Expenses are integrated with accounting.

### Scenario 11.7 - Leave Accrual Liability

Screen:

```text
Accounting > Journal Entries
Time Off > Accrual Plans
```

Story:

Unused leave creates a cost/liability for management review.

Demo steps:

1. Open leave accrual liability entry.
2. Show leave expense and leave liability.
3. Open accrual plan to explain how leave balances arise.

Expected result:

Leave balances become financial exposure.

### Scenario 11.8 - Loan Recovery Entry

Screen:

```text
Accounting > Journal Entries
Payroll > Payslips
```

Story:

Payroll deduction clears employee loan or advance.

Demo steps:

1. Open loan recovery accounting entry.
2. Show payable and employee loan account.
3. Open related payslip with `LOAN` input.

Expected result:

Payroll and accounting agree on employee recoveries.

### Scenario 11.9 - Retroactive Adjustment Entry

Screen:

```text
Accounting > Journal Entries
```

Story:

A late salary correction is accrued and reviewed.

Demo steps:

1. Open retroactive adjustment entry.
2. Show retro expense and payroll payable.
3. Discuss approval controls.

Expected result:

Corrections are visible and auditable.

### Scenario 11.10 - Draft Payroll Budget Review

Screen:

```text
Accounting > Journal Entries
```

Story:

Finance can review a draft payroll cost before posting.

Demo steps:

1. Filter draft journal entries.
2. Open payroll budget review.
3. Explain draft state and posting control.

Expected result:

Accounting can review before financial impact is final.

### Scenario 11.11 - Chart of Accounts

Screen:

```text
Accounting > Configuration > Chart of Accounts
```

Story:

The demo includes payroll expense, employer cost, payable, bank, leave liability and loan accounts.

Demo steps:

1. Search `Payroll`.
2. Search `Salary`.
3. Search `Leave`.
4. Open one expense and one liability account.

Expected result:

The financial structure behind the demo is visible.

### Scenario 11.12 - Journal Items

Screen:

```text
Accounting > Accounting > Journal Items
```

Story:

Accountants can analyze payroll cost line by line.

Demo steps:

1. Filter by salary expense or payroll payable account.
2. Group by account.
3. Group by journal.
4. Export or pivot if needed.

Expected result:

Payroll is available for detailed financial analysis.

## Segment 12 - Reports and Management Review

### Scenario 12.1 - Demo Scenario Catalog

Screen:

```text
Payroll Demo Enterprise > Reports > Demo Scenarios
```

Story:

The scenario catalog lets the presenter jump to specific business cases.

Demo steps:

1. Open Demo Scenarios.
2. Group by scenario type.
3. Show payroll, leave, attendance, accounting and reporting scenarios.
4. Open one scenario and read speaker note.

Expected result:

The demo can be adapted live to audience questions.

### Scenario 12.2 - Department Payroll Summary

Screen:

```text
Payroll Demo Enterprise > Reports > Department Payroll Summary
```

Story:

Managers compare payroll cost, overtime, attendance issues and leave by department.

Demo steps:

1. Open department summary.
2. Switch list, pivot and graph if available.
3. Compare Sales, Warehouse, Support and Operations.
4. Discuss why cost differs across departments.

Expected result:

Management sees payroll as a cost-control process.

### Scenario 12.3 - Payroll Reconciliation Report

Screen:

```text
Payroll Demo Enterprise > Reports > Payroll Reconciliation
```

Story:

Payroll, bank transfer and accounting must reconcile.

Demo steps:

1. Open reconciliation records.
2. Show matched case.
3. Show exception or difference case.
4. Explain review notes.

Expected result:

The audience sees how errors are detected after payment.

### Scenario 12.4 - Accounting Reporting

Screen:

```text
Accounting > Reporting
```

Story:

Payroll entries affect standard accounting reports.

Demo steps:

1. Open general ledger or trial balance.
2. Filter salary expense or payroll payable accounts.
3. Show posted entries.
4. Compare draft entries if appropriate.

Expected result:

Payroll accounting is part of normal finance reporting.

### Scenario 12.5 - Pivot Analysis

Screen:

```text
Payroll > Payslips
Accounting > Journal Items
```

Story:

Executives want payroll totals by department, category or account.

Demo steps:

1. Use payslip list/pivot if available.
2. Group by department or batch.
3. Use journal item pivot for account-level totals.

Expected result:

Odoo supports analysis without exporting to spreadsheets.

## Segment 13 - Mass Operations and Productivity

### Scenario 13.1 - Mass Employee Update

Screen:

```text
Payroll Demo Enterprise > Operations > Mass Operations
```

Story:

HR sometimes needs to apply a maintenance change to many employee records.

Demo steps:

1. Open Mass Operations.
2. Select `Mass Employee Update`.
3. Pick a department if you want to limit the action.
4. Execute.
5. Show affected employee count.

Expected result:

The system can support bulk HR maintenance.

### Scenario 13.2 - Batch Attendance Adjustment

Screen:

```text
Mass Operations
```

Story:

Attendance exceptions are reviewed in bulk.

Demo steps:

1. Select `Batch Attendance Adjustment`.
2. Execute.
3. Show reviewed attendance alerts and adjusted missing check-outs.

Expected result:

Payroll readiness improves without opening every attendance record.

### Scenario 13.3 - Bulk Leave Approval

Screen:

```text
Mass Operations
```

Story:

Leave approvals can be processed before payroll cutoff.

Demo steps:

1. Select `Bulk Leave Approval`.
2. Execute.
3. Open time off list and show status updates.

Expected result:

Approval bottlenecks are reduced.

### Scenario 13.4 - Batch Payslip Generation

Screen:

```text
Mass Operations
```

Story:

Payroll can generate payslips for all employees or one department.

Demo steps:

1. Select `Batch Payslip Generation`.
2. Choose date range.
3. Optional: choose department.
4. Execute.

Expected result:

Odoo replaces repetitive payslip creation.

### Scenario 13.5 - Batch Payslip Approval

Screen:

```text
Mass Operations
```

Story:

Payroll validates many payslips after review.

Demo steps:

1. Select `Batch Payslip Approval`.
2. Execute.
3. Show validated count and remaining corrections.

Expected result:

Payroll close is controlled and fast.

### Scenario 13.6 - Create Bank Transfer

Screen:

```text
Mass Operations
```

Story:

Finance can create bank transfer batches from payroll in one operation.

Demo steps:

1. Select `Create Bank Transfer`.
2. Execute.
3. Open created bank transfer.
4. Show payment lines and file preview.

Expected result:

Payroll-to-bank handoff is automated.

## Extended Use Case Catalog

Use these cases when presentation time is extended or the audience asks for more depth.

### Employee and HR Cases

1. New hire created before payroll cutoff.
2. New hire created mid-month with prorated payroll.
3. Employee assigned to department and manager.
4. Employee transferred from Support to Sales.
5. Employee promoted with salary increment.
6. Employee changed from temporary to full-time.
7. Employee changed from monthly to bi-weekly schedule.
8. Fixed-term employee renewed before contract end.
9. Seasonal employee prepared for final payoff.
10. Intern assigned to part-time schedule.
11. Remote IT employee assigned hybrid location.
12. Field employee assigned flexible schedule.
13. Employee missing bank account flagged during bank transfer.
14. Employee category used for payroll treatment.
15. Manager opens department team and reviews employees.
16. HR reviews employee certifications before assigning field work.
17. HR reviews training attendance for compliance.
18. HR reviews refused or failed training attendance.
19. HR compares employee resume/skills with job needs.
20. HR uses scenario catalog to open employee-specific cases.

### Attendance and Work Entry Cases

21. Standard office attendance for monthly employee.
22. Support morning shift attendance.
23. Support evening shift attendance.
24. Warehouse day shift attendance.
25. Warehouse night shift attendance.
26. Field operations flexible attendance.
27. Remote IT attendance pattern.
28. Missing check-out detected.
29. Missing check-out corrected in mass operation.
30. Long day creates overtime review.
31. Weekend work creates overtime scenario.
32. Late check-in creates deduction scenario.
33. Attendance exception reviewed before payroll.
34. Attendance records grouped by employee.
35. Attendance records grouped by department.
36. Work entries reviewed before payslip calculation.
37. Paid leave generates paid work entries.
38. Unpaid leave generates deduction impact.
39. Attendance and leave conflict discussed before validation.
40. Payroll cutoff blocked until attendance exceptions are reviewed.

### Time Off Cases

41. Annual leave approved and paid.
42. Sick leave reviewed by HR.
43. Casual leave approved by manager.
44. Emergency leave requires HR review.
45. Unpaid leave reduces salary.
46. Leave request refused because of inventory count or coverage need.
47. Pending leave before payroll cutoff.
48. Bulk leave approval by mass operation.
49. Annual leave accrual plan reviewed.
50. Sick leave accrual plan reviewed.
51. Hourly worked-time accrual plan reviewed.
52. Probation slow-start accrual reviewed.
53. Intern fixed-term accrual reviewed.
54. Leave liability posted to accounting.
55. Department leave load reviewed before payroll.

### Payroll Cases

56. Monthly payroll batch generated.
57. Bi-weekly operations payroll generated.
58. Payslip computed for office employee.
59. Payslip computed for warehouse employee.
60. Payslip computed for sales commission employee.
61. Housing allowance input applied.
62. Transportation allowance input applied.
63. Overtime input applied.
64. Bonus input applied.
65. Sales commission input applied.
66. Retroactive adjustment input applied.
67. Loan deduction input applied.
68. Absence penalty input applied.
69. Payroll correction after validation.
70. Draft payslip reviewed before approval.
71. Batch payslip approval validates clean payslips.
72. Error payslips remain for correction review.
73. Final payoff scenario reviewed.
74. Payroll batch opened from dashboard.
75. Payroll net total reviewed by executive.

### Expense Cases

76. Employee-paid meal expense submitted.
77. Employee-paid travel expense approved.
78. Mileage expense reviewed.
79. Communication expense approved.
80. Company-paid expense separated from reimbursement.
81. Refused expense reviewed.
82. Submitted expenses grouped by status.
83. Expense reimbursement accounting entry posted.
84. Expense payable cleared by bank.
85. Expense policy discussed with audit trail.

### Banking Cases

86. Bank transfer generated from payroll batch.
87. Employee payment lines reviewed.
88. Payment file preview exported conceptually.
89. Transfer approved by finance.
90. Transfer sent to bank.
91. Transfer marked reconciled.
92. Rejected salary payment reviewed.
93. Missing bank account blocks send-to-bank.
94. Salary payment linked to accounting move.
95. Bank transfer totals compared with payroll net total.

### Accounting Cases

96. Accounting dashboard shows Salaries journal.
97. Native `Salaries` journal contains payroll entries.
98. Custom HR payroll accounting journal contains detailed entries.
99. Salary bank journal contains payment entries.
100. Payroll accrual posted.
101. Salary payment posted.
102. Rejected payment accounting reviewed.
103. Employee expense reimbursement posted.
104. Company-paid expense entry reviewed.
105. Leave accrual liability posted.
106. Loan recovery posted.
107. Retroactive payroll adjustment posted.
108. Payroll reconciliation difference reviewed.
109. Draft payroll budget review opened.
110. Chart of accounts shows payroll accounts.
111. Journal items grouped by account.
112. Trial balance or general ledger includes payroll accounts.
113. Debit and credit balance verified.
114. Posted versus draft accounting entries explained.
115. Finance uses accounting entries to close payroll month.

### Reporting and Audit Cases

116. Operations dashboard KPIs reviewed.
117. Demo scenarios grouped by type.
118. Department payroll summary reviewed.
119. Payroll reconciliation report reviewed.
120. Attendance alerts converted into payroll readiness action.
121. Leave approvals converted into payroll readiness action.
122. Training compliance reviewed by department.
123. Expense statuses reviewed before payment.
124. Payroll batches reviewed by period.
125. Journal entries reviewed by state.
126. Salary bank payments reviewed by reconciliation status.
127. Executive asks for department cost explanation.
128. Payroll officer explains net pay variance.
129. Accountant explains payable clearing.
130. HR explains employee data quality impact.

## Recommended Live Story Flow

Use this flow if you need one continuous presentation without jumping randomly:

1. Start at `Operations Dashboard`.
2. Open employees and explain company population.
3. Open departments and job positions.
4. Open contract templates and compare monthly, bi-weekly, sales, intern and seasonal templates.
5. Open one sales employee, one warehouse employee, one support employee and one finance employee.
6. Open training sessions and training attendance.
7. Open attendance alerts and native attendance list.
8. Run or show `Batch Attendance Adjustment`.
9. Open Time Off and Accrual Plans.
10. Open Work Entries.
11. Open Payroll Batches.
12. Open payslips for sales commission, warehouse overtime, unpaid leave and loan deduction cases.
13. Open Mass Operations for payroll generation and approval.
14. Open Employee Expenses and explain reimbursement cases.
15. Open Bank Transfers and show payment file preview.
16. Open Payroll Reconciliation.
17. Open Accounting Dashboard.
18. Open `Salaries`, `ALLNETWORKS HR & Payroll Accounting` and `ALLNETWORKS Salary Bank`.
19. Open Chart of Accounts and Journal Items.
20. Finish with Department Payroll Summary and Demo Scenarios.

## Speaker Notes by Audience

### For HR Directors

Emphasize:

- employee master data
- contracts and templates
- approvals
- training and certifications
- leave policy and accruals
- mass operations
- audit trail

Key message:

"HR owns the data that makes payroll and finance accurate."

### For Payroll Managers

Emphasize:

- attendance readiness
- work entries
- payroll batches
- payslip inputs
- exceptions
- batch validation
- salary transfer handoff

Key message:

"Payroll is controlled by structured inputs and batch workflows, not spreadsheets."

### For Finance and Accounting

Emphasize:

- payroll accruals
- salary payment clearing
- expense reimbursements
- salary bank journal
- payroll payable
- leave liabilities
- reconciliation exceptions

Key message:

"Payroll becomes accounting data automatically and can be reconciled."

### For Executives

Emphasize:

- dashboards
- department payroll cost
- attendance and leave risk
- bank transfer status
- accounting visibility
- management reporting

Key message:

"Management sees the full payroll operation from people to payment to accounting."

## Closing Script

Say:

"The value of this workflow is not only that Odoo can create payslips. The value is that the whole company process is connected. HR data feeds attendance, leave and contracts. Attendance and leave feed work entries. Work entries and inputs feed payslips. Payslips feed bank transfers. Bank transfers and payroll accruals feed accounting. Accounting and reconciliation close the month. The demo company shows the same process across monthly staff, bi-weekly workers, commissions, overtime, bonuses, deductions, expenses, training and compliance."

Then open:

```text
Payroll Demo Enterprise > Reports > Department Payroll Summary
```

Finish with:

"This is where the executive discussion begins: which departments are costing more, why overtime happened, whether leave balances are controlled, and whether payroll payments were fully reconciled."
