from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = "hr_payroll_demo_enterprise"
    company = env.ref(f"{module}.company_allnetworks_caribbean", raise_if_not_found=False)
    if not company:
        return

    for xmlid in ("dashboard_allnetworks_payroll", "workflow_dashboard_allnetworks"):
        dashboard = env.ref(f"{module}.{xmlid}", raise_if_not_found=False)
        if dashboard and "company_id" in dashboard._fields:
            dashboard.company_id = company
