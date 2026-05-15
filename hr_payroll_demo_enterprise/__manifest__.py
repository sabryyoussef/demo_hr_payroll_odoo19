{
    "name": "HR Payroll Demo Enterprise",
    "version": "19.0.1.0.7",
    "category": "Human Resources/Payroll",
    "summary": "Production-grade HR, attendance, payroll, banking and mass operations demo",
    "description": (
        "Realistic medium-size company demo for Odoo 19 HR and Payroll operations. "
        "Includes a full demo company, departments, employees, contracts, attendance, "
        "leaves, payroll batches, banking workflow, reconciliation examples, dashboards, "
        "mass operation shortcuts, reports, tests, Playwright demo automation and docs."
    ),
    "author": "AllNetworks Demo Team",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "approvals",
        "hr_payroll_account",
        "account",
        "hr_attendance",
        "hr_holidays",
        "hr_skills",
        "hr_expense",
        "knowledge",
        "project_todo",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/hr_leave_type_compat.xml",
        "data/demo_config_data.xml",
        "data/demo_time_off_actions.xml",
        "views/hr_payroll_demo_bank_transfer_views.xml",
        "views/hr_payroll_demo_mass_operation_views.xml",
        "views/hr_payroll_demo_dashboard_views.xml",
        "views/hr_payroll_demo_report_views.xml",
        "views/hr_payroll_demo_training_views.xml",
        "views/hr_payroll_demo_knowledge_ai_views.xml",
        "views/hr_payroll_demo_workflow_views.xml",
        "views/hr_payroll_demo_menu.xml",
    ],
    "demo": [
        "demo/demo_marker.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "hr_payroll_demo_enterprise/static/src/css/workflow_dashboard.css",
        ],
    },
    "post_init_hook": "post_init_hook",
}
