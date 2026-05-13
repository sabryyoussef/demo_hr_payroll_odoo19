from odoo import _, fields, models


class HrPayrollDemoWorkflowDashboard(models.Model):
    _name = "hr.payroll.demo.workflow.dashboard"
    _description = "HR Payroll Demo Workflow Story Dashboard"

    name = fields.Char(default="ALLNETWORKS HR Payroll Workflow Story", required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    step_ids = fields.One2many("hr.payroll.demo.workflow.step", "dashboard_id", string="Workflow Steps")
    employee_count = fields.Integer(compute="_compute_kpis")
    attendance_count = fields.Integer(compute="_compute_kpis")
    payslip_count = fields.Integer(compute="_compute_kpis")
    expense_count = fields.Integer(compute="_compute_kpis")
    bank_transfer_count = fields.Integer(compute="_compute_kpis")
    accounting_entry_count = fields.Integer(compute="_compute_kpis")
    knowledge_article_count = fields.Integer(compute="_compute_kpis")
    monthly_net_total = fields.Monetary(compute="_compute_kpis", currency_field="currency_id")
    total_duration_minutes = fields.Integer(compute="_compute_duration")
    last_refresh = fields.Datetime(default=fields.Datetime.now)

    def _compute_kpis(self):
        Employee = self.env["hr.employee"].sudo()
        Attendance = self.env["hr.attendance"].sudo()
        Payslip = self.env["hr.payslip"].sudo()
        Expense = self.env["hr.expense"].sudo()
        Transfer = self.env["hr.payroll.demo.bank.transfer"].sudo()
        Move = self.env["account.move"].sudo()
        Knowledge = self.env["knowledge.article"].sudo() if "knowledge.article" in self.env.registry.models else False
        for dashboard in self:
            company_domain = [("company_id", "=", dashboard.company_id.id)]
            employee_company_domain = [("employee_id.company_id", "=", dashboard.company_id.id)]
            dashboard.employee_count = Employee.search_count(company_domain + [("active", "=", True)])
            dashboard.attendance_count = Attendance.search_count(employee_company_domain)
            payslips = Payslip.search(company_domain)
            dashboard.payslip_count = len(payslips)
            dashboard.monthly_net_total = sum(payslips.mapped("net_wage"))
            dashboard.expense_count = Expense.search_count(employee_company_domain)
            dashboard.bank_transfer_count = Transfer.search_count(company_domain)
            dashboard.accounting_entry_count = Move.search_count([("ref", "ilike", "ALLNETWORKS HR Accounting")])
            dashboard.knowledge_article_count = Knowledge.search_count([]) if Knowledge else 0

    def _compute_duration(self):
        for dashboard in self:
            dashboard.total_duration_minutes = sum(dashboard.step_ids.mapped("duration_minutes"))

    def action_refresh(self):
        self.write({"last_refresh": fields.Datetime.now()})

    def action_open_workflow_steps(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Workflow Story Steps"),
            "res_model": "hr.payroll.demo.workflow.step",
            "view_mode": "kanban,list,form",
            "domain": [("dashboard_id", "=", self.id)],
            "context": {
                "default_dashboard_id": self.id,
                "default_company_id": self.company_id.id,
                "allowed_company_ids": [self.company_id.id],
            },
        }

    def action_start_story(self):
        self.ensure_one()
        first_step = self.step_ids.sorted("sequence")[:1]
        return first_step.action_open_target() if first_step else self.action_open_workflow_steps()


class HrPayrollDemoWorkflowStep(models.Model):
    _name = "hr.payroll.demo.workflow.step"
    _description = "HR Payroll Demo Workflow Step"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    dashboard_id = fields.Many2one("hr.payroll.demo.workflow.dashboard", required=True, ondelete="cascade")
    company_id = fields.Many2one(related="dashboard_id.company_id", store=True, readonly=True)
    category = fields.Selection(
        [
            ("foundation", "HR Foundation"),
            ("activity", "Workforce Activity"),
            ("payroll", "Payroll Execution"),
            ("finance", "Finance Handoff"),
            ("accounting", "Accounting Close"),
            ("knowledge", "Knowledge & AI"),
        ],
        default="foundation",
        required=True,
    )
    status = fields.Selection(
        [
            ("ready", "Ready"),
            ("review", "Review"),
            ("optional", "Optional"),
        ],
        default="ready",
        required=True,
    )
    description = fields.Text(required=True)
    presenter_script = fields.Text()
    duration_minutes = fields.Integer(default=8)
    kpi_label = fields.Char()
    kpi_value = fields.Char(compute="_compute_kpi_value")
    real_menu_path = fields.Char(help="Presenter hint showing where this screen lives in the standard Odoo menu.")
    target_action_xmlid = fields.Char()
    target_model = fields.Char()
    target_view_mode = fields.Char(default="list,form")
    button_label = fields.Char(default="Open Screen")

    def _compute_kpi_value(self):
        Employee = self.env["hr.employee"].sudo()
        Department = self.env["hr.department"].sudo()
        Attendance = self.env["hr.attendance"].sudo()
        Leave = self.env["hr.leave"].sudo()
        WorkEntry = self.env["hr.work.entry"].sudo()
        PayslipRun = self.env["hr.payslip.run"].sudo()
        Payslip = self.env["hr.payslip"].sudo()
        Expense = self.env["hr.expense"].sudo()
        Transfer = self.env["hr.payroll.demo.bank.transfer"].sudo()
        Move = self.env["account.move"].sudo()
        Training = self.env["hr.payroll.demo.training"].sudo()
        Knowledge = self.env["knowledge.article"].sudo() if "knowledge.article" in self.env.registry.models else False
        Ask = self.env["hr.payroll.demo.knowledge.ask"].sudo()
        for step in self:
            company = step.company_id
            company_domain = [("company_id", "=", company.id)]
            employee_company_domain = [("employee_id.company_id", "=", company.id)]
            values = {
                "company_setup": lambda: _("%s departments") % Department.search_count(company_domain),
                "employees": lambda: _("%s active employees") % Employee.search_count(company_domain + [("active", "=", True)]),
                "contracts": lambda: _("%s employees") % Employee.search_count(company_domain + [("active", "=", True)]),
                "training": lambda: _("%s training sessions") % Training.search_count(company_domain),
                "attendance": lambda: _("%s attendance records") % Attendance.search_count(employee_company_domain),
                "time_off": lambda: _("%s time off records") % Leave.search_count(employee_company_domain),
                "work_entries": lambda: _("%s work entries") % WorkEntry.search_count(employee_company_domain),
                "payroll_batches": lambda: _("%s payroll batches") % PayslipRun.search_count(company_domain),
                "payslips": lambda: _("%s payslips") % Payslip.search_count(company_domain),
                "expenses": lambda: _("%s expenses") % Expense.search_count(employee_company_domain),
                "bank_transfer": lambda: _("%s bank transfers") % Transfer.search_count(company_domain),
                "accounting": lambda: _("%s HR accounting entries") % Move.search_count([("ref", "ilike", "ALLNETWORKS HR Accounting")]),
                "reconciliation": lambda: _("%s reconciliation cases")
                % self.env["hr.payroll.demo.reconciliation"].sudo().search_count(company_domain),
                "knowledge": lambda: _("%s knowledge articles") % (Knowledge.search_count([]) if Knowledge else 0),
                "ai": lambda: _("%s sample questions") % Ask.search_count(company_domain),
            }
            step.kpi_value = values.get(step.code, lambda: _("Ready"))()

    def _company_context(self):
        self.ensure_one()
        return {
            "allowed_company_ids": [self.company_id.id],
            "default_company_id": self.company_id.id,
        }

    def _target_domain(self):
        self.ensure_one()
        company_id = self.company_id.id
        company_domain = [("company_id", "=", company_id)]
        employee_company_domain = [("employee_id.company_id", "=", company_id)]
        domains = {
            "company_setup": company_domain,
            "employees": company_domain + [("active", "=", True)],
            "training": company_domain,
            "attendance": employee_company_domain,
            "time_off": employee_company_domain,
            "work_entries": employee_company_domain,
            "payroll_batches": company_domain,
            "payslips": company_domain,
            "expenses": employee_company_domain,
            "bank_transfer": company_domain,
            "accounting": [("ref", "ilike", "ALLNETWORKS HR Accounting")],
            "reconciliation": company_domain,
            "ai": company_domain,
        }
        return domains.get(self.code, [])

    def _fallback_action(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.name,
            "res_model": self.target_model or self._name,
            "view_mode": self.target_view_mode or "list,form",
            "domain": self._target_domain(),
            "context": self._company_context(),
            "target": "current",
        }

    def action_open_target(self):
        self.ensure_one()
        action = False
        if self.target_action_xmlid:
            action_record = self.env.ref(self.target_action_xmlid, raise_if_not_found=False)
            if action_record:
                action = action_record.read()[0]
        if not action:
            action = self._fallback_action()
        context = action.get("context") if isinstance(action.get("context"), dict) else {}
        context.update(self._company_context())
        action["context"] = context
        action["domain"] = self._target_domain()
        action["target"] = "current"
        return action
