# HR Payroll Demo Enterprise

Production-grade Odoo 19 demo module for HR, Attendance, Payroll, Banking Integration Flow, Mass Operations and Reporting.

## What It Creates

- Company: `ALLNETWORKS Caribbean Holdings Ltd`
- 9 departments: Executive and Administration, HR, Finance and Accounting, Sales, Customer Support, Operations, Warehouse and Logistics, IT and Systems, Temporary and Interns
- 100 realistic employees with manager/supervisor hierarchy, employee categories, positions, contract types and work schedules
- Contract/wage setup, salary structures and payroll inputs
- 3 months of attendance records with late check-ins, overtime, weekend work and missing check-outs
- Leave allocations and requests across annual, sick, casual, unpaid and emergency leave
- Monthly and bi-weekly payroll batches
- Payslips with overtime, bonus, commission, loan, absence and retroactive adjustment inputs
- Bank transfer batches and reconciliation examples
- HR and Payroll operations dashboard
- Mass operation tools
- 40-scenario catalog and reporting records covering HR, payroll, accounting, banking, payoff and reconciliation

## Dependencies

This module uses the real Odoo 19 Enterprise payroll stack:

- `hr_payroll_account`
- `hr_payroll_attendance`
- `hr_holidays_attendance`
- `hr_attendance`
- `hr_holidays`
- `account`

## Installation

Add this folder to `addons_path`, update apps, then install:

```bash
hr_payroll_demo_enterprise
```

The module post-init hook seeds the complete dataset automatically.

## Main Menu

Open:

```text
Payroll Demo Enterprise
```

Key entries:

- Operations Dashboard
- Bank Transfers
- Mass Operations
- Demo Scenarios
- Department Payroll Summary
- Payroll Reconciliation

## Demo Message

The demo is designed to prove:

> Odoo can handle medium-size payroll operations efficiently, with dashboards, mass actions, payroll batches, banking handoff and reconciliation in a realistic operational company.

## Important Notes

- This is a demo module. Do not install it in a production customer database.
- Data is generated with stable external IDs through the post-init hook.
- The generated dataset is intentionally interconnected for presentation value.
