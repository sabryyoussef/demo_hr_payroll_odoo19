/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { onWillStart } from "@odoo/owl";
import { user } from "@web/core/user";
import { HrDashboard } from "@hrms_dashboard/js/dashboard";

patch(HrDashboard.prototype, {
    setup() {
        super.setup(...arguments);
        this.state.manager_scope = {};
        onWillStart(async () => {
            if (await user.hasGroup("hr.group_hr_manager")) {
                await this.loadManagerScope(false);
            }
        });
    },

    getManagerAllowedCompanyIds() {
        const allowedCompanies = session.user_companies?.allowed_companies || {};
        const allowedCompanyIds = Object.keys(allowedCompanies).map((companyId) => parseInt(companyId));
        const contextCompanyIds = user.context?.allowed_company_ids || session.user_context?.allowed_company_ids || [];
        return allowedCompanyIds.length ? allowedCompanyIds : contextCompanyIds;
    },

    getManagerContext() {
        const allowedCompanyIds = this.getManagerAllowedCompanyIds();
        const context = {};
        if (allowedCompanyIds.length) {
            context.allowed_company_ids = allowedCompanyIds;
        }
        return context;
    },

    async loadManagerScope(departmentId) {
        this.state.manager_scope = await this.orm.call(
            "hr.employee",
            "get_manager_dashboard_scope",
            [departmentId || false],
            { context: this.getManagerContext() }
        );
    },

    async onManagerDepartmentChange(ev) {
        const departmentId = ev.target.value ? parseInt(ev.target.value) : false;
        await this.loadManagerScope(departmentId);
    },

    managerDepartmentDomain() {
        const scope = this.state.manager_scope || {};
        return scope.department_id ? [["department_id", "=", scope.department_id]] : [];
    },

    managerEmployeeLinkDomain() {
        const scope = this.state.manager_scope || {};
        return scope.department_id ? [["employee_id.department_id", "=", scope.department_id]] : [];
    },

    openManagerEmployees() {
        this.action.doAction({
            name: _t("Employees"),
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            view_mode: "list,kanban,form",
            views: [[false, "list"], [false, "kanban"], [false, "form"]],
            domain: [["company_id", "=", this.state.manager_scope.company_id], ["active", "=", true], ...this.managerDepartmentDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },

    openManagerContracts() {
        this.action.doAction({
            name: _t("Employee Contracts"),
            type: "ir.actions.act_window",
            res_model: "hr.version",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["company_id", "=", this.state.manager_scope.company_id], ...this.managerEmployeeLinkDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },

    openManagerPayslips() {
        this.action.doAction({
            name: _t("Payslips"),
            type: "ir.actions.act_window",
            res_model: "hr.payslip",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["company_id", "=", this.state.manager_scope.company_id], ...this.managerEmployeeLinkDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },

    openManagerAttendances() {
        this.action.doAction({
            name: _t("Attendances"),
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["employee_id.company_id", "=", this.state.manager_scope.company_id], ...this.managerEmployeeLinkDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },

    openManagerLeaves() {
        this.action.doAction({
            name: _t("Time Off"),
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            view_mode: "list,form,calendar",
            views: [[false, "list"], [false, "form"], [false, "calendar"]],
            domain: [["employee_id.company_id", "=", this.state.manager_scope.company_id], ...this.managerEmployeeLinkDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },

    openManagerExpenses() {
        this.action.doAction({
            name: _t("Employee Expenses"),
            type: "ir.actions.act_window",
            res_model: "hr.expense",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["employee_id.company_id", "=", this.state.manager_scope.company_id], ...this.managerEmployeeLinkDomain()],
            context: this.getManagerContext(),
            target: "current",
        });
    },
});
