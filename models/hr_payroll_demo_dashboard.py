from dateutil.relativedelta import relativedelta

from odoo import _, fields, models


class HrPayrollDemoDashboard(models.Model):
    _name = "hr.payroll.demo.dashboard"
    _description = "HR Payroll Demo Dashboard"

    name = fields.Char(default="ALLNETWORKS Payroll Operations Dashboard", required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    employee_count = fields.Integer(compute="_compute_kpis")
    department_count = fields.Integer(compute="_compute_kpis")
    open_leave_count = fields.Integer(compute="_compute_kpis")
    attendance_alert_count = fields.Integer(compute="_compute_kpis")
    payroll_batch_count = fields.Integer(compute="_compute_kpis")
    draft_payslip_count = fields.Integer(compute="_compute_kpis")
    pending_bank_transfer_count = fields.Integer(compute="_compute_kpis")
    monthly_net_total = fields.Monetary(compute="_compute_kpis", currency_field="currency_id")
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    last_refresh = fields.Datetime(default=fields.Datetime.now)

    def _compute_kpis(self):
        Employee = self.env["hr.employee"].sudo()
        Department = self.env["hr.department"].sudo()
        Leave = self.env["hr.leave"].sudo()
        Attendance = self.env["hr.attendance"].sudo()
        PayslipRun = self.env["hr.payslip.run"].sudo()
        Payslip = self.env["hr.payslip"].sudo()
        Transfer = self.env["hr.payroll.demo.bank.transfer"].sudo()
        today = fields.Date.context_today(self)
        month_start = today.replace(day=1)
        month_end = month_start + relativedelta(months=1, days=-1)
        for dashboard in self:
            company_domain = [("company_id", "=", dashboard.company_id.id)]
            employee_company_domain = [("employee_id.company_id", "=", dashboard.company_id.id)]
            dashboard.employee_count = Employee.search_count(company_domain + [("active", "=", True)])
            dashboard.department_count = Department.search_count(company_domain)
            dashboard.open_leave_count = Leave.search_count(employee_company_domain + [("state", "in", ["confirm", "validate1"])])
            dashboard.attendance_alert_count = Attendance.search_count(
                employee_company_domain + ["|", ("check_out", "=", False), ("worked_hours", ">", 10)]
            )
            dashboard.payroll_batch_count = PayslipRun.search_count(
                company_domain + [("date_start", ">=", month_start), ("date_end", "<=", month_end)]
            )
            dashboard.draft_payslip_count = Payslip.search_count(company_domain + [("state", "=", "draft")])
            dashboard.pending_bank_transfer_count = Transfer.search_count(
                company_domain + [("state", "in", ["draft", "generated", "approved", "sent"])]
            )
            payslips = Payslip.search(company_domain + [("date_from", ">=", month_start), ("date_to", "<=", month_end)])
            dashboard.monthly_net_total = sum(payslips.mapped("net_wage"))

    def action_refresh_kpis(self):
        self.write({"last_refresh": fields.Datetime.now()})

    def action_open_employees(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("ALLNETWORKS Employees"),
            "res_model": "hr.employee",
            "view_mode": "list,kanban,form",
            "views": [(False, "list"), (False, "kanban"), (False, "form")],
            "domain": [("company_id", "=", self.company_id.id)],
            "context": {
                "allowed_company_ids": [self.company_id.id],
                "default_company_id": self.company_id.id,
            },
            "target": "current",
        }

    def action_open_payroll_batches(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Payroll Batches"),
            "res_model": "hr.payslip.run",
            "view_mode": "list,form",
            "views": [(False, "list"), (False, "form")],
            "domain": [("company_id", "=", self.company_id.id)],
            "context": {
                "allowed_company_ids": [self.company_id.id],
                "default_company_id": self.company_id.id,
            },
            "target": "current",
        }

    def action_open_attendance_alerts(self):
        action = self.env.ref("hr_attendance.hr_attendance_action").read()[0]
        action["domain"] = [
            ("employee_id.company_id", "=", self.company_id.id),
            "|",
            ("check_out", "=", False),
            ("worked_hours", ">", 10),
        ]
        return action

    def action_open_bank_transfers(self):
        return self.env.ref("hr_payroll_demo_enterprise.action_hr_payroll_demo_bank_transfer").read()[0]

    def action_generate_payroll(self):
        operation = self.env["hr.payroll.demo.mass.operation"].create(
            {
                "name": _("Quick Payroll Generation"),
                "operation_type": "generate_payslips",
                "date_from": fields.Date.context_today(self).replace(day=1),
                "date_to": fields.Date.context_today(self),
                "company_id": self.env.company.id,
            }
        )
        operation.action_execute()
        return operation.action_open_result()

    def action_validate_attendance(self):
        operation = self.env["hr.payroll.demo.mass.operation"].create(
            {
                "name": _("Quick Attendance Validation"),
                "operation_type": "attendance_adjustment",
                "company_id": self.env.company.id,
            }
        )
        operation.action_execute()
        return operation.action_open_result()

    def action_approve_leaves(self):
        operation = self.env["hr.payroll.demo.mass.operation"].create(
            {
                "name": _("Quick Bulk Leave Approval"),
                "operation_type": "approve_leaves",
                "company_id": self.env.company.id,
            }
        )
        operation.action_execute()
        return operation.action_open_result()

    def action_create_bank_transfer(self):
        batch = self.env["hr.payslip.run"].search([("company_id", "=", self.env.company.id)], limit=1, order="date_end desc")
        transfer = self.env["hr.payroll.demo.bank.transfer"].create(
            {
                "name": _("Demo Salary Transfer - %s") % (batch.name if batch else fields.Date.today()),
                "batch_id": batch.id,
                "company_id": self.env.company.id,
            }
        )
        if batch:
            transfer.action_generate_from_batch()
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.payroll.demo.bank.transfer",
            "view_mode": "form",
            "res_id": transfer.id,
        }
