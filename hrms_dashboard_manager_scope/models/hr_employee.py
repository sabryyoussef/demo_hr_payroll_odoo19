from odoo import api, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_manager_dashboard_scope(self, department_id=False):
        """Return company-wide KPIs for the active company, optionally by department."""
        if not self.env.user.has_group("hr.group_hr_manager"):
            return {}

        company = self.env.company
        department_id = int(department_id or 0)

        employee_domain = [("company_id", "=", company.id), ("active", "=", True)]
        employee_link_domain = [("employee_id.company_id", "=", company.id)]

        if department_id:
            employee_domain.append(("department_id", "=", department_id))
            employee_link_domain.append(("employee_id.department_id", "=", department_id))

        Employee = self.env["hr.employee"].sudo()
        Department = self.env["hr.department"].sudo()
        Contract = self.env["hr.version"].sudo()
        Payslip = self.env["hr.payslip"].sudo()
        Attendance = self.env["hr.attendance"].sudo()
        Leave = self.env["hr.leave"].sudo()
        Expense = self.env["hr.expense"].sudo()

        departments = Department.search(
            ["|", ("company_id", "=", company.id), ("company_id", "=", False)],
            order="name",
        )
        payslip_domain = [("company_id", "=", company.id)]
        contract_domain = [("company_id", "=", company.id)]
        if department_id:
            payslip_domain.append(("employee_id.department_id", "=", department_id))
            contract_domain.append(("employee_id.department_id", "=", department_id))

        return {
            "company_id": company.id,
            "company_name": company.name,
            "department_id": department_id,
            "department_name": Department.browse(department_id).display_name if department_id else "All Departments",
            "departments": [{"id": department.id, "name": department.display_name} for department in departments],
            "employee_count": Employee.search_count(employee_domain),
            "department_count": len(departments),
            "contract_count": Contract.search_count(contract_domain),
            "payslip_count": Payslip.search_count(payslip_domain),
            "attendance_count": Attendance.search_count(employee_link_domain),
            "leave_count": Leave.search_count(employee_link_domain),
            "leave_to_approve_count": Leave.search_count(employee_link_domain + [("state", "in", ["confirm", "validate1"])]),
            "expense_count": Expense.search_count(employee_link_domain),
            "expense_to_approve_count": Expense.search_count(employee_link_domain + [("state", "in", ["reported", "submitted"])]),
        }
