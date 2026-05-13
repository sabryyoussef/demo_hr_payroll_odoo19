# Technical Architecture

## Module Design

The module uses the native Odoo 19 Enterprise payroll models for core payroll:

- `hr.employee`
- `hr.department`
- `hr.attendance`
- `hr.leave`
- `hr.payslip`
- `hr.payslip.run`
- `hr.payroll.structure`
- `hr.payslip.input.type`

Custom models are only added for demo usability:

- `hr.payroll.demo.dashboard`
- `hr.payroll.demo.mass.operation`
- `hr.payroll.demo.bank.transfer`
- `hr.payroll.demo.bank.transfer.line`
- `hr.payroll.demo.scenario`
- `hr.payroll.demo.department.summary`
- `hr.payroll.demo.reconciliation`

## Data Strategy

The dataset is generated in `post_init_hook` because the demo volume is large and interconnected.

Each generated record receives an external ID in `ir.model.data`, so demo records are traceable.

## Performance Choices

- Batch record creation is used where possible.
- Payslip generation uses native `compute_sheet()`.
- Dashboard KPIs use `search_count()` and targeted domains.
- Mass operations use department/date filters.

## Security

Two groups are created:

- Payroll Demo User
- Payroll Demo Manager

Multi-company record rules are defined for demo bank transfers and mass operations.

## Extension Points

Common extension points:

- Add payroll localizations.
- Replace payment file preview with real bank export format.
- Add real account move creation per payroll transfer.
- Add spreadsheet or OWL dashboard for richer visuals.
