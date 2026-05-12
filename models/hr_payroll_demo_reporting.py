from odoo import fields, models


class HrPayrollDemoScenario(models.Model):
    _name = "hr.payroll.demo.scenario"
    _description = "HR Payroll Demo Scenario"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    scenario_type = fields.Selection(
        [
            ("payroll", "Payroll"),
            ("attendance", "Attendance"),
            ("leave", "Leave"),
            ("banking", "Banking"),
            ("accounting", "Accounting"),
            ("mass", "Mass Operation"),
            ("reporting", "Reporting"),
        ],
        required=True,
    )
    employee_id = fields.Many2one("hr.employee")
    department_id = fields.Many2one("hr.department")
    description = fields.Text(required=True)
    speaker_note = fields.Text()
    status = fields.Selection(
        [("ready", "Ready"), ("needs_review", "Needs Review"), ("optional", "Optional")],
        default="ready",
        required=True,
    )


class HrPayrollDemoDepartmentSummary(models.Model):
    _name = "hr.payroll.demo.department.summary"
    _description = "HR Payroll Demo Department Summary"
    _order = "department_id"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    department_id = fields.Many2one("hr.department", required=True)
    employee_count = fields.Integer()
    monthly_gross = fields.Monetary(currency_field="currency_id")
    monthly_net = fields.Monetary(currency_field="currency_id")
    overtime_hours = fields.Float()
    attendance_violation_count = fields.Integer()
    pending_leave_count = fields.Integer()
    bank_transfer_amount = fields.Monetary(currency_field="currency_id")
    payroll_risk_note = fields.Char()


class HrPayrollDemoPayrollReconciliation(models.Model):
    _name = "hr.payroll.demo.reconciliation"
    _description = "HR Payroll Demo Reconciliation Example"
    _order = "date desc, id desc"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    date = fields.Date(default=fields.Date.context_today)
    payslip_run_id = fields.Many2one("hr.payslip.run")
    bank_transfer_id = fields.Many2one("hr.payroll.demo.bank.transfer")
    payroll_total = fields.Monetary(currency_field="currency_id")
    bank_statement_total = fields.Monetary(currency_field="currency_id")
    difference = fields.Monetary(currency_field="currency_id")
    state = fields.Selection(
        [
            ("open", "Open"),
            ("matched", "Matched"),
            ("exception", "Exception"),
            ("closed", "Closed"),
        ],
        default="open",
    )
    note = fields.Text()
