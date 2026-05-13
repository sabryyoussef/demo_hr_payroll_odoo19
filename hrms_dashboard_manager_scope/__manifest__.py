{
    "name": "Open HRMS Dashboard Manager Scope",
    "version": "19.0.1.0.0",
    "category": "Human Resources",
    "summary": "Adds company and department managerial KPIs to Open HRMS Dashboard",
    "description": """
Adds a managerial company-wide dashboard layer to Open HRMS Dashboard without
modifying the original module. HR managers can view all active employees and
filter core HR, payroll, attendance, leave and expense counters by department.
    """,
    "author": "AllNetworks Demo Team",
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "hrms_dashboard",
        "hr_payroll",
        "hr_attendance",
        "hr_holidays",
        "hr_expense",
    ],
    "assets": {
        "web.assets_backend": [
            "hrms_dashboard_manager_scope/static/src/js/manager_scope_dashboard.js",
            "hrms_dashboard_manager_scope/static/src/xml/manager_scope_dashboard.xml",
            "hrms_dashboard_manager_scope/static/src/css/manager_scope_dashboard.css",
        ],
    },
}
