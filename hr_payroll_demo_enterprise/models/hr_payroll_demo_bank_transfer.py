from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrPayrollDemoBankTransfer(models.Model):
    _name = "hr.payroll.demo.bank.transfer"
    _description = "Demo Payroll Bank Transfer"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "payment_date desc, id desc"

    name = fields.Char(required=True, default=lambda self: _("New Bank Transfer"))
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    batch_id = fields.Many2one("hr.payslip.run", string="Payroll Batch", tracking=True)
    payment_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    bank_journal_id = fields.Many2one(
        "account.journal",
        domain="[('type', '=', 'bank'), ('company_id', '=', company_id)]",
        string="Payment Bank Journal",
        tracking=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("generated", "Generated"),
            ("approved", "Approved"),
            ("sent", "Sent to Bank"),
            ("reconciled", "Reconciled"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
        required=True,
    )
    line_ids = fields.One2many("hr.payroll.demo.bank.transfer.line", "transfer_id", copy=True)
    line_count = fields.Integer(compute="_compute_totals", store=True)
    total_amount = fields.Monetary(compute="_compute_totals", currency_field="currency_id", store=True)
    payment_file_preview = fields.Text(readonly=True)
    account_move_id = fields.Many2one("account.move", readonly=True)
    reconciliation_note = fields.Text()

    @api.depends("line_ids.amount")
    def _compute_totals(self):
        for transfer in self:
            transfer.line_count = len(transfer.line_ids)
            transfer.total_amount = sum(transfer.line_ids.mapped("amount"))

    def action_generate_from_batch(self):
        for transfer in self:
            if not transfer.batch_id:
                raise UserError(_("Select a payroll batch first."))
            transfer.line_ids.unlink()
            lines = []
            slips = transfer.batch_id.slip_ids.filtered(lambda slip: slip.state != "cancel")
            for slip in slips:
                amount = slip.net_wage or slip.basic_wage or 0.0
                if amount <= 0:
                    amount = slip.employee_id.contract_wage or slip.employee_id.wage or 0.0
                bank_account = slip.employee_id.primary_bank_account_id
                lines.append(
                    (
                        0,
                        0,
                        {
                            "employee_id": slip.employee_id.id,
                            "payslip_id": slip.id,
                            "bank_account_id": bank_account.id,
                            "amount": amount,
                            "status": "ready" if bank_account else "missing_bank",
                        },
                    )
                )
            transfer.write({"line_ids": lines, "state": "generated"})
            transfer._generate_payment_file_preview()

    def _generate_payment_file_preview(self):
        for transfer in self:
            rows = ["Employee,Account,Amount,Status"]
            for line in transfer.line_ids:
                rows.append(
                    "%s,%s,%.2f,%s"
                    % (
                        line.employee_id.name,
                        line.bank_account_id.acc_number or "MISSING",
                        line.amount,
                        line.status,
                    )
                )
            transfer.payment_file_preview = "\n".join(rows)

    def action_approve(self):
        self.write({"state": "approved"})

    def action_send_to_bank(self):
        for transfer in self:
            if any(line.status == "missing_bank" for line in transfer.line_ids):
                raise UserError(_("Some employees are missing bank accounts. Resolve them before sending."))
            transfer.write({"state": "sent"})

    def action_mark_reconciled(self):
        for transfer in self:
            transfer.write(
                {
                    "state": "reconciled",
                    "reconciliation_note": _("Demo reconciliation completed against the salary payment bank statement."),
                }
            )

    def action_cancel(self):
        self.write({"state": "cancelled"})


class HrPayrollDemoBankTransferLine(models.Model):
    _name = "hr.payroll.demo.bank.transfer.line"
    _description = "Demo Payroll Bank Transfer Line"
    _order = "employee_id"

    transfer_id = fields.Many2one("hr.payroll.demo.bank.transfer", required=True, ondelete="cascade")
    company_id = fields.Many2one(related="transfer_id.company_id", store=True)
    currency_id = fields.Many2one(related="transfer_id.currency_id", readonly=True)
    employee_id = fields.Many2one("hr.employee", required=True)
    department_id = fields.Many2one(related="employee_id.department_id", store=True)
    payslip_id = fields.Many2one("hr.payslip")
    bank_account_id = fields.Many2one("res.partner.bank")
    amount = fields.Monetary(currency_field="currency_id")
    status = fields.Selection(
        [
            ("ready", "Ready"),
            ("missing_bank", "Missing Bank"),
            ("sent", "Sent"),
            ("reconciled", "Reconciled"),
            ("failed", "Failed"),
        ],
        default="ready",
    )
    note = fields.Char()
