# Functional Workflow Guide

## Story 1 - Department Payroll Overview

Open `Payroll Demo Enterprise > Operations Dashboard`.

Explain:

- employee count
- department count
- open leaves
- attendance alerts
- payroll totals
- pending bank transfers

## Story 2 - Attendance Exception Review

Click `Attendance Alerts`.

Show:

- missing check-outs
- overtime records
- late check-ins
- manual adjustment potential

Then open `Mass Operations` and run `Batch Attendance Adjustment`.

## Story 3 - Bulk Leave Approval

Open `Mass Operations`.

Create:

- Operation Type: `Bulk Leave Approval`
- Execute

Explain that managers can process multiple pending approvals without opening every leave request.

## Story 4 - Payroll Generation

Open Dashboard and click `Generate Payroll`, or create a mass operation:

- Operation Type: `Batch Payslip Generation`
- Select date range
- Select department if needed
- Execute

Explain the batch creation and department filtering.

## Story 5 - Payslip Validation

Open Mass Operations:

- Operation Type: `Batch Payslip Approval`
- Execute

Explain batch approval and reduced clicking.

## Story 6 - Bank Transfer

Open:

```text
Payroll Demo Enterprise > Operations > Bank Transfers
```

Show:

- payment lines
- employee bank accounts
- payment file preview
- approve
- send to bank
- reconcile

## Story 7 - Reconciliation

Open:

```text
Payroll Demo Enterprise > Reports > Payroll Reconciliation
```

Show:

- matched payroll transfer
- exception case with difference
- management review note

## Story 8 - Department Reporting

Open:

```text
Payroll Demo Enterprise > Reports > Department Payroll Summary
```

Use list/pivot/graph to show:

- monthly gross
- monthly net
- overtime hours
- attendance violations
- pending leave
- bank transfer amount
