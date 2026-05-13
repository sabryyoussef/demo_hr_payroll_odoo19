from dateutil.relativedelta import relativedelta

from odoo import _, fields, models


class HrPayrollDemoMassOperation(models.Model):
    _name = "hr.payroll.demo.mass.operation"
    _description = "HR Payroll Demo Mass Operation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    operation_type = fields.Selection(
        [
            ("employee_update", "Mass Employee Update"),
            ("generate_payslips", "Batch Payslip Generation"),
            ("approve_payslips", "Batch Payslip Approval"),
            ("attendance_adjustment", "Batch Attendance Adjustment"),
            ("approve_leaves", "Bulk Leave Approval"),
            ("create_bank_transfer", "Create Bank Transfer"),
        ],
        required=True,
        default="generate_payslips",
        tracking=True,
    )
    department_id = fields.Many2one("hr.department")
    date_from = fields.Date(default=lambda self: fields.Date.context_today(self).replace(day=1))
    date_to = fields.Date(default=lambda self: fields.Date.context_today(self) + relativedelta(day=31))
    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done"), ("failed", "Failed")],
        default="draft",
        tracking=True,
    )
    affected_employee_count = fields.Integer(readonly=True)
    result_summary = fields.Text(readonly=True)

    def _employee_domain(self):
        domain = [("company_id", "=", self.company_id.id), ("active", "=", True)]
        if self.department_id:
            domain.append(("department_id", "=", self.department_id.id))
        return domain

    def action_execute(self):
        for operation in self:
            try:
                method = getattr(operation, "_execute_%s" % operation.operation_type)
                method()
                operation.state = "done"
            except Exception as exc:
                operation.state = "failed"
                operation.result_summary = str(exc)
                raise

    def _execute_employee_update(self):
        employees = self.env["hr.employee"].search(self._employee_domain())
        employees.write({"employee_properties": {}})
        self.affected_employee_count = len(employees)
        self.result_summary = _("Updated %s employee records for demo mass maintenance.") % len(employees)

    def _execute_generate_payslips(self):
        employees = self.env["hr.employee"].search(self._employee_domain())
        batch = self.env["hr.payslip.run"].create(
            {
                "name": _("Mass Payroll %s to %s") % (self.date_from, self.date_to),
                "date_start": self.date_from,
                "date_end": self.date_to,
                "company_id": self.company_id.id,
            }
        )
        slips = self.env["hr.payslip"].create(
            [
                {
                    "name": _("Payslip - %s - %s") % (employee.name, self.date_from),
                    "employee_id": employee.id,
                    "date_from": self.date_from,
                    "date_to": self.date_to,
                    "payslip_run_id": batch.id,
                    "company_id": self.company_id.id,
                }
                for employee in employees
            ]
        )
        slips.compute_sheet()
        self.affected_employee_count = len(employees)
        self.result_summary = _("Generated %s payslips in batch %s.") % (len(slips), batch.name)

    def _execute_approve_payslips(self):
        domain = [("company_id", "=", self.company_id.id), ("state", "=", "draft")]
        if self.date_from:
            domain.append(("date_from", ">=", self.date_from))
        if self.date_to:
            domain.append(("date_to", "<=", self.date_to))
        payslips = self.env["hr.payslip"].search(domain)
        payslips.compute_sheet()
        valid_payslips = payslips.filtered(lambda slip: not slip.error_count)
        valid_payslips.action_validate()
        self.affected_employee_count = len(payslips.mapped("employee_id"))
        self.result_summary = _("Validated %s payslips; %s remain for correction review.") % (len(valid_payslips), len(payslips - valid_payslips))

    def _execute_attendance_adjustment(self):
        attendances = self.env["hr.attendance"].search(
            [
                ("employee_id.company_id", "=", self.company_id.id),
                "|",
                ("check_out", "=", False),
                ("worked_hours", ">", 10),
            ]
        )
        adjusted = 0
        for attendance in attendances.filtered(lambda att: not att.check_out):
            attendance.check_out = attendance.check_in + relativedelta(hours=8)
            adjusted += 1
        self.affected_employee_count = len(attendances.mapped("employee_id"))
        self.result_summary = _("Reviewed %s attendance alerts and adjusted %s missing check-outs.") % (len(attendances), adjusted)

    def _execute_approve_leaves(self):
        leaves = self.env["hr.leave"].search(
            [
                ("company_id", "=", self.company_id.id),
                ("state", "in", ["confirm", "validate1"]),
            ]
        )
        for leave in leaves:
            if hasattr(leave, "action_approve") and leave.state == "confirm":
                leave.action_approve()
            if hasattr(leave, "action_validate") and leave.state in ("confirm", "validate1"):
                leave.action_validate()
        self.affected_employee_count = len(leaves.mapped("employee_id"))
        self.result_summary = _("Approved %s pending leave requests.") % len(leaves)

    def _execute_create_bank_transfer(self):
        batch = self.env["hr.payslip.run"].search([("company_id", "=", self.company_id.id)], limit=1, order="date_end desc")
        transfer = self.env["hr.payroll.demo.bank.transfer"].create(
            {
                "name": _("Mass Operation Bank Transfer"),
                "company_id": self.company_id.id,
                "batch_id": batch.id,
            }
        )
        transfer.action_generate_from_batch()
        self.affected_employee_count = len(transfer.line_ids.mapped("employee_id"))
        self.result_summary = _("Created bank transfer %s with %s payment lines.") % (transfer.name, len(transfer.line_ids))

    def action_open_result(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
        }
