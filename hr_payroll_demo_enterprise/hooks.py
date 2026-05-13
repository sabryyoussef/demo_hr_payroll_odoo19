from datetime import datetime, time
from html import escape
from dateutil.relativedelta import relativedelta

from odoo import Command, SUPERUSER_ID, api, fields


MODULE = "hr_payroll_demo_enterprise"


DEPARTMENTS = [
    ("executive", "Executive and Administration", 6, 7600),
    ("hr", "Human Resources", 8, 4200),
    ("finance", "Finance and Accounting", 10, 5100),
    ("sales", "Sales", 18, 3500),
    ("support", "Customer Support", 16, 3200),
    ("operations", "Operations", 14, 3900),
    ("warehouse", "Warehouse and Logistics", 20, 3000),
    ("it", "IT and Systems", 5, 4700),
    ("temporary", "Temporary and Interns", 3, 1800),
]

DEPARTMENT_ROLES = {
    "executive": ["General Manager", "Office Manager", "Executive Assistant", "Compliance Officer"],
    "hr": ["HR Manager", "Payroll Specialist", "Recruiter", "HR Officer", "HR Coordinator"],
    "finance": ["Finance Manager", "Payroll Accountant", "AP Officer", "AR Officer", "Accountant"],
    "sales": ["Sales Manager", "Account Executive", "Sales Representative", "Sales Coordinator"],
    "support": ["Support Manager", "Support Team Lead", "Support Agent", "Quality Analyst"],
    "operations": ["Operations Manager", "Dispatcher", "Field Supervisor", "Field Technician"],
    "warehouse": ["Warehouse Manager", "Inventory Supervisor", "Inventory Clerk", "Picker", "Driver", "Forklift Operator"],
    "it": ["IT Manager", "System Administrator", "Helpdesk Analyst"],
    "temporary": ["HR Intern", "Warehouse Temp", "Finance Intern"],
}

EMPLOYEE_CATEGORIES = {
    "full_time": "Full-time salaried",
    "hourly": "Hourly operations",
    "warehouse_biweekly": "Warehouse bi-weekly",
    "sales_commission": "Sales commission",
    "manager": "Managers",
    "fixed_term": "Fixed-term contract",
    "intern": "Interns",
    "remote": "Remote and hybrid",
    "sporadic_bonus": "Sporadic - one-time bonus",
    "sporadic_commission": "Sporadic - exceptional commission",
    "sporadic_overtime": "Sporadic - overtime payout",
    "sporadic_allowance": "Sporadic - temporary allowance",
    "sporadic_retro": "Sporadic - retroactive adjustment",
    "sporadic_deduction": "Sporadic - deduction or recovery",
    "sporadic_final_payoff": "Sporadic - final payoff",
}

FIRST_NAMES = [
    "Alicia", "Marcus", "Janelle", "Devon", "Priya", "Omar", "Natalie", "Andre",
    "Sofia", "Miguel", "Leah", "Darren", "Camila", "Rafael", "Tanya", "Noah",
    "Imani", "Victor", "Bianca", "Ethan", "Maya", "Julian", "Kiara", "Samuel",
    "Elena", "Carlos", "Nadia", "Malik", "Serena", "Adrian", "Fatima", "Jason",
    "Renee", "Dwayne", "Amara", "Luis", "Kayla", "Hassan", "Monique", "Diego",
    "Chloe", "Aaron", "Lina", "Rohan", "Isabella", "Theo", "Yara", "Mateo",
    "Grace", "Kareem", "Nia", "Leon", "Zara", "Tariq", "Mila", "Simon",
]
LAST_NAMES = [
    "Bennett", "Clarke", "Joseph", "Ramirez", "Singh", "Williams", "Mendez", "Brown",
    "Campbell", "Thomas", "Hernandez", "Francis", "Ali", "Roberts", "Morgan", "Reyes",
]


def post_init_hook(env):
    env = api.Environment(env.cr, SUPERUSER_ID, {})
    if _xmlid_record(env, "company_allnetworks_caribbean"):
        return
    company = _create_company(env)
    _ensure_admin_company(env, company)
    structures = _prepare_payroll_structures(env)
    leave_types = _prepare_leave_types(env, company)
    categories = _prepare_employee_categories(env)
    departments, jobs, calendars, locations = _create_org(env, company)
    _create_contract_templates(env, company, departments, jobs, calendars, structures)
    employees = _create_employees(env, company, departments, jobs, calendars, locations, structures, categories)
    _assign_managers(departments, employees)
    _create_bank_accounts(env, employees)
    _create_attendance(env, employees)
    _create_leave_allocations(env, employees, leave_types)
    accrual_plans = _create_accrual_plans(env, company, leave_types)
    _create_accrual_allocations(env, employees, leave_types, accrual_plans)
    _create_leaves(env, employees, leave_types)
    batches = _create_payroll(env, company, employees, structures)
    _create_sporadic_employee_scenarios(env, company, employees, categories, batches)
    transfers = _create_bank_transfers(env, company, batches)
    _create_reports(env, company, departments, employees, batches, transfers)
    _create_mass_operations(env, company, departments)
    _create_scenarios(env, employees, departments)
    _create_certifications(env, employees)
    _create_training_sessions(env, company, employees, departments)
    _create_expenses(env, company, employees)
    _create_accounting_entries(env, company, employees, batches, transfers)
    _create_knowledge_base(env, company)
    _create_knowledge_ai_questions(env, company)
    dashboard = env.ref(f"{MODULE}.dashboard_allnetworks_payroll", raise_if_not_found=False)
    if dashboard:
        dashboard.company_id = company
    workflow_dashboard = env.ref(f"{MODULE}.workflow_dashboard_allnetworks", raise_if_not_found=False)
    if workflow_dashboard:
        workflow_dashboard.company_id = company


def _xmlid_record(env, name):
    data = env["ir.model.data"].search([("module", "=", MODULE), ("name", "=", name)], limit=1)
    return env[data.model].browse(data.res_id) if data else False


def _register_xmlid(env, record, name):
    existing = env["ir.model.data"].search([("module", "=", MODULE), ("name", "=", name)], limit=1)
    if existing:
        return
    env["ir.model.data"].create(
        {
            "module": MODULE,
            "name": name,
            "model": record._name,
            "res_id": record.id,
            "noupdate": True,
        }
    )


def _create_company(env):
    usd = env.ref("base.USD", raise_if_not_found=False) or env.company.currency_id
    company = env["res.company"].create(
        {
            "name": "ALLNETWORKS Caribbean Holdings Ltd",
            "currency_id": usd.id,
            "email": "hr@allnetworks-caribbean.example.com",
            "phone": "+1 246 555 0199",
            "street": "Harbour View Business Park",
            "city": "Bridgetown",
        }
    )
    _register_xmlid(env, company, "company_allnetworks_caribbean")
    return company


def _ensure_admin_company(env, company):
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if admin:
        admin.write({"company_ids": [Command.link(company.id)], "company_id": company.id})
        demo_manager_group = env.ref(f"{MODULE}.group_hr_payroll_demo_manager", raise_if_not_found=False)
        if demo_manager_group:
            admin.write({"group_ids": [Command.link(demo_manager_group.id)]})


def _prepare_payroll_structures(env):
    employee_type = env.ref("hr.structure_type_employee")
    worker_type = env.ref("hr.structure_type_worker")
    regular = env.ref("hr_payroll.structure_002")
    worker = env.ref("hr_payroll.structure_worker_001")
    employee_type.default_schedule_pay = "monthly"
    worker_type.default_schedule_pay = "bi-weekly"

    input_defs = [
        ("input_overtime", "Overtime", "OVERTIME"),
        ("input_bonus", "Bonus", "BONUS"),
        ("input_commission", "Sales Commission", "COMMISSION"),
        ("input_loan", "Loan Installment", "LOAN"),
        ("input_absence", "Absence / Late Penalty", "ABSENCE"),
        ("input_retro", "Retroactive Adjustment", "RETRO"),
        ("input_transport", "Transportation Allowance", "TRANSPORT"),
        ("input_housing", "Housing Allowance", "HOUSING"),
    ]
    input_types = {}
    for xml_name, label, code in input_defs:
        input_type = env["hr.payslip.input.type"].create(
            {"name": label, "code": code, "struct_ids": [Command.link(regular.id), Command.link(worker.id)]}
        )
        _register_xmlid(env, input_type, xml_name)
        input_types[code] = input_type

    category_allowance = env.ref("hr_payroll.ALW")
    category_ded = env.ref("hr_payroll.DED")
    rule_defs = [
        ("rule_housing", "Housing Allowance", "HOUSING", category_allowance, 31, "inputs['HOUSING'].amount if 'HOUSING' in inputs else 0.0"),
        ("rule_transport", "Transportation Allowance", "TRANSPORT", category_allowance, 32, "inputs['TRANSPORT'].amount if 'TRANSPORT' in inputs else 0.0"),
        ("rule_overtime", "Overtime", "OVERTIME", category_allowance, 33, "inputs['OVERTIME'].amount if 'OVERTIME' in inputs else 0.0"),
        ("rule_bonus", "Bonus", "BONUS", category_allowance, 34, "inputs['BONUS'].amount if 'BONUS' in inputs else 0.0"),
        ("rule_commission", "Sales Commission", "COMMISSION", category_allowance, 35, "inputs['COMMISSION'].amount if 'COMMISSION' in inputs else 0.0"),
        ("rule_retro", "Retroactive Adjustment", "RETRO", category_allowance, 36, "inputs['RETRO'].amount if 'RETRO' in inputs else 0.0"),
        ("rule_loan", "Loan Deduction", "LOAN", category_ded, 180, "-inputs['LOAN'].amount if 'LOAN' in inputs else 0.0"),
        ("rule_absence", "Absence / Late Penalty", "ABSENCE", category_ded, 181, "-inputs['ABSENCE'].amount if 'ABSENCE' in inputs else 0.0"),
    ]
    for xml_name, label, code, category, seq, expression in rule_defs:
        for struct in (regular, worker):
            rule = env["hr.salary.rule"].create(
                {
                    "name": label,
                    "code": code,
                    "sequence": seq,
                    "category_id": category.id,
                    "condition_select": "python",
                    "condition_python": f"result = '{code}' in inputs and inputs['{code}'].amount",
                    "amount_select": "code",
                    "amount_python_compute": f"result = {expression}",
                    "struct_id": struct.id,
                }
            )
            _register_xmlid(env, rule, f"{xml_name}_{struct.id}")
    return {"monthly": employee_type, "biweekly": worker_type, "regular": regular, "worker": worker, "inputs": input_types}


def _prepare_leave_types(env, company):
    vals = [
        ("annual", "Annual Leave", False, "manager"),
        ("sick", "Sick Leave", False, "hr"),
        ("casual", "Casual Leave", False, "manager"),
        ("unpaid", "Unpaid Leave", True, "hr"),
        ("emergency", "Emergency Leave", False, "hr"),
    ]
    result = {}
    for key, name, unpaid, validation in vals:
        leave_type = env["hr.leave.type"].create(
            {
                "name": name,
                "company_id": company.id,
                "requires_allocation": False,
                "leave_validation_type": validation,
                "unpaid": unpaid,
            }
        )
        _register_xmlid(env, leave_type, f"leave_type_{key}")
        result[key] = leave_type
    return result


def _prepare_employee_categories(env):
    categories = {}
    for key, name in EMPLOYEE_CATEGORIES.items():
        category = env["hr.employee.category"].create({"name": name})
        _register_xmlid(env, category, f"employee_category_{key}")
        categories[key] = category
    return categories


def _create_contract_templates(env, company, departments, jobs, calendars, structures):
    today = fields.Date.today()
    Version = env["hr.version"].with_company(company)
    hr_user = env.ref("base.user_admin")
    work_entry_source_field = Version._fields.get("work_entry_source")
    available_work_entry_sources = set()
    if work_entry_source_field:
        available_work_entry_sources = {
            key for key, _label in work_entry_source_field._description_selection(env)
        }

    def _contract_type(xmlid):
        return env.ref(xmlid, raise_if_not_found=False)

    permanent = _contract_type("hr.contract_type_permanent")
    temporary = _contract_type("hr.contract_type_temporary")
    full_time = _contract_type("hr.contract_type_full_time")
    part_time = _contract_type("hr.contract_type_part_time")
    intern = _contract_type("hr.contract_type_intern")
    seasonal = _contract_type("hr.contract_type_seasonal")

    template_defs = [
        {
            "xmlid": "contract_template_executive_monthly",
            "name": "Executive Leadership - Monthly Salary",
            "department": "executive",
            "job": ("executive", "general_manager"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "standard",
            "wage": 8500.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Senior leadership template with monthly payroll, full benefits eligibility, and board-level approval.",
        },
        {
            "xmlid": "contract_template_hr_payroll_monthly",
            "name": "HR & Payroll Specialist - Monthly Salary",
            "department": "hr",
            "job": ("hr", "payroll_specialist"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "standard",
            "wage": 5200.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Standard monthly HR/payroll template for employees handling sensitive personnel and payroll operations.",
        },
        {
            "xmlid": "contract_template_finance_accountant_monthly",
            "name": "Finance Accountant - Monthly Salary",
            "department": "finance",
            "job": ("finance", "accountant"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "standard",
            "wage": 5000.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Finance staff template with monthly salary and payroll accounting responsibilities.",
        },
        {
            "xmlid": "contract_template_sales_commission",
            "name": "Sales Representative - Monthly + Commission",
            "department": "sales",
            "job": ("sales", "sales_representative"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "standard",
            "wage": 3900.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Sales template used for employees with base salary plus commission inputs during payroll.",
        },
        {
            "xmlid": "contract_template_support_shift",
            "name": "Customer Support Agent - Shift Schedule",
            "department": "support",
            "job": ("support", "support_agent"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "support_evening",
            "wage": 3400.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Support-center template for evening shift teams with SLA-driven attendance monitoring.",
        },
        {
            "xmlid": "contract_template_operations_field_biweekly",
            "name": "Field Technician - Bi-weekly Attendance",
            "department": "operations",
            "job": ("operations", "field_technician"),
            "contract_type": permanent or full_time,
            "structure": structures["biweekly"],
            "calendar": "field_flexible",
            "wage": 0.0,
            "hourly_wage": 24.0,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "work_entry_source": "attendance",
            "employee_type": "worker",
            "note": "Field operations template using attendance-based work entries and bi-weekly payroll.",
        },
        {
            "xmlid": "contract_template_warehouse_day_biweekly",
            "name": "Warehouse Day Shift - Bi-weekly Hourly",
            "department": "warehouse",
            "job": ("warehouse", "picker"),
            "contract_type": permanent or full_time,
            "structure": structures["biweekly"],
            "calendar": "warehouse_day",
            "wage": 0.0,
            "hourly_wage": 20.0,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "work_entry_source": "attendance",
            "employee_type": "worker",
            "note": "Warehouse day-shift hourly template with overtime and attendance exception scenarios.",
        },
        {
            "xmlid": "contract_template_warehouse_night_premium",
            "name": "Warehouse Night Shift - Premium Hourly",
            "department": "warehouse",
            "job": ("warehouse", "forklift_operator"),
            "contract_type": permanent or full_time,
            "structure": structures["biweekly"],
            "calendar": "warehouse_night",
            "wage": 0.0,
            "hourly_wage": 23.5,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "work_entry_source": "attendance",
            "employee_type": "worker",
            "note": "Night-shift hourly template for premium pay, cross-midnight attendance, and safety certification demos.",
        },
        {
            "xmlid": "contract_template_it_remote",
            "name": "IT Systems Analyst - Remote Hybrid",
            "department": "it",
            "job": ("it", "helpdesk_analyst"),
            "contract_type": permanent or full_time,
            "structure": structures["monthly"],
            "calendar": "remote",
            "wage": 4800.0,
            "wage_type": "monthly",
            "schedule_pay": "monthly",
            "employee_type": "employee",
            "note": "Remote/hybrid IT template with flexible calendar and cybersecurity certification expectations.",
        },
        {
            "xmlid": "contract_template_fixed_term_project",
            "name": "Fixed-term Project Contractor",
            "department": "operations",
            "job": ("operations", "dispatcher"),
            "contract_type": temporary or seasonal,
            "structure": structures["biweekly"],
            "calendar": "field_flexible",
            "wage": 0.0,
            "hourly_wage": 27.0,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "work_entry_source": "attendance",
            "employee_type": "contractor",
            "contract_months": 6,
            "note": "Fixed-term project template for temporary operational scale-ups and contract-renewal demos.",
        },
        {
            "xmlid": "contract_template_part_time_intern",
            "name": "Part-time Internship - Training Plan",
            "department": "temporary",
            "job": ("temporary", "hr_intern"),
            "contract_type": intern or part_time,
            "structure": structures["biweekly"],
            "calendar": "part_time",
            "wage": 0.0,
            "hourly_wage": 14.0,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "employee_type": "student",
            "contract_months": 3,
            "note": "Internship template connected to onboarding, training attendance, and certification progress demos.",
        },
        {
            "xmlid": "contract_template_seasonal_warehouse_peak",
            "name": "Seasonal Warehouse Peak Staffing",
            "department": "warehouse",
            "job": ("warehouse", "picker"),
            "contract_type": seasonal or temporary,
            "structure": structures["biweekly"],
            "calendar": "warehouse_day",
            "wage": 0.0,
            "hourly_wage": 18.0,
            "wage_type": "hourly",
            "schedule_pay": "bi-weekly",
            "work_entry_source": "attendance",
            "employee_type": "worker",
            "contract_months": 2,
            "note": "Seasonal peak-period template for bulk hiring, short-term payroll, and final payoff scenarios.",
        },
    ]

    for index, template_def in enumerate(template_defs, start=1):
        if _xmlid_record(env, template_def["xmlid"]):
            continue
        contract_months = template_def.get("contract_months")
        contract_start = today.replace(day=1)
        values = {
            "name": template_def["name"],
            "employee_id": False,
            "company_id": company.id,
            "date_version": contract_start,
            "contract_date_start": contract_start,
            "contract_date_end": contract_start + relativedelta(months=contract_months, days=-1) if contract_months else False,
            "trial_date_end": contract_start + relativedelta(months=3, days=-1) if not contract_months else False,
            "department_id": departments[template_def["department"]].id,
            "job_id": jobs[template_def["job"]].id,
            "hr_responsible_id": hr_user.id,
            "contract_type_id": template_def["contract_type"].id if template_def.get("contract_type") else False,
            "structure_type_id": template_def["structure"].id,
            "resource_calendar_id": calendars[template_def["calendar"]].id,
            "wage": template_def["wage"],
            "wage_type": template_def["wage_type"],
            "schedule_pay": template_def["schedule_pay"],
            "hourly_wage": template_def.get("hourly_wage", 0.0),
            "employee_type": template_def["employee_type"],
            "additional_note": template_def["note"],
        }
        if work_entry_source_field:
            requested_source = template_def.get("work_entry_source", "calendar")
            values["work_entry_source"] = (
                requested_source
                if requested_source in available_work_entry_sources
                else "calendar"
            )
        template = Version.create(values)
        _register_xmlid(env, template, template_def["xmlid"])


def _create_org(env, company):
    locations = {}
    for key, name in {
        "hq": "Bridgetown Head Office",
        "warehouse": "Warrens Distribution Center",
        "remote": "Remote Work",
        "sales": "Field Sales",
        "support": "Customer Support Center",
        "field": "Field Operations",
    }.items():
        loc = env["hr.work.location"].create({
            "name": name,
            "company_id": company.id,
            "location_type": "office" if key != "remote" else "home",
            "address_id": company.partner_id.id,
        })
        _register_xmlid(env, loc, f"work_location_{key}")
        locations[key] = loc

    calendars = {
        "standard": env.ref("resource.resource_calendar_std"),
        "support_morning": env["resource.calendar"].create({"name": "ALLNETWORKS Support Morning Shift", "company_id": company.id}),
        "support_evening": env["resource.calendar"].create({"name": "ALLNETWORKS Support Evening Shift", "company_id": company.id}),
        "warehouse_day": env["resource.calendar"].create({"name": "ALLNETWORKS Warehouse Day Shift", "company_id": company.id}),
        "warehouse_night": env["resource.calendar"].create({"name": "ALLNETWORKS Warehouse Night Shift", "company_id": company.id}),
        "field_flexible": env["resource.calendar"].create({"name": "ALLNETWORKS Field Flexible Schedule", "company_id": company.id}),
        "part_time": env["resource.calendar"].create({"name": "ALLNETWORKS Part-time Internship Schedule", "company_id": company.id}),
        "remote": env["resource.calendar"].create({"name": "ALLNETWORKS Remote Flexible Schedule", "company_id": company.id}),
    }
    _register_xmlid(env, calendars["support_morning"], "calendar_support_morning")
    _register_xmlid(env, calendars["support_evening"], "calendar_support_evening")
    _register_xmlid(env, calendars["warehouse_day"], "calendar_warehouse_day")
    _register_xmlid(env, calendars["warehouse_night"], "calendar_warehouse_night")
    _register_xmlid(env, calendars["field_flexible"], "calendar_field_flexible")
    _register_xmlid(env, calendars["part_time"], "calendar_part_time")
    _register_xmlid(env, calendars["remote"], "calendar_remote")

    departments = {}
    jobs = {}
    for key, name, _count, _base in DEPARTMENTS:
        dept = env["hr.department"].create({"name": name, "company_id": company.id})
        _register_xmlid(env, dept, f"department_{key}")
        departments[key] = dept
        for role in DEPARTMENT_ROLES[key]:
            job = env["hr.job"].create({"name": f"{name} {role}", "company_id": company.id})
            role_key = role.lower().replace(" ", "_")
            _register_xmlid(env, job, f"job_{key}_{role_key}")
            jobs[(key, role_key)] = job
    return departments, jobs, calendars, locations


def _employee_name(index):
    return f"{FIRST_NAMES[index % len(FIRST_NAMES)]} {LAST_NAMES[index % len(LAST_NAMES)]}"


def _employee_profile(dept_key, pos, index):
    roles = DEPARTMENT_ROLES[dept_key]
    role = roles[min(pos, len(roles) - 1)]
    role_key = role.lower().replace(" ", "_")
    is_manager = pos == 0 or "Manager" in role

    category_keys = ["full_time"]
    schedule = "monthly"
    calendar_key = "standard"
    location_key = "hq"

    if is_manager:
        category_keys.append("manager")
    if dept_key == "sales":
        category_keys.append("sales_commission")
        location_key = "sales"
    elif dept_key == "support":
        calendar_key = "support_morning" if pos % 2 == 0 else "support_evening"
        location_key = "support"
    elif dept_key == "operations":
        category_keys.append("hourly" if pos > 2 else "full_time")
        schedule = "biweekly" if pos > 4 else "monthly"
        calendar_key = "field_flexible"
        location_key = "field"
    elif dept_key == "warehouse":
        category_keys.extend(["hourly", "warehouse_biweekly"])
        schedule = "biweekly"
        calendar_key = "warehouse_night" if pos % 5 == 0 else "warehouse_day"
        location_key = "warehouse"
    elif dept_key == "it":
        calendar_key = "remote" if pos > 1 else "standard"
        location_key = "remote" if pos > 1 else "hq"
        if pos > 1:
            category_keys.append("remote")
    elif dept_key == "temporary":
        category_keys = ["intern"] if "Intern" in role else ["fixed_term", "hourly"]
        schedule = "biweekly"
        calendar_key = "part_time"
        location_key = "warehouse" if "Warehouse" in role else "hq"

    if index % 17 == 0 and "remote" not in category_keys:
        category_keys.append("remote")
        location_key = "remote"

    return role_key, category_keys, schedule, calendar_key, location_key


def _create_employees(env, company, departments, jobs, calendars, locations, structures, categories):
    employees = {}
    index = 0
    for dept_key, _dept_name, count, base_wage in DEPARTMENTS:
        dept_employees = []
        for pos in range(count):
            role_key, category_keys, schedule, calendar_key, location_key = _employee_profile(dept_key, pos, index)
            name = _employee_name(index)
            hire_date = fields.Date.today() - relativedelta(years=3, months=index % 18, days=index % 12)
            if index in (8, 29, 51):
                hire_date = fields.Date.today() - relativedelta(days=14)
            wage = base_wage + (1200 if pos == 0 else 650 if pos == 1 else (index % 7) * 135)
            if dept_key == "sales" and pos > 1:
                wage += 300
            if dept_key == "temporary":
                wage = base_wage + (index % 3) * 150
            location = locations[location_key]
            employee = env["hr.employee"].create(
                {
                    "name": name,
                    "company_id": company.id,
                    "department_id": departments[dept_key].id,
                    "job_id": jobs[(dept_key, role_key)].id,
                    "work_email": f"{name.lower().replace(' ', '.')}@allnetworks-caribbean.example.com",
                    "mobile_phone": f"+1 246 555 {1000 + index}",
                    "work_location_id": location.id,
                    "resource_calendar_id": calendars[calendar_key].id,
                    "contract_date_start": hire_date,
                    "contract_date_end": fields.Date.today() + relativedelta(months=6) if index in (12, 31, 72, 98) else False,
                    "structure_type_id": structures[schedule].id,
                    "contract_type_id": env.ref("hr.contract_type_employee", raise_if_not_found=False).id if env.ref("hr.contract_type_employee", raise_if_not_found=False) else False,
                    "wage": wage,
                    "category_ids": [Command.link(categories[key].id) for key in category_keys],
                }
            )
            if index in (44, 86):
                employee.active = False
                employee.departure_date = fields.Date.today() - relativedelta(days=10)
                employee.departure_description = "Demo resigned employee for final settlement payroll and payoff."
            _register_xmlid(env, employee, f"employee_{dept_key}_{pos + 1:02d}")
            dept_employees.append(employee)
            index += 1
        employees[dept_key] = dept_employees
    return employees


def _assign_managers(departments, employees):
    for dept_key, dept_employees in employees.items():
        manager = dept_employees[0]
        supervisor = dept_employees[1]
        departments[dept_key].manager_id = manager
        supervisor.parent_id = manager
        for employee in dept_employees[2:]:
            employee.parent_id = supervisor


def _create_bank_accounts(env, employees):
    banks = ["CIBC FirstCaribbean", "Republic Bank", "Scotiabank", "RBC Royal Bank"]
    counter = 0
    for dept_key, dept_employees in employees.items():
        for employee in dept_employees:
            partner = employee.work_contact_id
            if not partner:
                partner = env["res.partner"].create({"name": employee.name, "email": employee.work_email})
                employee.work_contact_id = partner
            bank = env["res.partner.bank"].create(
                {
                    "acc_number": f"BB{counter:02d}000{counter + 100000}",
                    "partner_id": partner.id,
                    "allow_out_payment": True,
                }
            )
            _register_xmlid(env, bank, f"bank_{dept_key}_{counter:02d}")
            employee.bank_account_ids = [Command.link(bank.id)]
            if counter % 17 == 0:
                second_bank = env["res.partner.bank"].create(
                    {
                        "acc_number": f"BB{counter:02d}SPLIT{counter + 200000}",
                        "partner_id": partner.id,
                        "allow_out_payment": True,
                    }
                )
                _register_xmlid(env, second_bank, f"bank_split_{counter:02d}")
                employee.bank_account_ids = [Command.link(second_bank.id)]
            counter += 1


def _create_attendance(env, employees):
    Attendance = env["hr.attendance"]
    start = fields.Date.today().replace(day=1) - relativedelta(months=3)
    all_employees = [emp for dept_employees in employees.values() for emp in dept_employees if emp.active]
    for emp_index, employee in enumerate(all_employees):
        day = start
        seq = 0
        while day <= fields.Date.today() - relativedelta(days=2):
            is_weekend_work = emp_index % 9 == 0 and day.weekday() == 5
            is_warehouse = employee.department_id.name == "Warehouse and Logistics"
            is_support = employee.department_id.name == "Customer Support"
            is_field = employee.department_id.name == "Operations"
            if day.weekday() < 5 or is_weekend_work:
                late_minutes = 25 if seq % 13 == 0 else 0
                overtime_hours = 2 if seq % 10 == 0 else 0
                if is_warehouse and emp_index % 5 == 0:
                    base_time = time(22, 0)
                    shift_hours = 8
                elif is_warehouse:
                    base_time = time(6, 0)
                    shift_hours = 8
                elif is_support and emp_index % 2:
                    base_time = time(15, 0)
                    shift_hours = 8
                elif is_support:
                    base_time = time(7, 0)
                    shift_hours = 8
                elif is_field:
                    base_time = time(9, 0)
                    shift_hours = 8
                    overtime_hours += 1 if seq % 12 == 0 else 0
                else:
                    base_time = time(8, 30)
                    shift_hours = 8
                check_in = datetime.combine(day, base_time) + relativedelta(minutes=late_minutes)
                check_out = check_in + relativedelta(hours=shift_hours + overtime_hours, minutes=30)
                attendance = Attendance.create(
                    {
                        "employee_id": employee.id,
                        "check_in": check_in,
                        "check_out": False if (seq % 37 == 0 and day > fields.Date.today() - relativedelta(days=8)) else check_out,
                        "in_mode": "manual",
                        "out_mode": "manual",
                    }
                )
                _register_xmlid(env, attendance, f"attendance_{employee.id}_{day.strftime('%Y%m%d')}")
            day += relativedelta(days=1)
            seq += 1


def _create_leaves(env, employees, leave_types):
    Leave = env["hr.leave"]
    all_employees = [emp for dept_employees in employees.values() for emp in dept_employees if emp.active]
    states = ["validate", "validate", "confirm", "refuse"]
    leave_keys = ["annual", "sick", "casual", "unpaid", "emergency"]
    for index, employee in enumerate(all_employees[:60]):
        start = fields.Date.today().replace(day=3) - relativedelta(months=index % 3)
        leave = Leave.create(
            {
                "employee_id": employee.id,
                "holiday_status_id": leave_types[leave_keys[index % len(leave_keys)]].id,
                "request_date_from": start,
                "request_date_to": start + relativedelta(days=index % 3),
                "private_name": f"Demo {leave_keys[index % len(leave_keys)]} leave scenario",
            }
        )
        target_state = states[index % len(states)]
        if target_state != "confirm":
            env.cr.execute("UPDATE hr_leave SET state = %s WHERE id = %s", (target_state, leave.id))
            leave.invalidate_recordset(["state"])
        _register_xmlid(env, leave, f"leave_{index:02d}")


def _create_leave_allocations(env, employees, leave_types):
    Allocation = env["hr.leave.allocation"]
    all_employees = [emp for dept_employees in employees.values() for emp in dept_employees if emp.active]
    for index, employee in enumerate(all_employees):
        allocation = Allocation.create(
            {
                "name": f"Annual Leave Allocation - {employee.name}",
                "employee_id": employee.id,
                "holiday_status_id": leave_types["annual"].id,
                "number_of_days": 18 if index % 5 else 21,
            }
        )
        env.cr.execute("UPDATE hr_leave_allocation SET state = %s WHERE id = %s", ("validate", allocation.id))
        allocation.invalidate_recordset(["state"])
        _register_xmlid(env, allocation, f"allocation_annual_{index:03d}")


def _create_accrual_plans(env, company, leave_types):
    Plan = env["hr.leave.accrual.plan"].with_company(company).sudo()
    Level = env["hr.leave.accrual.level"].sudo()

    def _create_level(plan, xmlid, vals):
        if _xmlid_record(env, xmlid):
            return
        vals = dict(vals, accrual_plan_id=plan.id)
        level = Level.create(vals)
        _register_xmlid(env, level, xmlid)

    plan_defs = [
        {
            "xmlid": "accrual_plan_annual_standard",
            "name": "ALLNETWORKS Standard Annual Leave Accrual",
            "time_off_type": "annual",
            "can_be_carryover": True,
            "carryover_date": "year_start",
            "transition_mode": "immediately",
            "accrued_gain_time": "end",
            "is_based_on_worked_time": False,
            "levels": [
                {"xmlid": "accrual_level_annual_standard_base", "milestone_date": "creation", "start_count": 0, "start_type": "day", "added_value": 1.5, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 24, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 5},
                {"xmlid": "accrual_level_annual_standard_senior", "milestone_date": "after", "start_count": 3, "start_type": "year", "added_value": 1.75, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 30, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 8},
                {"xmlid": "accrual_level_annual_standard_long_service", "milestone_date": "after", "start_count": 5, "start_type": "year", "added_value": 2.0, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 36, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 10},
            ],
        },
        {
            "xmlid": "accrual_plan_sick_monthly",
            "name": "ALLNETWORKS Sick Leave Monthly Accrual",
            "time_off_type": "sick",
            "can_be_carryover": False,
            "transition_mode": "immediately",
            "accrued_gain_time": "end",
            "is_based_on_worked_time": False,
            "levels": [
                {"xmlid": "accrual_level_sick_monthly", "milestone_date": "creation", "start_count": 0, "start_type": "day", "added_value": 0.75, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 12, "action_with_unused_accruals": "lost"},
            ],
        },
        {
            "xmlid": "accrual_plan_hourly_worked_time",
            "name": "ALLNETWORKS Hourly Worked-Time Accrual",
            "time_off_type": "annual",
            "can_be_carryover": True,
            "carryover_date": "year_start",
            "transition_mode": "end_of_accrual",
            "accrued_gain_time": "end",
            "is_based_on_worked_time": True,
            "levels": [
                {"xmlid": "accrual_level_hourly_worked_time_base", "milestone_date": "creation", "start_count": 0, "start_type": "day", "added_value": 0.05, "frequency": "daily", "cap_accrued_time": True, "maximum_leave": 18, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 4},
                {"xmlid": "accrual_level_hourly_worked_time_senior", "milestone_date": "after", "start_count": 2, "start_type": "year", "added_value": 0.07, "frequency": "daily", "cap_accrued_time": True, "maximum_leave": 24, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 6},
            ],
        },
        {
            "xmlid": "accrual_plan_probation_slow_start",
            "name": "ALLNETWORKS Probation Slow-Start Accrual",
            "time_off_type": "annual",
            "can_be_carryover": True,
            "carryover_date": "allocation",
            "transition_mode": "immediately",
            "accrued_gain_time": "end",
            "is_based_on_worked_time": False,
            "levels": [
                {"xmlid": "accrual_level_probation_after_3_months", "milestone_date": "after", "start_count": 3, "start_type": "month", "added_value": 1.25, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 15, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 3},
                {"xmlid": "accrual_level_probation_after_1_year", "milestone_date": "after", "start_count": 1, "start_type": "year", "added_value": 1.5, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 21, "action_with_unused_accruals": "all", "carryover_options": "limited", "postpone_max_days": 5},
            ],
        },
        {
            "xmlid": "accrual_plan_intern_fixed_term",
            "name": "ALLNETWORKS Intern Fixed-Term Accrual",
            "time_off_type": "casual",
            "can_be_carryover": False,
            "transition_mode": "immediately",
            "accrued_gain_time": "start",
            "is_based_on_worked_time": False,
            "levels": [
                {"xmlid": "accrual_level_intern_monthly", "milestone_date": "creation", "start_count": 0, "start_type": "day", "added_value": 0.5, "frequency": "monthly", "cap_accrued_time": True, "maximum_leave": 6, "action_with_unused_accruals": "lost"},
            ],
        },
    ]

    plans = {}
    for plan_def in plan_defs:
        existing = _xmlid_record(env, plan_def["xmlid"])
        if existing:
            plans[plan_def["xmlid"]] = existing
            continue
        plan = Plan.create(
            {
                "name": plan_def["name"],
                "company_id": company.id,
                "time_off_type_id": leave_types[plan_def["time_off_type"]].id,
                "can_be_carryover": plan_def["can_be_carryover"],
                "carryover_date": plan_def.get("carryover_date", "year_start"),
                "transition_mode": plan_def["transition_mode"],
                "accrued_gain_time": plan_def["accrued_gain_time"],
                "is_based_on_worked_time": plan_def["is_based_on_worked_time"],
            }
        )
        _register_xmlid(env, plan, plan_def["xmlid"])
        for level_def in plan_def["levels"]:
            level_xmlid = level_def["xmlid"]
            level_values = {key: value for key, value in level_def.items() if key != "xmlid"}
            _create_level(plan, level_xmlid, level_values)
        plans[plan_def["xmlid"]] = plan
    return plans


def _create_accrual_allocations(env, employees, leave_types, accrual_plans):
    Allocation = env["hr.leave.allocation"].sudo()
    assignments = [
        ("accrual_plan_annual_standard", "annual", "executive", 0, 4),
        ("accrual_plan_annual_standard", "annual", "finance", 0, 6),
        ("accrual_plan_annual_standard", "annual", "hr", 0, 5),
        ("accrual_plan_sick_monthly", "sick", "support", 0, 6),
        ("accrual_plan_sick_monthly", "sick", "sales", 0, 6),
        ("accrual_plan_hourly_worked_time", "annual", "warehouse", 0, 10),
        ("accrual_plan_hourly_worked_time", "annual", "operations", 4, 11),
        ("accrual_plan_probation_slow_start", "annual", "sales", 6, 12),
        ("accrual_plan_probation_slow_start", "annual", "support", 6, 12),
        ("accrual_plan_intern_fixed_term", "casual", "temporary", 0, 3),
    ]
    counter = 0
    for plan_xmlid, leave_key, dept_key, start, end in assignments:
        plan = accrual_plans.get(plan_xmlid)
        if not plan:
            continue
        for employee in employees.get(dept_key, [])[start:end]:
            if not employee.active:
                continue
            xmlid = f"allocation_{plan_xmlid}_{counter:03d}"
            if _xmlid_record(env, xmlid):
                counter += 1
                continue
            allocation = Allocation.create(
                {
                    "name": f"{plan.name} - {employee.name}",
                    "employee_id": employee.id,
                    "holiday_status_id": leave_types[leave_key].id,
                    "allocation_type": "accrual",
                    "accrual_plan_id": plan.id,
                    "number_of_days": 0,
                    "date_from": employee.contract_date_start or fields.Date.today().replace(day=1),
                }
            )
            env.cr.execute("UPDATE hr_leave_allocation SET state = %s WHERE id = %s", ("validate", allocation.id))
            allocation.invalidate_recordset(["state"])
            _register_xmlid(env, allocation, xmlid)
            counter += 1


def _create_payroll(env, company, employees, structures):
    batches = []
    all_employees = [emp for dept_employees in employees.values() for emp in dept_employees]
    monthly_employees = [emp for emp in all_employees if emp.structure_type_id != structures["biweekly"]]
    biweekly_employees = [emp for emp in all_employees if emp.structure_type_id == structures["biweekly"]]
    input_types = structures["inputs"]
    for months_back in (2, 1, 0):
        start = fields.Date.today().replace(day=1) - relativedelta(months=months_back)
        end = start + relativedelta(months=1, days=-1)
        batch = env["hr.payslip.run"].create(
            {
                "name": f"ALLNETWORKS Monthly Payroll {start.strftime('%b %Y')}",
                "date_start": start,
                "date_end": end,
                "structure_id": structures["regular"].id,
                "company_id": company.id,
            }
        )
        _register_xmlid(env, batch, f"payroll_batch_monthly_{months_back}")
        slips = env["hr.payslip"]
        for index, employee in enumerate(monthly_employees):
            slip = env["hr.payslip"].create(
                {
                    "name": f"Payslip - {employee.name} - {start.strftime('%b %Y')}",
                    "employee_id": employee.id,
                    "date_from": start,
                    "date_to": end,
                    "payslip_run_id": batch.id,
                    "company_id": company.id,
                    "struct_id": structures["regular"].id,
                }
            )
            slips |= slip
            _register_xmlid(env, slip, f"payslip_{months_back}_{index:02d}")
            slip._compute_input_line_ids()
            amounts = {
                "HOUSING": employee.wage * 0.18,
                "TRANSPORT": 175,
                "OVERTIME": 250 if index % 6 == 0 else 0,
                "BONUS": 500 if index % 14 == 0 else 0,
                "COMMISSION": 700 if employee.department_id.name == "Sales" and index % 3 == 0 else 0,
                "LOAN": 150 if index % 10 == 0 else 0,
                "ABSENCE": 125 if index % 12 == 0 else 0,
                "RETRO": 300 if months_back == 0 and index % 19 == 0 else 0,
            }
            for line in slip.input_line_ids:
                if line.code in amounts:
                    line.amount = amounts[line.code]
        slips.compute_sheet()
        batches.append(batch)

    start = fields.Date.today().replace(day=1)
    biweekly = env["hr.payslip.run"].create(
        {
            "name": "ALLNETWORKS Bi-weekly Operations Payroll",
            "date_start": start,
            "date_end": start + relativedelta(days=13),
            "structure_id": structures["worker"].id,
            "schedule_pay": "bi-weekly",
            "company_id": company.id,
        }
    )
    _register_xmlid(env, biweekly, "payroll_batch_biweekly_operations")
    slips = env["hr.payslip"]
    for index, employee in enumerate(biweekly_employees):
        slip = env["hr.payslip"].create(
            {
                "name": f"Payslip - {employee.name} - Bi-weekly {start.strftime('%d %b %Y')}",
                "employee_id": employee.id,
                "date_from": start,
                "date_to": start + relativedelta(days=13),
                "payslip_run_id": biweekly.id,
                "company_id": company.id,
                "struct_id": structures["worker"].id,
            }
        )
        slips |= slip
        _register_xmlid(env, slip, f"payslip_biweekly_{index:02d}")
        slip._compute_input_line_ids()
        amounts = {
            "HOUSING": 0,
            "TRANSPORT": 85,
            "OVERTIME": 180 if index % 3 == 0 else 0,
            "BONUS": 200 if index % 11 == 0 else 0,
            "COMMISSION": 0,
            "LOAN": 75 if index % 8 == 0 else 0,
            "ABSENCE": 95 if index % 7 == 0 else 0,
            "RETRO": 150 if index % 13 == 0 else 0,
        }
        for line in slip.input_line_ids:
            if line.code in amounts:
                line.amount = amounts[line.code]
    slips.compute_sheet()
    batches.append(biweekly)
    return batches


def _create_sporadic_employee_scenarios(env, company, employees, categories, batches):
    """Mark selected employees with one-off payroll scenarios and update their current payslips."""
    scenario_defs = [
        ("sales", 3, "sporadic_commission", "COMMISSION", 1450.0, "Sporadic commission payout for a large enterprise deal."),
        ("sales", 8, "sporadic_bonus", "BONUS", 900.0, "Quarter-end discretionary bonus for top sales performance."),
        ("support", 5, "sporadic_overtime", "OVERTIME", 420.0, "Emergency customer coverage overtime after a service outage."),
        ("operations", 6, "sporadic_overtime", "OVERTIME", 510.0, "Field callout overtime for weekend installation support."),
        ("operations", 9, "sporadic_allowance", "TRANSPORT", 280.0, "Temporary transport allowance for offsite project deployment."),
        ("warehouse", 4, "sporadic_overtime", "OVERTIME", 390.0, "Peak stock-count overtime for warehouse operations."),
        ("warehouse", 10, "sporadic_deduction", "ABSENCE", 160.0, "One-off unpaid absence correction before payroll close."),
        ("finance", 4, "sporadic_retro", "RETRO", 650.0, "Retroactive salary adjustment after delayed promotion approval."),
        ("hr", 2, "sporadic_bonus", "BONUS", 750.0, "Retention bonus for critical payroll implementation support."),
        ("it", 3, "sporadic_allowance", "TRANSPORT", 300.0, "Temporary remote-work equipment allowance paid through payroll."),
        ("temporary", 1, "sporadic_final_payoff", "RETRO", 480.0, "Final internship payoff including accrued balance correction."),
        ("executive", 2, "sporadic_deduction", "LOAN", 1000.0, "Executive salary advance recovery as a one-off deduction."),
    ]
    current_start = fields.Date.today().replace(day=1)
    scenario_model = env["hr.payroll.demo.scenario"]

    for index, (dept_key, employee_index, category_key, input_code, amount, description) in enumerate(scenario_defs, start=1):
        dept_employees = employees.get(dept_key, [])
        if employee_index >= len(dept_employees):
            continue
        employee = dept_employees[employee_index]
        category = categories.get(category_key)
        if category:
            employee.category_ids = [Command.link(category.id)]

        slip = env["hr.payslip"].search(
            [
                ("employee_id", "=", employee.id),
                ("company_id", "=", company.id),
                ("date_from", ">=", current_start),
            ],
            order="date_from desc, id desc",
            limit=1,
        )
        if slip:
            slip._compute_input_line_ids()
            target_line = slip.input_line_ids.filtered(lambda line: line.code == input_code)[:1]
            if target_line:
                target_line.amount = amount
            else:
                input_type = env["hr.payslip.input.type"].search([("code", "=", input_code)], limit=1)
                if input_type:
                    target_line = env["hr.payslip.input"].create(
                        {
                            "name": input_type.name,
                            "payslip_id": slip.id,
                            "input_type_id": input_type.id,
                            "amount": amount,
                        }
                    )
                    slip.invalidate_recordset(["input_line_ids"])
                    target_line.invalidate_recordset(["amount"])
                    target_line.flush_recordset()
            if target_line:
                slip.compute_sheet()

        if not _xmlid_record(env, f"scenario_sporadic_{index:02d}"):
            scenario = scenario_model.create(
                {
                    "sequence": 40 + index,
                    "name": f"Sporadic - {employee.name} - {input_code}",
                    "scenario_type": "payroll",
                    "employee_id": employee.id,
                    "department_id": employee.department_id.id,
                    "description": description,
                    "speaker_note": (
                        f"Open {employee.name}'s current payslip and review the {input_code} input line "
                        "to demonstrate one-off sporadic payroll handling."
                    ),
                    "status": "ready",
                }
            )
            _register_xmlid(env, scenario, f"scenario_sporadic_{index:02d}")


def _create_bank_transfers(env, company, batches):
    transfers = []
    for index, batch in enumerate(batches[:3]):
        transfer = env["hr.payroll.demo.bank.transfer"].create(
            {
                "name": f"Salary Transfer {batch.name}",
                "company_id": company.id,
                "batch_id": batch.id,
            }
        )
        transfer.action_generate_from_batch()
        if index == 1 and transfer.line_ids:
            transfer.line_ids[-1].write({"status": "failed", "note": "Rejected by bank due to invalid account number; reissue required."})
        if index == 0:
            transfer.action_approve()
            transfer.action_send_to_bank()
            transfer.action_mark_reconciled()
        elif index == 1:
            transfer.action_approve()
        _register_xmlid(env, transfer, f"bank_transfer_{index}")
        transfers.append(transfer)
    return transfers


def _create_reports(env, company, departments, employees, batches, transfers):
    for dept_key, dept in departments.items():
        dept_employees = employees[dept_key]
        net_total = sum(emp.wage * 1.15 for emp in dept_employees)
        summary = env["hr.payroll.demo.department.summary"].create(
            {
                "company_id": company.id,
                "department_id": dept.id,
                "employee_count": len(dept_employees),
                "monthly_gross": sum(emp.wage for emp in dept_employees),
                "monthly_net": net_total,
                "overtime_hours": 18 + len(dept_employees) * 1.5,
                "attendance_violation_count": len(dept_employees) // 2,
                "pending_leave_count": len(dept_employees) % 3,
                "bank_transfer_amount": net_total,
                "payroll_risk_note": "Review overtime and missing checkout alerts before final approval.",
            }
        )
        _register_xmlid(env, summary, f"summary_{dept_key}")
    for idx, transfer in enumerate(transfers):
        rec = env["hr.payroll.demo.reconciliation"].create(
            {
                "name": f"Payroll Reconciliation {transfer.name}",
                "company_id": company.id,
                "payslip_run_id": transfer.batch_id.id,
                "bank_transfer_id": transfer.id,
                "payroll_total": transfer.total_amount,
                "bank_statement_total": transfer.total_amount if idx != 1 else transfer.total_amount - 150,
                "difference": 0 if idx != 1 else 150,
                "state": "matched" if idx != 1 else "exception",
                "note": "Demo reconciliation case for management reporting.",
            }
        )
        _register_xmlid(env, rec, f"reconciliation_{idx}")


def _create_mass_operations(env, company, departments):
    today = fields.Date.today()
    month_start = today.replace(day=1)
    month_end = month_start + relativedelta(months=1, days=-1)
    operation_defs = [
        (
            "Demo - Generate Current Monthly Payslips",
            "generate_payslips",
            "finance",
            "Ready example for generating monthly payroll in bulk.",
        ),
        (
            "Demo - Validate Clean Payslips",
            "approve_payslips",
            "hr",
            "Ready example for batch validation with exception handling.",
        ),
        (
            "Demo - Fix Attendance Clock Outage",
            "attendance_adjustment",
            "warehouse",
            "Ready example for mass attendance correction.",
        ),
        (
            "Demo - Bulk Approve Pending Leaves",
            "approve_leaves",
            "support",
            "Ready example for bulk time off approval.",
        ),
    ]
    for index, (name, operation_type, dept_key, summary) in enumerate(operation_defs, start=1):
        operation = env["hr.payroll.demo.mass.operation"].create(
            {
                "name": name,
                "operation_type": operation_type,
                "department_id": departments[dept_key].id,
                "company_id": company.id,
                "date_from": month_start,
                "date_to": month_end,
                "result_summary": summary,
            }
        )
        _register_xmlid(env, operation, f"mass_operation_seed_{index:02d}")


def _create_scenarios(env, employees, departments):
    scenario_data = [
        ("New hire onboarding before payroll cutoff", "payroll", "Employee profile, contract, schedule and bank account are created before payroll."),
        ("New hire mid-month proration", "payroll", "New joiner has short-period payroll and contract start date."),
        ("Employee category change", "payroll", "Temporary employee is converted to full-time hourly payroll."),
        ("Department transfer", "reporting", "Employee cost moves from Customer Support to Sales through department and analytic reporting."),
        ("Promotion and salary increment", "payroll", "Increment scenario reflected through employee wage/version data."),
        ("Contract renewal", "payroll", "Fixed-term contract renewal scenario in employee version."),
        ("Resignation and final payoff", "payroll", "Inactive employee retained for final settlement demo."),
        ("Termination with deductions", "payroll", "Final payment includes unpaid absence and company deduction."),
        ("Standard monthly payroll", "payroll", "Standard monthly payroll for salaried employees."),
        ("Bi-weekly warehouse payroll", "payroll", "Warehouse and hourly teams are processed in a separate bi-weekly run."),
        ("Overtime approval and payment", "attendance", "Approved overtime increases pay for operations and warehouse employees."),
        ("Weekend work", "attendance", "Weekend attendance creates overtime or premium pay."),
        ("Night shift attendance", "attendance", "Warehouse night shift crosses midnight and is still paid correctly."),
        ("Late check-in penalty", "attendance", "Late check-ins create review alerts and optional penalties."),
        ("Missing checkout correction", "attendance", "Manager corrects missing checkout before payroll cutoff."),
        ("Remote work attendance", "attendance", "Hybrid employee works remotely without payroll penalty."),
        ("Approved annual leave", "leave", "Approved annual leave does not reduce net pay."),
        ("Sick leave during payroll month", "leave", "Sick leave is reflected in Time Off and payroll."),
        ("Unpaid leave deduction", "leave", "Unpaid leave flows into payroll as a deduction scenario."),
        ("Leave request refused due to business need", "leave", "Refused request has audit trail and no payroll effect."),
        ("Pending leave before payroll cutoff", "leave", "Pending request appears as a payroll control item."),
        ("Employee loan installment", "payroll", "Recurring loan deduction on payslip input lines."),
        ("Salary advance recovery", "payroll", "Advance deduction reduces net salary and clears finance balance."),
        ("Sales commission payroll", "payroll", "Sales commission scenario for field sales employees."),
        ("Performance bonus", "payroll", "One-off bonus included in current period payroll."),
        ("Expense reimbursement coordination", "accounting", "Expense reimbursement is tracked separately from payroll salary."),
        ("Payroll correction after validation", "payroll", "Payslip correction/review scenario after validation."),
        ("Retroactive salary adjustment", "payroll", "Retroactive pay input corrects prior salary change."),
        ("Payroll batch validation with exceptions", "mass", "Clean payslips validate while exception payslips remain for correction."),
        ("Mass attendance adjustment", "mass", "Bulk attendance correction handles a time clock outage."),
        ("Bulk leave approval", "mass", "Pending leaves are approved through one mass operation."),
        ("Multi-department payroll batch", "mass", "Batch payroll covers all departments with filtering available."),
        ("Payroll journal entry posting", "accounting", "Salary expense and payroll liabilities are posted to accounting."),
        ("Multi-bank salary transfer", "banking", "Employee salary payments are grouped for bank handoff."),
        ("Cash payment exception", "banking", "Employee without bank-ready payment is tracked as manual exception."),
        ("Bank reconciliation of salary payments", "accounting", "Salary payable is matched against bank statement payment."),
        ("Rejected bank payment", "banking", "Rejected employee bank payment requires correction and reissue."),
        ("Payroll accrual at month end", "accounting", "Payroll expense is accrued before salary payment date."),
        ("Department payroll budget review", "reporting", "Management report summarizes gross, net, overtime and risks."),
        ("Payroll audit and security review", "reporting", "HR, Payroll, Finance and manager permissions are separated."),
    ]
    all_employees = [emp for dept_employees in employees.values() for emp in dept_employees]
    departments_list = list(departments.values())
    for index, (name, scenario_type, description) in enumerate(scenario_data, start=1):
        scenario = env["hr.payroll.demo.scenario"].create(
            {
                "sequence": index,
                "name": name,
                "scenario_type": scenario_type,
                "employee_id": all_employees[index % len(all_employees)].id,
                "department_id": departments_list[index % len(departments_list)].id,
                "description": description,
                "speaker_note": f"Use this scenario to explain {name.lower()} in a realistic payroll operation.",
                "status": "ready",
            }
        )
        _register_xmlid(env, scenario, f"scenario_{index:02d}")


# ── Certifications & Skills ──────────────────────────────────────────────────

def _create_certifications(env, employees):
    """Seed hr.resume.line (certifications) and hr.employee.skill for key employees."""
    today = fields.Date.today()

    # ── Resume line types ────────────────────────────────────────────────────
    ResLineType = env["hr.resume.line.type"]
    def _get_or_create_line_type(name):
        lt = ResLineType.search([("name", "=", name)], limit=1)
        return lt or ResLineType.create({"name": name})

    cert_type = _get_or_create_line_type("Certification")
    exp_type = _get_or_create_line_type("Experience")
    edu_type = _get_or_create_line_type("Education")

    # ── Skill setup ─────────────────────────────────────────────────────────
    SkillType = env["hr.skill.type"]
    Skill = env["hr.skill"]
    SkillLevel = env["hr.skill.level"]
    EmpSkill = env["hr.employee.skill"]

    SKILL_DEFS = {
        "HR & Payroll": {
            "skills": ["Payroll Processing", "Labor Law", "HRIS / Odoo HR", "Employee Relations", "Recruitment"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Advanced", 75), ("Expert", 100)],
        },
        "Finance & Accounting": {
            "skills": ["Bookkeeping", "Tax Compliance", "Bank Reconciliation", "Financial Reporting", "Accounts Payable"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Advanced", 75), ("Expert", 100)],
        },
        "Sales & CRM": {
            "skills": ["CRM Systems", "Negotiation", "Territory Management", "Customer Acquisition", "Sales Reporting"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Proficient", 75), ("Expert", 100)],
        },
        "Customer Support": {
            "skills": ["Conflict Resolution", "Ticketing Systems", "Product Knowledge", "Communication", "SLA Management"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Proficient", 75), ("Expert", 100)],
        },
        "IT & Systems": {
            "skills": ["Network Administration", "Cybersecurity", "Help Desk Support", "ERP Administration", "Cloud Services"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Advanced", 75), ("Expert", 100)],
        },
        "Warehouse & Logistics": {
            "skills": ["Forklift Operation", "Inventory Management", "Shipping & Receiving", "Warehouse Safety", "Stock Counting"],
            "levels": [("Trainee", 20), ("Certified", 50), ("Experienced", 75), ("Senior", 100)],
        },
        "Operations": {
            "skills": ["Project Coordination", "Field Operations", "Dispatching", "Health & Safety", "Process Improvement"],
            "levels": [("Beginner", 25), ("Intermediate", 50), ("Advanced", 75), ("Expert", 100)],
        },
    }

    # Map each department key to a skill type name
    DEPT_SKILL_MAP = {
        "hr": "HR & Payroll",
        "finance": "Finance & Accounting",
        "sales": "Sales & CRM",
        "support": "Customer Support",
        "it": "IT & Systems",
        "warehouse": "Warehouse & Logistics",
        "operations": "Operations",
        "executive": "HR & Payroll",
        "temporary": "HR & Payroll",
    }

    # Create skill types, skills and levels
    skill_type_cache = {}
    skill_cache = {}
    skill_level_cache = {}

    for type_name, defn in SKILL_DEFS.items():
        stype = SkillType.search([("name", "=", type_name)], limit=1)
        if not stype:
            stype = SkillType.create({"name": type_name})
        skill_type_cache[type_name] = stype

        for lvl_name, progress in defn["levels"]:
            key = (stype.id, lvl_name)
            sl = SkillLevel.search([("skill_type_id", "=", stype.id), ("name", "=", lvl_name)], limit=1)
            if not sl:
                sl = SkillLevel.create({"name": lvl_name, "skill_type_id": stype.id, "level_progress": progress})
            skill_level_cache[key] = sl

        for sk_name in defn["skills"]:
            key = (stype.id, sk_name)
            sk = Skill.search([("skill_type_id", "=", stype.id), ("name", "=", sk_name)], limit=1)
            if not sk:
                sk = Skill.create({"name": sk_name, "skill_type_id": stype.id})
            skill_cache[key] = sk

    # ── Certification resume lines per key employee ──────────────────────────
    DEPT_CERTIFICATIONS = {
        "hr": [
            ("SHRM Certified Professional (SHRM-CP)", today.replace(year=today.year - 1), "Awarded by SHRM Institute"),
            ("Odoo HR & Payroll Certification", today.replace(year=today.year - 1, month=6, day=1), "Odoo Official Certification"),
            ("Payroll Compliance Certificate", today.replace(year=today.year - 2), "Caribbean Payroll Association"),
        ],
        "finance": [
            ("ACCA Part-Qualified", today.replace(year=today.year - 2), "ACCA Global"),
            ("Tax Compliance Specialist", today.replace(year=today.year - 1), "Regional Tax Authority"),
            ("Anti-Money Laundering (AML) Certificate", today.replace(year=today.year - 1, month=3, day=1), "CARICOM Financial Intelligence"),
        ],
        "sales": [
            ("Certified Sales Professional (CSP)", today.replace(year=today.year - 1), "Sales Institute"),
            ("CRM Systems Certification", today.replace(year=today.year - 1, month=8, day=1), "Odoo Certified Partner"),
        ],
        "support": [
            ("Customer Experience Management Certificate", today.replace(year=today.year - 1), "CCXP Board"),
            ("ITIL Foundation", today.replace(year=today.year - 2), "Axelos"),
        ],
        "it": [
            ("CompTIA Security+", today.replace(year=today.year - 1), "CompTIA"),
            ("Odoo Technical Certification", today.replace(year=today.year - 1, month=5, day=1), "Odoo SA"),
            ("AWS Cloud Practitioner", today.replace(year=today.year - 2), "Amazon Web Services"),
        ],
        "warehouse": [
            ("Forklift Operator Licence", today.replace(year=today.year - 1), "National Safety Council"),
            ("Warehouse Safety Level 2", today.replace(year=today.year - 1, month=4, day=1), "OSHA Caribbean"),
            ("First Aid & CPR", today.replace(year=today.year - 1, month=2, day=1), "Red Cross"),
        ],
        "operations": [
            ("Health & Safety Officer Certificate", today.replace(year=today.year - 1), "NEBOSH"),
            ("Project Management Fundamentals", today.replace(year=today.year - 2), "PMI"),
            ("First Aid & CPR", today.replace(year=today.year - 1, month=2, day=1), "Red Cross"),
        ],
        "executive": [
            ("Executive Leadership Programme", today.replace(year=today.year - 2), "UWI School of Business"),
            ("Anti-Money Laundering (AML) Certificate", today.replace(year=today.year - 1, month=3, day=1), "CARICOM Financial Intelligence"),
        ],
        "temporary": [
            ("Workplace Induction Certificate", today.replace(year=today.year - 1), "ALLNETWORKS Internal"),
        ],
    }

    cert_idx = 0
    for dept_key, emp_list in employees.items():
        certs = DEPT_CERTIFICATIONS.get(dept_key, [])
        stype_name = DEPT_SKILL_MAP.get(dept_key, "HR & Payroll")
        stype = skill_type_cache[stype_name]
        levels = list(skill_level_cache.keys())
        dept_skill_keys = [(stype.id, sn) for sn in SKILL_DEFS[stype_name]["skills"]]
        dept_levels = [skill_level_cache[k] for k in skill_level_cache if k[0] == stype.id]

        for emp_idx, emp in enumerate(emp_list):
            # Certification resume line (first 3 employees per dept get certifications)
            cert = certs[emp_idx % len(certs)] if certs else None
            if cert and emp_idx < min(4, len(emp_list)):
                cert_name, cert_date, cert_issuer = cert
                env["hr.resume.line"].create({
                    "employee_id": emp.id,
                    "name": cert_name,
                    "date_start": cert_date,
                    "date_end": cert_date.replace(year=cert_date.year + 2),
                    "description": f"Issued by {cert_issuer}",
                    "line_type_id": cert_type.id,
                })
                cert_idx += 1

            # Assign 2 skills per employee
            if dept_skill_keys:
                chosen_skills = [dept_skill_keys[emp_idx % len(dept_skill_keys)],
                                 dept_skill_keys[(emp_idx + 1) % len(dept_skill_keys)]]
                for sk_key in chosen_skills:
                    if sk_key not in skill_cache:
                        continue
                    sk = skill_cache[sk_key]
                    lvl_idx = min(emp_idx // 3, len(dept_levels) - 1)
                    sl = dept_levels[lvl_idx] if dept_levels else None
                    if sl and not EmpSkill.search([("employee_id", "=", emp.id), ("skill_id", "=", sk.id)], limit=1):
                        EmpSkill.create({
                            "employee_id": emp.id,
                            "skill_type_id": stype.id,
                            "skill_id": sk.id,
                            "skill_level_id": sl.id,
                        })


# ── Training Sessions ────────────────────────────────────────────────────────

def _create_training_sessions(env, company, employees, departments):
    """Seed realistic training sessions with attendance records."""
    today = fields.Date.today()
    Training = env["hr.payroll.demo.training"]
    Attendance = env["hr.payroll.demo.training.attendance"]

    all_employees = {k: v for k, v in employees.items()}

    def emp(dept, start=0, end=None):
        lst = all_employees.get(dept, [])
        return lst[start:end] if end else lst[start:]

    def months_ago(n, day=10):
        d = today - relativedelta(months=n)
        return d.replace(day=day)

    SESSIONS = [
        {
            "name": "Company Induction & Culture Orientation",
            "training_type": "induction",
            "trainer_name": "HR Team",
            "date_start": months_ago(3, 3),
            "date_end": months_ago(3, 4),
            "duration_hours": 16.0,
            "location": "ALLNETWORKS Head Office – Conference Room A",
            "max_participants": 30,
            "state": "completed",
            "notes": "Covers company history, values, HR policies, benefits, and Odoo system access.",
            "dept_participants": [
                ("hr", 0, 3), ("finance", 0, 3), ("sales", 0, 4),
                ("support", 0, 4), ("temporary", 0, 3),
            ],
            "pass_rate_hint": 0.95,
            "cert_issued": False,
            "xmlid": "training_induction_q1",
        },
        {
            "name": "Workplace Safety & Compliance Workshop",
            "training_type": "safety",
            "trainer_name": "Marcus Clarke – Safety Officer",
            "date_start": months_ago(3, 8),
            "date_end": months_ago(3, 8),
            "duration_hours": 8.0,
            "location": "Warehouse Training Bay",
            "max_participants": 25,
            "state": "completed",
            "notes": "OSHA requirements, fire safety, hazard reporting, and PPE usage.",
            "dept_participants": [
                ("warehouse", 0, 8), ("operations", 0, 5), ("it", 0, 2),
            ],
            "pass_rate_hint": 0.88,
            "cert_issued": True,
            "xmlid": "training_safety_q1",
        },
        {
            "name": "Anti-Money Laundering (AML) Compliance Briefing",
            "training_type": "safety",
            "trainer_name": "Priya Singh – Compliance Officer",
            "date_start": months_ago(3, 15),
            "date_end": months_ago(3, 15),
            "duration_hours": 4.0,
            "location": "Executive Boardroom",
            "max_participants": 20,
            "state": "completed",
            "notes": "Mandatory annual AML compliance refresher for finance and executive staff.",
            "dept_participants": [
                ("finance", 0, 6), ("executive", 0, 4),
            ],
            "pass_rate_hint": 1.0,
            "cert_issued": True,
            "xmlid": "training_aml_q1",
        },
        {
            "name": "Odoo Payroll & HR System Training",
            "training_type": "hr_payroll",
            "trainer_name": "External Odoo Partner",
            "date_start": months_ago(2, 5),
            "date_end": months_ago(2, 7),
            "duration_hours": 24.0,
            "location": "IT Training Lab",
            "max_participants": 15,
            "state": "completed",
            "notes": "Deep-dive on payroll structures, leave management, attendance, and reporting in Odoo 19.",
            "dept_participants": [
                ("hr", 0, 6), ("finance", 0, 4), ("it", 0, 2),
            ],
            "pass_rate_hint": 0.83,
            "cert_issued": True,
            "xmlid": "training_odoo_payroll",
        },
        {
            "name": "Customer Service Excellence Programme",
            "training_type": "customer_service",
            "trainer_name": "Natalie Morgan – Support Manager",
            "date_start": months_ago(2, 12),
            "date_end": months_ago(2, 13),
            "duration_hours": 16.0,
            "location": "Support Hub – Training Room",
            "max_participants": 20,
            "state": "completed",
            "notes": "Active listening, escalation handling, SLA management, and NPS improvement.",
            "dept_participants": [
                ("support", 0, 10), ("sales", 0, 4),
            ],
            "pass_rate_hint": 0.92,
            "cert_issued": False,
            "xmlid": "training_customer_service",
        },
        {
            "name": "IT Security Awareness & Data Protection",
            "training_type": "it_digital",
            "trainer_name": "Omar Ali – IT Manager",
            "date_start": months_ago(2, 20),
            "date_end": months_ago(2, 20),
            "duration_hours": 6.0,
            "location": "IT Training Lab",
            "max_participants": 50,
            "state": "completed",
            "notes": "Password hygiene, phishing awareness, data classification, GDPR basics.",
            "dept_participants": [
                ("it", 0, 4), ("hr", 0, 4), ("finance", 0, 4),
                ("executive", 0, 3), ("sales", 0, 4),
            ],
            "pass_rate_hint": 0.87,
            "cert_issued": False,
            "xmlid": "training_it_security",
        },
        {
            "name": "Forklift Operator Recertification",
            "training_type": "certification_prep",
            "trainer_name": "National Safety Council – Certified Instructor",
            "date_start": months_ago(2, 25),
            "date_end": months_ago(2, 26),
            "duration_hours": 12.0,
            "location": "Warehouse Yard",
            "max_participants": 10,
            "state": "completed",
            "notes": "Recertification of active forklift operators. Certificate valid 3 years.",
            "dept_participants": [
                ("warehouse", 3, 8),
            ],
            "pass_rate_hint": 0.80,
            "cert_issued": True,
            "xmlid": "training_forklift_recert",
        },
        {
            "name": "First Aid & CPR Certification",
            "training_type": "certification_prep",
            "trainer_name": "Red Cross – Certified Trainer",
            "date_start": months_ago(1, 6),
            "date_end": months_ago(1, 6),
            "duration_hours": 8.0,
            "location": "ALLNETWORKS Head Office – Multi-Purpose Hall",
            "max_participants": 30,
            "state": "completed",
            "notes": "Basic first aid, CPR, AED use, and emergency response procedures.",
            "dept_participants": [
                ("operations", 0, 6), ("warehouse", 0, 5),
                ("hr", 0, 2), ("executive", 0, 2),
            ],
            "pass_rate_hint": 0.93,
            "cert_issued": True,
            "xmlid": "training_first_aid",
        },
        {
            "name": "Advanced Excel & Financial Reporting",
            "training_type": "technical",
            "trainer_name": "Devon Joseph – Finance Manager",
            "date_start": months_ago(1, 10),
            "date_end": months_ago(1, 11),
            "duration_hours": 14.0,
            "location": "Finance Office – Training Corner",
            "max_participants": 12,
            "state": "completed",
            "notes": "Pivot tables, VLOOKUP/XLOOKUP, payroll reconciliation templates, and dashboard charts.",
            "dept_participants": [
                ("finance", 0, 8), ("hr", 0, 3),
            ],
            "pass_rate_hint": 0.91,
            "cert_issued": False,
            "xmlid": "training_excel_finance",
        },
        {
            "name": "Leadership Development Workshop – Managers Cohort",
            "training_type": "leadership",
            "trainer_name": "UWI School of Business – Guest Faculty",
            "date_start": months_ago(1, 18),
            "date_end": months_ago(1, 20),
            "duration_hours": 24.0,
            "location": "Offsite – Hilton Barbados",
            "max_participants": 15,
            "state": "completed",
            "notes": "Covers situational leadership, performance conversations, coaching, and team motivation.",
            "dept_participants": [
                ("executive", 0, 3), ("hr", 0, 2), ("finance", 0, 2),
                ("sales", 0, 2), ("support", 0, 2), ("operations", 0, 2),
                ("warehouse", 0, 1), ("it", 0, 1),
            ],
            "pass_rate_hint": 1.0,
            "cert_issued": True,
            "xmlid": "training_leadership_mgmt",
        },
        {
            "name": "Sales Techniques & Objection Handling",
            "training_type": "soft_skills",
            "trainer_name": "Camila Ramirez – Sales Manager",
            "date_start": months_ago(1, 22),
            "date_end": months_ago(1, 22),
            "duration_hours": 8.0,
            "location": "Sales Floor – Meeting Room 2",
            "max_participants": 20,
            "state": "completed",
            "notes": "Prospecting, handling objections, closing techniques, and CRM pipeline hygiene.",
            "dept_participants": [
                ("sales", 0, 12),
            ],
            "pass_rate_hint": 0.90,
            "cert_issued": False,
            "xmlid": "training_sales_techniques",
        },
        {
            "name": "HR Professional Development – Employment Law Update",
            "training_type": "hr_payroll",
            "trainer_name": "Caribbean Labour Law Institute",
            "date_start": months_ago(0, 5),
            "date_end": months_ago(0, 5),
            "duration_hours": 6.0,
            "location": "ALLNETWORKS Head Office – Conference Room B",
            "max_participants": 10,
            "state": "ongoing",
            "notes": "2025 updates to employment regulations, termination procedures, and leave entitlements.",
            "dept_participants": [
                ("hr", 0, 6), ("executive", 0, 2),
            ],
            "pass_rate_hint": 0.0,
            "cert_issued": False,
            "xmlid": "training_hr_law_update",
        },
        {
            "name": "Warehouse Operations & Inventory Accuracy",
            "training_type": "technical",
            "trainer_name": "Leon Thomas – Warehouse Manager",
            "date_start": today + relativedelta(weeks=1),
            "date_end": today + relativedelta(weeks=1, days=1),
            "duration_hours": 12.0,
            "location": "Warehouse Training Bay",
            "max_participants": 15,
            "state": "planned",
            "notes": "Cycle counting, FIFO, barcode scanning, and Odoo inventory module overview.",
            "dept_participants": [
                ("warehouse", 0, 10),
            ],
            "pass_rate_hint": 0.0,
            "cert_issued": False,
            "xmlid": "training_warehouse_inventory",
        },
        {
            "name": "Performance Management & KPI Setting",
            "training_type": "leadership",
            "trainer_name": "HR Team",
            "date_start": today + relativedelta(weeks=2),
            "date_end": today + relativedelta(weeks=2, days=1),
            "duration_hours": 16.0,
            "location": "ALLNETWORKS Head Office – Conference Room A",
            "max_participants": 20,
            "state": "planned",
            "notes": "Goal setting using OKR/KPI frameworks, appraisal processes, and feedback conversations.",
            "dept_participants": [
                ("hr", 0, 4), ("executive", 0, 2), ("sales", 0, 3),
                ("support", 0, 3), ("operations", 0, 2),
            ],
            "state": "planned",
            "xmlid": "training_performance_mgmt",
        },
    ]

    import random
    rng = random.Random(42)

    for sess_def in SESSIONS:
        if _xmlid_record(env, sess_def["xmlid"]):
            continue

        session = Training.create({
            "name": sess_def["name"],
            "training_type": sess_def["training_type"],
            "trainer_name": sess_def.get("trainer_name", ""),
            "date_start": sess_def["date_start"],
            "date_end": sess_def["date_end"],
            "duration_hours": sess_def.get("duration_hours", 8.0),
            "location": sess_def.get("location", ""),
            "max_participants": sess_def.get("max_participants", 20),
            "state": sess_def["state"],
            "notes": sess_def.get("notes", ""),
            "company_id": company.id,
        })
        _register_xmlid(env, session, sess_def["xmlid"])

        # Build attendance list
        pass_rate = sess_def.get("pass_rate_hint", 0.85)
        cert_issued = sess_def.get("cert_issued", False)
        is_completed = sess_def["state"] == "completed"

        for dept_key, start_idx, end_idx in sess_def.get("dept_participants", []):
            dept_emps = all_employees.get(dept_key, [])
            selected = dept_emps[start_idx:end_idx]
            for att_idx, emp in enumerate(selected):
                # Determine status
                r = rng.random()
                if not is_completed:
                    status = "present"
                    score = 0.0
                    passed = False
                    issued = False
                elif r < 0.75:
                    status = "present"
                elif r < 0.85:
                    status = "late"
                elif r < 0.92:
                    status = "absent"
                else:
                    status = "excused"

                if is_completed:
                    attended = status in ("present", "late")
                    raw_score = rng.uniform(55, 99) if attended else 0.0
                    score = round(raw_score, 1)
                    passed = attended and (score >= 65) and (rng.random() < pass_rate)
                    issued = cert_issued and passed
                    cert_num = f"CERT-{session.id:04d}-{emp.id:04d}" if issued else ""
                else:
                    score = 0.0
                    passed = False
                    issued = False
                    cert_num = ""

                Attendance.create({
                    "training_id": session.id,
                    "employee_id": emp.id,
                    "attendance_status": status,
                    "score": score,
                    "passed": passed,
                    "certification_issued": issued,
                    "certificate_number": cert_num if cert_num else False,
                })


# ── Employee Expenses ────────────────────────────────────────────────────────

def _create_expenses(env, company, employees):
    """Seed realistic HR expenses with native hr.expense records and categories."""
    today = fields.Date.today()
    Expense = env["hr.expense"].with_company(company).sudo()

    def _product(xmlid, fallback_code=False):
        product = env.ref(xmlid, raise_if_not_found=False)
        if product:
            return product
        domain = [("can_be_expensed", "=", True)]
        if fallback_code:
            domain.append(("default_code", "=", fallback_code))
        return env["product.product"].search(domain, limit=1)

    products = {
        "meal": _product("hr_expense.expense_product_meal", "FOOD"),
        "travel": _product("hr_expense.expense_product_travel_accommodation", "TRANS & ACC"),
        "mileage": _product("hr_expense.expense_product_mileage", "MIL"),
        "gift": _product("hr_expense.expense_product_gift", "GIFT"),
        "communication": _product("hr_expense.expense_product_communication", "COMM"),
        "general": _product("hr_expense.product_product_no_cost", "EXP_GEN"),
    }

    def _employee(dept_key, index):
        dept_employees = employees.get(dept_key, [])
        return dept_employees[index] if index < len(dept_employees) else False

    def _set_state(expense, approval_state):
        if not approval_state:
            return
        manager_id = env.ref("base.user_admin").id
        env.cr.execute(
            """
            UPDATE hr_expense
               SET approval_state = %s,
                   approval_date = CASE WHEN %s = 'approved' THEN now() ELSE approval_date END,
                   manager_id = %s
             WHERE id = %s
            """,
            (approval_state, approval_state, manager_id, expense.id),
        )
        expense.invalidate_recordset(["approval_state", "approval_date", "manager_id", "state"])
        expense._compute_state()

    expense_defs = [
        ("expense_sales_airfare", "sales", 2, "travel", "Airfare - Trinidad enterprise prospect visit", 820.0, 1, "own_account", "submitted", 2),
        ("expense_sales_client_lunch", "sales", 4, "meal", "Client lunch - retail chain negotiation", 186.0, 1, "own_account", "approved", 1),
        ("expense_sales_customer_gift", "sales", 7, "gift", "Customer appreciation gift basket", 95.0, 1, "company_account", "submitted", 0),
        ("expense_support_phone", "support", 3, "communication", "Emergency support phone top-up", 42.0, 1, "own_account", "approved", 0),
        ("expense_support_team_meal", "support", 8, "meal", "Late shift meal during outage response", 128.0, 1, "company_account", "approved", 1),
        ("expense_operations_mileage", "operations", 4, "mileage", "Mileage - field installation route", 1.15, 148, "own_account", "submitted", 0),
        ("expense_operations_hotel", "operations", 7, "travel", "Hotel - overnight field deployment", 275.0, 1, "own_account", "approved", 1),
        ("expense_warehouse_safety_boots", "warehouse", 5, "general", "Safety boots reimbursement", 110.0, 1, "own_account", "draft", 0),
        ("expense_warehouse_forklift_training", "warehouse", 9, "general", "Forklift recertification fee", 240.0, 1, "company_account", "approved", 2),
        ("expense_it_cloud_lab", "it", 2, "general", "Cloud lab subscription for certification practice", 165.0, 1, "company_account", "approved", 0),
        ("expense_it_remote_internet", "it", 3, "communication", "Remote work internet reimbursement", 60.0, 1, "own_account", "submitted", 0),
        ("expense_hr_recruitment_ad", "hr", 3, "general", "Recruitment campaign posting fee", 135.0, 1, "company_account", "approved", 2),
        ("expense_hr_training_materials", "hr", 5, "general", "Training materials for onboarding cohort", 210.0, 1, "own_account", "approved", 1),
        ("expense_finance_tax_workshop", "finance", 2, "travel", "Taxi and registration - tax compliance workshop", 315.0, 1, "own_account", "submitted", 0),
        ("expense_finance_duplicate_receipt", "finance", 4, "meal", "Duplicate receipt review - vendor lunch", 78.0, 1, "own_account", "refused", 1),
        ("expense_executive_board_dinner", "executive", 1, "meal", "Board dinner after quarterly strategy review", 420.0, 1, "company_account", "approved", 1),
        ("expense_executive_airport_transfer", "executive", 3, "travel", "Airport transfer - regional partner meeting", 95.0, 1, "own_account", "submitted", 0),
        ("expense_temporary_training_transport", "temporary", 1, "travel", "Intern transport to training center", 38.0, 1, "own_account", "approved", 0),
    ]

    for sequence, (xmlid, dept_key, emp_index, product_key, name, unit_amount, quantity, payment_mode, approval_state, months_back) in enumerate(expense_defs, start=1):
        if _xmlid_record(env, xmlid):
            continue
        employee = _employee(dept_key, emp_index)
        product = products.get(product_key)
        if not employee or not product:
            continue
        expense_date = today - relativedelta(months=months_back, days=sequence % 9)
        expense = Expense.create(
            {
                "name": name,
                "employee_id": employee.id,
                "company_id": company.id,
                "product_id": product.id,
                "date": expense_date,
                "quantity": quantity,
                "total_amount_currency": unit_amount * quantity,
                "payment_mode": payment_mode,
                "description": (
                    f"Demo expense category: {product.display_name}. "
                    f"Scenario owner: {employee.department_id.name} / {employee.job_id.name}."
                ),
            }
        )
        _set_state(expense, approval_state if approval_state != "draft" else False)
        _register_xmlid(env, expense, xmlid)

        if not _xmlid_record(env, f"scenario_{xmlid}"):
            scenario = env["hr.payroll.demo.scenario"].create(
                {
                    "sequence": 70 + sequence,
                    "name": f"Expense - {employee.name} - {product.name}",
                    "scenario_type": "accounting",
                    "employee_id": employee.id,
                    "department_id": employee.department_id.id,
                    "description": (
                        f"{employee.name} submits {name.lower()} under the {product.name} expense category "
                        f"with payment mode '{payment_mode.replace('_', ' ')}'."
                    ),
                    "speaker_note": (
                        "Open the Employee Expenses menu and use this record to demonstrate category selection, "
                        "employee ownership, approval status, and accounting reimbursement flow."
                    ),
                    "status": "ready" if approval_state != "refused" else "optional",
                }
            )
            _register_xmlid(env, scenario, f"scenario_{xmlid}")


# ── HR / Payroll Accounting Entries ──────────────────────────────────────────

def _create_accounting_entries(env, company, employees, batches, transfers):
    """Create balanced demo journal entries that complete HR/payroll/accounting workflows."""
    Move = env["account.move"].with_company(company).sudo()
    Journal = env["account.journal"].with_company(company).sudo()
    Account = env["account.account"].with_company(company).sudo()
    today = fields.Date.today()
    month_start = today.replace(day=1)
    prefix = "ALLNETWORKS HR Accounting"

    def _account(xmlid, code, name, account_type, reconcile=False):
        existing = _xmlid_record(env, xmlid)
        if existing:
            return existing
        existing_code = Account.search([("code", "=", code), ("company_ids", "in", company.id)], limit=1)
        if existing_code:
            _register_xmlid(env, existing_code, xmlid)
            return existing_code
        account = Account.create(
            {
                "name": name,
                "code": code,
                "account_type": account_type,
                "company_ids": [Command.link(company.id)],
                "reconcile": reconcile,
            }
        )
        _register_xmlid(env, account, xmlid)
        return account

    accounts = {
        "salary_expense": _account("account_salary_expense", "610100", "Salaries and Wages Expense", "expense"),
        "overtime_expense": _account("account_overtime_expense", "610110", "Overtime and Shift Premium Expense", "expense"),
        "allowance_expense": _account("account_allowance_expense", "610120", "Payroll Allowances Expense", "expense"),
        "bonus_expense": _account("account_bonus_expense", "610130", "Bonus and Commission Expense", "expense"),
        "expense_reimbursement": _account("account_expense_reimbursement", "610200", "Employee Expense Reimbursements", "expense"),
        "leave_expense": _account("account_leave_expense", "610300", "Accrued Leave Expense", "expense"),
        "retro_expense": _account("account_retro_expense", "610400", "Retroactive Payroll Adjustment Expense", "expense"),
        "payroll_payable": _account("account_payroll_payable", "221100", "Payroll Payable", "liability_current", True),
        "employee_payable": _account("account_employee_expense_payable", "221200", "Employee Expense Payable", "liability_current", True),
        "leave_liability": _account("account_leave_liability", "221300", "Accrued Leave Liability", "liability_current", True),
        "rejected_payment": _account("account_rejected_salary_payment", "221400", "Rejected Salary Payments", "liability_current", True),
        "loan_receivable": _account("account_employee_loan_receivable", "132100", "Employee Loan Receivable", "asset_current", True),
        "payroll_clearing": _account("account_payroll_clearing_difference", "659900", "Payroll Clearing Difference", "expense_other"),
        "bank": _account("account_demo_salary_bank", "101900", "ALLNETWORKS Salary Bank Clearing", "asset_cash", True),
    }

    journal = env.ref(f"{MODULE}.journal_hr_payroll_accounting", raise_if_not_found=False)
    if not journal:
        journal = Journal.create(
            {
                "name": "ALLNETWORKS HR & Payroll Accounting",
                "code": "HRPAY",
                "type": "general",
                "company_id": company.id,
            }
        )
        _register_xmlid(env, journal, "journal_hr_payroll_accounting")

    bank_journal = env.ref(f"{MODULE}.journal_salary_bank", raise_if_not_found=False)
    if not bank_journal:
        bank_journal = Journal.create(
            {
                "name": "ALLNETWORKS Salary Bank",
                "code": "SALBK",
                "type": "bank",
                "company_id": company.id,
                "default_account_id": accounts["bank"].id,
            }
        )
        _register_xmlid(env, bank_journal, "journal_salary_bank")

    current_batch = batches[-1] if batches else env["hr.payslip.run"].search([("company_id", "=", company.id)], order="date_end desc", limit=1)
    current_slips = current_batch.slip_ids if current_batch else env["hr.payslip"].search([("company_id", "=", company.id)], limit=30)
    gross_total = sum(current_slips.mapped("gross_wage")) or sum(current_slips.mapped("basic_wage")) or 95000.0
    net_total = sum(current_slips.mapped("net_wage")) or (gross_total * 0.82)
    overtime_total = sum(
        line.amount
        for slip in current_slips
        for line in slip.input_line_ids
        if line.code == "OVERTIME"
    ) or 2200.0
    allowance_total = sum(
        line.amount
        for slip in current_slips
        for line in slip.input_line_ids
        if line.code in ("HOUSING", "TRANSPORT")
    ) or 4800.0
    bonus_total = sum(
        line.amount
        for slip in current_slips
        for line in slip.input_line_ids
        if line.code in ("BONUS", "COMMISSION")
    ) or 3500.0
    loan_total = sum(
        line.amount
        for slip in current_slips
        for line in slip.input_line_ids
        if line.code == "LOAN"
    ) or 1000.0
    retro_total = sum(
        line.amount
        for slip in current_slips
        for line in slip.input_line_ids
        if line.code == "RETRO"
    ) or 1130.0
    expense_total = sum(env["hr.expense"].search([("company_id", "=", company.id), ("payment_mode", "=", "own_account")]).mapped("total_amount")) or 2600.0
    company_expense_total = sum(env["hr.expense"].search([("company_id", "=", company.id), ("payment_mode", "=", "company_account")]).mapped("total_amount")) or 1800.0
    rejected_amount = 150.0
    leave_accrual_total = 4200.0

    def _line(account, label, debit=0.0, credit=0.0, partner=False):
        return Command.create(
            {
                "account_id": account.id,
                "name": label,
                "debit": round(debit, 2),
                "credit": round(credit, 2),
                "partner_id": partner.id if partner else False,
            }
        )

    def _move(xmlid, ref, date_value, lines, post=True, journal_record=False):
        existing = _xmlid_record(env, xmlid)
        if existing:
            return existing
        move = Move.create(
            {
                "move_type": "entry",
                "journal_id": (journal_record or journal).id,
                "company_id": company.id,
                "date": date_value,
                "ref": f"{prefix} - {ref}",
                "line_ids": lines,
            }
        )
        if post:
            move.action_post()
        _register_xmlid(env, move, xmlid)
        return move

    payroll_expenses = gross_total + overtime_total + allowance_total + bonus_total
    payroll_move = _move(
        "account_move_payroll_accrual",
        f"Monthly Payroll Accrual - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(days=24),
        [
            _line(accounts["salary_expense"], "Gross salaries", gross_total),
            _line(accounts["overtime_expense"], "Approved overtime and shift premiums", overtime_total),
            _line(accounts["allowance_expense"], "Housing and transport allowances", allowance_total),
            _line(accounts["bonus_expense"], "Sporadic bonuses and commissions", bonus_total),
            _line(accounts["loan_receivable"], "Employee loan recoveries", credit=loan_total),
            _line(accounts["payroll_payable"], "Net payroll payable", credit=payroll_expenses - loan_total),
        ],
    )

    salaries_journal = (
        env.ref("hr_payroll_account.hr_payroll_account_journal", raise_if_not_found=False)
        or Journal.search(
            [
                ("company_id", "=", company.id),
                "|",
                ("code", "=", "SLR"),
                ("name", "ilike", "Salaries"),
            ],
            limit=1,
        )
    )
    if salaries_journal:
        salaries_journal.show_on_dashboard = True
        _move(
            "account_move_salaries_dashboard_monthly",
            f"Salaries Dashboard - Monthly Payroll - {month_start.strftime('%b %Y')}",
            month_start + relativedelta(days=24),
            [
                _line(accounts["salary_expense"], "Monthly salaries posted to native Salaries journal", gross_total),
                _line(accounts["bonus_expense"], "Sporadic bonus and commission payroll lines", bonus_total),
                _line(accounts["overtime_expense"], "Overtime payroll lines", overtime_total),
                _line(accounts["payroll_payable"], "Payroll payable from Salaries journal", credit=gross_total + bonus_total + overtime_total),
            ],
            journal_record=salaries_journal,
        )
        _move(
            "account_move_salaries_dashboard_biweekly",
            "Salaries Dashboard - Bi-weekly Operations Payroll",
            month_start + relativedelta(days=13),
            [
                _line(accounts["salary_expense"], "Bi-weekly warehouse and operations wages", net_total * 0.28),
                _line(accounts["allowance_expense"], "Transport and field allowances", allowance_total * 0.35),
                _line(accounts["payroll_payable"], "Bi-weekly payroll payable", credit=(net_total * 0.28) + (allowance_total * 0.35)),
            ],
            journal_record=salaries_journal,
        )
        _move(
            "account_move_salaries_dashboard_sick_leave",
            "Salaries Dashboard - Paid Sick Leave Cost",
            month_start + relativedelta(days=16),
            [
                _line(accounts["leave_expense"], "Paid sick leave payroll cost", 1850.0),
                _line(accounts["payroll_payable"], "Sick leave payable through payroll", credit=1850.0),
            ],
            journal_record=salaries_journal,
        )
        _move(
            "account_move_salaries_dashboard_draft_adjustment",
            "Salaries Dashboard - Draft Payroll Adjustment Review",
            month_start + relativedelta(days=22),
            [
                _line(accounts["retro_expense"], "Draft retroactive payroll correction", 975.0),
                _line(accounts["payroll_payable"], "Draft payroll correction payable", credit=975.0),
            ],
            post=False,
            journal_record=salaries_journal,
        )

    salary_payment = _move(
        "account_move_salary_payment",
        f"Salary Bank Payment Batch - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(days=26),
        [
            _line(accounts["payroll_payable"], "Salary payment batch released", net_total),
            _line(accounts["bank"], "Bank salary transfer", credit=net_total),
        ],
        journal_record=bank_journal,
    )

    rejected_move = _move(
        "account_move_rejected_salary_payment",
        "Rejected Salary Payment - Reissue Required",
        month_start + relativedelta(days=27),
        [
            _line(accounts["rejected_payment"], "Rejected salary payment liability", rejected_amount),
            _line(accounts["bank"], "Returned bank payment", credit=rejected_amount),
        ],
        post=False,
        journal_record=bank_journal,
    )

    _move(
        "account_move_expense_reimbursements",
        f"Employee Expense Reimbursements - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(days=18),
        [
            _line(accounts["expense_reimbursement"], "Employee-paid travel, meals and communication claims", expense_total),
            _line(accounts["employee_payable"], "Employee reimbursement payable", credit=expense_total),
        ],
    )

    _move(
        "account_move_expense_reimbursement_payment",
        f"Employee Expense Payment - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(days=20),
        [
            _line(accounts["employee_payable"], "Expense reimbursements paid", expense_total),
            _line(accounts["bank"], "Bank payment to employees", credit=expense_total),
        ],
        journal_record=bank_journal,
    )

    _move(
        "account_move_company_paid_expenses",
        f"Company-paid HR Expenses - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(days=19),
        [
            _line(accounts["expense_reimbursement"], "Company-paid cards and direct expense charges", company_expense_total),
            _line(accounts["bank"], "Company card / bank clearing", credit=company_expense_total),
        ],
        journal_record=bank_journal,
    )

    _move(
        "account_move_leave_accrual_liability",
        f"Leave Accrual Liability - {month_start.strftime('%b %Y')}",
        month_start + relativedelta(months=1, days=-1),
        [
            _line(accounts["leave_expense"], "Earned leave accrual expense", leave_accrual_total),
            _line(accounts["leave_liability"], "Accrued leave liability", credit=leave_accrual_total),
        ],
    )

    _move(
        "account_move_salary_advance",
        "Employee Salary Advance",
        month_start + relativedelta(days=5),
        [
            _line(accounts["loan_receivable"], "Salary advance issued", 1200.0),
            _line(accounts["bank"], "Bank disbursement for salary advance", credit=1200.0),
        ],
        journal_record=bank_journal,
    )

    _move(
        "account_move_retro_adjustment",
        "Retroactive Payroll Adjustment",
        month_start + relativedelta(days=23),
        [
            _line(accounts["retro_expense"], "Retroactive pay and final payoff adjustment", retro_total),
            _line(accounts["payroll_payable"], "Retroactive amount due to employees", credit=retro_total),
        ],
    )

    _move(
        "account_move_reconciliation_difference",
        "Payroll Reconciliation Difference",
        month_start + relativedelta(days=28),
        [
            _line(accounts["payroll_clearing"], "Bank reconciliation shortage under review", 150.0),
            _line(accounts["bank"], "Unmatched payroll bank difference", credit=150.0),
        ],
        post=False,
        journal_record=bank_journal,
    )

    _move(
        "account_move_payroll_budget_review",
        "Draft Department Payroll Budget Review",
        month_start + relativedelta(days=15),
        [
            _line(accounts["salary_expense"], "Draft payroll budget variance review", 5000.0),
            _line(accounts["payroll_payable"], "Draft payroll budget accrual", credit=5000.0),
        ],
        post=False,
    )

    if transfers:
        transfers[0].write({"account_move_id": salary_payment.id, "bank_journal_id": bank_journal.id})

    scenario_defs = [
        ("scenario_accounting_payroll_accrual", "Payroll journal entry posting", "Monthly payroll costs are accrued before bank payment."),
        ("scenario_accounting_salary_payment", "Salary payment bank entry", "Payroll payable is cleared against the salary bank journal."),
        ("scenario_accounting_rejected_payment", "Rejected salary payment accounting", "Returned salary transfer stays open for reissue and review."),
        ("scenario_accounting_expense_reimbursement", "Employee expense reimbursement accounting", "Approved employee-paid expenses create payable and bank payment entries."),
        ("scenario_accounting_company_paid_expense", "Company-paid expense accounting", "Company card and direct-paid expenses clear directly against bank clearing."),
        ("scenario_accounting_leave_liability", "Leave accrual liability accounting", "Earned time off creates leave expense and liability."),
        ("scenario_accounting_salary_advance", "Employee salary advance accounting", "Salary advance is tracked as an employee receivable and recovered by payroll."),
        ("scenario_accounting_retro_adjustment", "Retroactive pay accounting", "Retro and final payoff inputs create separate payroll adjustment expense."),
        ("scenario_accounting_reconciliation_difference", "Payroll bank reconciliation difference", "A small bank difference remains draft as an accounting exception."),
        ("scenario_accounting_budget_review", "Draft payroll budget review", "Finance can compare draft department accruals before posting."),
    ]
    finance_employee = employees.get("finance", [False])[0] if employees.get("finance") else False
    finance_department = finance_employee.department_id if finance_employee else False
    for index, (xmlid, name, description) in enumerate(scenario_defs, start=1):
        if _xmlid_record(env, xmlid):
            continue
        scenario = env["hr.payroll.demo.scenario"].create(
            {
                "sequence": 90 + index,
                "name": name,
                "scenario_type": "accounting",
                "employee_id": finance_employee.id if finance_employee else False,
                "department_id": finance_department.id if finance_department else False,
                "description": description,
                "speaker_note": "Open Reports > Accounting Entries to show the related journal entry and explain the debit/credit flow.",
                "status": "ready",
            }
        )
        _register_xmlid(env, scenario, xmlid)


# -- Knowledge Base ------------------------------------------------------------

def _create_knowledge_base(env, company):
    """Create an employee-facing Knowledge handbook when Knowledge is installed."""
    if "knowledge.article" not in env.registry.models:
        return

    module_state = env["ir.module.module"].sudo().search([("name", "=", "knowledge")], limit=1).state
    if module_state != "installed":
        return

    Article = env["knowledge.article"].sudo()

    def _html(title, purpose, bullets, owner="People Operations", last_review="Quarterly"):
        bullet_html = "".join(f"<li>{escape(item)}</li>" for item in bullets)
        return f"""
            <div class="o_knowledge_demo_policy">
                <h1>{escape(title)}</h1>
                <p><strong>Purpose:</strong> {escape(purpose)}</p>
                <h2>What employees need to know</h2>
                <ul>{bullet_html}</ul>
                <h2>Who to contact</h2>
                <p>{escape(owner)} owns this page. Employees should ask their manager first for operational approval, then HR or Finance for policy interpretation.</p>
                <h2>Review rhythm</h2>
                <p>This demo policy is reviewed {escape(last_review)} and before every payroll close.</p>
            </div>
        """

    def _article(xmlid, name, body, parent=False, sequence=10, icon="📘", permission=False):
        existing = _xmlid_record(env, xmlid)
        admin = env.ref("base.user_admin", raise_if_not_found=False)
        values = {
            "name": name,
            "body": body,
            "parent_id": parent.id if parent else False,
            "sequence": sequence,
            "icon": icon,
            "full_width": True,
            "is_article_visible_by_everyone": True,
            "is_template": False,
        }
        if not parent:
            values["internal_permission"] = permission or "read"
            if admin and not existing:
                values["article_member_ids"] = [
                    Command.create({"partner_id": admin.partner_id.id, "permission": "write"})
                ]
        if existing:
            existing.write(values)
            return existing
        article = Article.create(values)
        _register_xmlid(env, article, xmlid)
        return article

    root = _article(
        "knowledge_root_employee_handbook",
        "ALLNETWORKS Employee Knowledge Base",
        _html(
            "ALLNETWORKS Employee Knowledge Base",
            "One searchable home for company policy, HR services, payroll questions, holidays, expenses, training, banking and accounting workflows.",
            [
                "Use this workspace before asking HR repetitive policy questions.",
                "Every article is written for employees, managers, payroll and finance users.",
                "Policies are connected to the demo data: employees, departments, attendance, leave, payroll, expenses, bank transfers and accounting entries.",
                "When a rule affects pay, the article explains which Odoo screen supports the workflow.",
                "For live demo navigation, open the related app screen after reading the policy.",
            ],
            "HR, Payroll and Finance",
        ),
        sequence=1,
        icon="🏢",
        permission="read",
    )

    sections = [
        (
            "knowledge_section_start_here",
            "Start Here - Employee Service Desk",
            "🧭",
            [
                ("knowledge_start_first_week", "Your First Week at ALLNETWORKS", "How new employees complete onboarding, verify profile data, attend induction and prepare for first payroll.", ["Confirm your work email, department, job, manager and work location.", "Check your bank account before payroll cutoff.", "Attend Company Induction and Culture Orientation.", "Review attendance expectations before your first working day.", "Ask HR to correct missing data immediately."]),
                ("knowledge_start_employee_self_service", "Employee Self-Service Guide", "Where employees go in Odoo to answer common questions without contacting HR.", ["Employees can check profile data, time off balances, payslips, expenses and training attendance.", "Use Knowledge search before opening an HR ticket.", "Managers should use department views for team questions.", "Payroll questions must include the payslip period and employee name.", "Finance questions must include expense or bank transfer reference."]),
                ("knowledge_start_who_to_ask", "Who to Ask for Help", "Routing rules for HR, payroll, attendance, expenses, banking, IT and manager approvals.", ["Manager: schedules, overtime approval, leave timing and department coverage.", "HR: contracts, personal data, job changes, training and policies.", "Payroll: payslip, deductions, allowances, commissions and retro adjustments.", "Finance: expenses, reimbursements, salary bank transfer and rejected payments.", "IT: login, access, security, device and remote work tools."]),
                ("knowledge_start_demo_map", "Odoo Screen Map for Employees", "A practical map of where each employee question is answered in Odoo.", ["Employees app stores profile, department, job and manager.", "Attendance app stores check-in, check-out and exceptions.", "Time Off app stores leave requests, approvals and balances.", "Payroll app stores payslips, work entries and salary rules.", "Expenses app stores employee claims and reimbursement status."]),
            ],
        ),
        (
            "knowledge_section_company_policy",
            "Company Policies and Handbook",
            "📚",
            [
                ("knowledge_policy_code_of_conduct", "Code of Conduct", "Expected behavior for all employees, contractors, interns and managers.", ["Act with professionalism, fairness and respect.", "Protect customer and employee information.", "Report conflicts of interest before decisions are made.", "Follow approval limits for expenses, overtime and payroll changes.", "Policy violations may affect disciplinary action and final settlement."]),
                ("knowledge_policy_workplace_respect", "Workplace Respect and Anti-Harassment", "How ALLNETWORKS keeps a respectful workplace across office, warehouse, field and remote teams.", ["Harassment, discrimination and retaliation are not tolerated.", "Employees can report concerns to manager, HR or compliance.", "Managers must escalate serious concerns immediately.", "Investigations are confidential and documented.", "Training attendance supports compliance evidence."]),
                ("knowledge_policy_disciplinary", "Disciplinary and Corrective Action Policy", "How attendance, conduct, safety and performance issues are handled.", ["Corrective action should be documented with facts and dates.", "Repeated late check-ins can lead to formal review.", "Safety violations in warehouse or field operations are escalated quickly.", "Payroll deductions require policy basis and payroll review.", "Final action is coordinated by HR and department management."]),
                ("knowledge_policy_documents", "Employee Document and Record Policy", "Rules for employee files, certificates, bank details and contract records.", ["HR owns employee master data and contract records.", "Employees must keep contact and bank details current.", "Certifications should be attached or recorded before regulated work.", "Only authorized users may view sensitive HR data.", "Corrections should be requested before payroll cutoff."]),
            ],
        ),
        (
            "knowledge_section_holidays_attendance",
            "Holidays, Working Time and Attendance",
            "🕒",
            [
                ("knowledge_holidays_calendar", "Company Holiday Calendar", "Holiday policy used for payroll and workforce planning in the demo quarter.", ["Public holidays are treated as paid non-working days for eligible employees.", "Warehouse and support teams may still require coverage during peak periods.", "Holiday work requires manager approval before payroll cutoff.", "Company holidays are reviewed by HR at the start of each quarter.", "Payroll checks public holidays before validating work entries."]),
                ("knowledge_attendance_checkin", "Check-In and Check-Out Rules", "Daily attendance rules for office, shift, field, warehouse and remote employees.", ["Employees must check in at the start of work and check out at the end.", "Missing check-outs create attendance alerts and must be corrected.", "Late check-ins may trigger coaching or payroll deduction depending on policy.", "Remote employees follow the same attendance accountability rules.", "Managers review exceptions before payroll is generated."]),
                ("knowledge_attendance_overtime", "Overtime and Weekend Work Policy", "When overtime can be paid and how employees request approval.", ["Overtime must be approved by the manager before payment.", "Emergency support and field callouts are documented as exceptions.", "Warehouse weekend work is reviewed separately from normal shifts.", "Payroll uses approved overtime inputs such as OVERTIME.", "Unauthorized overtime may be rejected or converted to manager review."]),
                ("knowledge_attendance_night_shift", "Night Shift and Shift Premium Guide", "Rules for warehouse night shift, support evening shift and cross-day attendance.", ["Night shift employees may have attendance spanning two calendar days.", "Shift premiums must match contract and schedule policy.", "Managers review long shifts for fatigue and compliance risk.", "Payroll separates shift premium from base wage when configured.", "Employees should report incorrect shift allocation immediately."]),
                ("knowledge_attendance_remote", "Remote and Field Work Attendance", "How remote IT and field operations employees record working time.", ["Remote work requires manager approval and correct work location.", "Field technicians record attendance around assigned visits.", "Flexible schedules still require payroll cutoff discipline.", "Unusual long days must include a business reason.", "Remote attendance is reviewed with the same audit standard as office work."]),
            ],
        ),
        (
            "knowledge_section_time_off",
            "Time Off, Leave and Accruals",
            "🌴",
            [
                ("knowledge_leave_types", "Leave Types Explained", "Employee guide to annual, sick, casual, unpaid and emergency leave.", ["Annual leave is planned and manager-approved.", "Sick leave may require HR review depending on duration.", "Casual leave covers short urgent absences.", "Unpaid leave can reduce payroll.", "Emergency leave may require HR validation and documentation."]),
                ("knowledge_leave_request", "How to Request Time Off", "Step-by-step expectations for requesting leave in Odoo.", ["Submit leave before the department planning deadline.", "Choose the correct leave type.", "Avoid peak periods such as inventory count unless urgent.", "Manager approval confirms business coverage.", "Pending leave before payroll cutoff must be resolved."]),
                ("knowledge_leave_accrual", "Leave Accrual and Balance Policy", "How leave balances are earned, reviewed and used.", ["Standard employees earn annual leave through the accrual plan.", "Sick leave accrues monthly according to company policy.", "Hourly worked-time accrual applies to eligible hourly workers.", "Probation employees may accrue slowly at first.", "Interns and fixed-term staff have limited accrual rules."]),
                ("knowledge_leave_unpaid", "Unpaid Leave and Payroll Impact", "What employees need to know before taking unpaid leave.", ["Unpaid leave can reduce gross or net pay.", "Payroll reviews unpaid leave before payslip validation.", "Employees should check the period affected by the leave.", "Unpaid leave can affect bank transfer amount.", "Managers must not promise paid treatment for unpaid leave without HR approval."]),
                ("knowledge_leave_refusal", "Why Leave Can Be Refused", "Business reasons that may cause a leave request to be refused.", ["Inventory count, customer escalation and payroll cutoff can require coverage.", "Refused leave remains visible for audit trail.", "Employees may submit a new date after discussing with the manager.", "Emergency cases should be escalated to HR.", "Refusal does not reduce leave balance when properly handled."]),
            ],
        ),
        (
            "knowledge_section_payroll",
            "Payroll, Compensation and Payslips",
            "💵",
            [
                ("knowledge_payroll_calendar", "Payroll Calendar and Cutoff", "Key deadlines for employees, managers, HR and payroll.", ["Monthly payroll covers salaried staff.", "Bi-weekly payroll covers eligible warehouse and operations workers.", "Attendance corrections must be completed before payroll generation.", "Leave approvals must be completed before payslip validation.", "Bank details must be correct before transfer approval."]),
                ("knowledge_payroll_payslip", "How to Read Your Payslip", "Employee explanation of gross wage, inputs, deductions and net wage.", ["Basic wage comes from contract and salary structure.", "Allowances may include housing, transport, bonus, commission or overtime.", "Deductions may include loan recovery, absence or late penalty.", "Net wage is the amount prepared for bank transfer.", "Questions should mention the payslip period and line item."]),
                ("knowledge_payroll_sporadic", "Sporadic Payments and Deductions", "How one-time payroll inputs are handled.", ["COMMISSION is used for approved sales commission.", "BONUS is used for one-time performance or manager bonus.", "OVERTIME is used for approved extra hours.", "RETRO is used for backdated salary corrections.", "LOAN and ABSENCE reduce net pay when applicable."]),
                ("knowledge_payroll_commission", "Sales Commission Policy", "Rules for commission eligibility, approval and payment.", ["Commission must be linked to an approved sales achievement.", "Sales manager confirms eligibility before payroll input.", "Commission is paid through payslip, not expense reimbursement.", "Commission appears in payroll and accounting bonus/commission cost.", "Disputes are reviewed before the next payroll close."]),
                ("knowledge_payroll_final_pay", "Resignation, Termination and Final Pay", "How final settlement is prepared.", ["HR confirms last working day and employee status.", "Payroll calculates earned salary, unused leave, deductions and advances.", "Finance confirms any outstanding expenses or employee receivables.", "Final pay may include retroactive adjustment or final payoff input.", "Employee access and assets are reviewed before closure."]),
                ("knowledge_payroll_loans", "Salary Advances and Loan Recovery", "Rules for salary advances and recovery through payroll.", ["Salary advance requires approval before payment.", "Employee loan receivable is tracked by finance.", "Installments are deducted through payroll input.", "Payslip shows the deduction clearly.", "Accounting clears the receivable when payroll is posted."]),
            ],
        ),
        (
            "knowledge_section_expenses",
            "Expenses and Reimbursements",
            "🧾",
            [
                ("knowledge_expense_submit", "How to Submit an Employee Expense", "Employee process for meals, travel, mileage, communication and general expenses.", ["Create the expense promptly after the business cost.", "Attach receipt when available.", "Choose the right category and payment mode.", "Submit for manager or finance review.", "Do not mix salary claims with expense claims."]),
                ("knowledge_expense_payment_modes", "Employee-Paid vs Company-Paid Expenses", "How payment mode changes reimbursement.", ["Employee-paid expenses create reimbursement payable after approval.", "Company-paid expenses do not reimburse the employee.", "Company card charges should be marked as company-paid.", "Finance reviews payment mode before posting.", "Incorrect mode delays reimbursement."]),
                ("knowledge_expense_approval", "Expense Approval Rules", "Manager and finance review expectations.", ["Manager confirms business purpose.", "Finance confirms receipt, category and policy compliance.", "Refused expenses remain visible as audit evidence.", "Approved expenses can be posted to accounting.", "Large or unusual claims may require extra explanation."]),
                ("knowledge_expense_reimbursement", "When Will I Be Reimbursed?", "Employee FAQ for reimbursement timing.", ["Approved employee-paid expenses are prepared for payment by finance.", "Payment timing may be separate from salary payroll.", "Bank account data must be valid.", "Reimbursement appears in accounting entries, not as base salary.", "Ask Finance with the expense reference if payment is delayed."]),
            ],
        ),
        (
            "knowledge_section_benefits_support",
            "Benefits and Employee Support",
            "🤝",
            [
                ("knowledge_benefits_overview", "Employee Benefits Overview", "High-level guide for benefits and support programs.", ["Eligibility depends on contract type and employee category.", "Full-time salaried employees receive standard benefit coverage.", "Fixed-term, intern and seasonal employees may have limited benefits.", "Leave accrual is a benefit and follows policy rules.", "Questions should be routed to HR."]),
                ("knowledge_support_wellbeing", "Employee Wellbeing and Support", "How employees ask for support during personal or work difficulty.", ["Speak to your manager or HR early.", "Emergency leave may be available depending on the case.", "HR can guide documentation and confidentiality.", "Support requests do not replace attendance reporting.", "Payroll impact must be explained before leave is finalized."]),
                ("knowledge_benefits_bank_details", "Bank Account and Payment Data", "Policy for salary payment bank details.", ["Employees must provide correct bank details before payroll cutoff.", "Missing bank accounts can block salary transfer.", "Changes after cutoff may move to next payment cycle.", "Finance may reject incomplete or invalid bank details.", "Bank account changes should be treated as sensitive data."]),
                ("knowledge_benefits_letters", "Employment Letters and HR Requests", "How to ask HR for employment letters and records.", ["Submit requests with purpose and deadline.", "HR verifies employee status and contract data.", "Salary letters require payroll confirmation.", "Bank or visa letters may need manager approval.", "Standard processing time is based on HR workload."]),
            ],
        ),
        (
            "knowledge_section_training",
            "Training, Compliance and Certifications",
            "🎓",
            [
                ("knowledge_training_catalog", "Training Catalog", "Available demo training sessions and purpose.", ["Company Induction covers culture and basic policies.", "Safety training supports warehouse and field compliance.", "AML briefing supports finance and compliance awareness.", "Odoo Payroll and HR training supports system adoption.", "Customer service and IT security training support role readiness."]),
                ("knowledge_training_attendance_policy", "Training Attendance Policy", "Attendance expectations for required sessions.", ["Employees must attend mandatory training assigned by HR or manager.", "Absence from compliance training must be explained.", "Scores and pass/fail status may be tracked.", "Certifications can be linked to employee records.", "Managers review training gaps before assigning regulated work."]),
                ("knowledge_training_certifications", "Certification and Recertification Rules", "How certifications are tracked and renewed.", ["Forklift, first aid and safety certifications must stay current.", "Expired certification can block operational assignment.", "HR records certification evidence in employee profile.", "Training attendance supports audit review.", "Recertification planning should start before expiry."]),
                ("knowledge_training_manager_review", "Manager Training Review Guide", "How managers use training data.", ["Review team training attendance before peak operations.", "Follow up with absent or failed participants.", "Coordinate retraining with HR.", "Use training evidence during compliance audits.", "Do not assign regulated work without required certification."]),
            ],
        ),
        (
            "knowledge_section_it_security",
            "IT, Security and Data Protection",
            "🔐",
            [
                ("knowledge_it_access", "System Access and Password Rules", "Access policy for Odoo, email and internal systems.", ["Never share passwords or one-time codes.", "Access is granted based on role and manager approval.", "Leavers must have access removed promptly.", "Suspicious access should be reported to IT.", "Payroll and HR screens require extra care because they hold sensitive data."]),
                ("knowledge_it_data_privacy", "Employee Data Privacy", "How employee and payroll data must be protected.", ["Do not export employee data unless authorized.", "Do not send payroll files over unsecured channels.", "Use Odoo permissions instead of screenshots where possible.", "Report accidental disclosure immediately.", "Managers can only access data needed for their role."]),
                ("knowledge_it_remote_work", "Remote Work Security", "Security expectations for remote and hybrid employees.", ["Use approved devices and secure networks.", "Lock your screen when away.", "Do not store payroll or HR files on personal devices.", "Report lost devices immediately.", "Remote work does not remove attendance obligations."]),
                ("knowledge_it_incident", "Security Incident Reporting", "What employees do when security risk occurs.", ["Report phishing, suspicious login, lost device or data exposure immediately.", "Do not delete evidence before IT review.", "Notify manager if work is affected.", "Payroll or bank data incidents must be escalated urgently.", "IT documents incident response actions."]),
            ],
        ),
        (
            "knowledge_section_finance_accounting",
            "Finance, Banking and Accounting",
            "🏦",
            [
                ("knowledge_finance_salary_transfer", "Salary Transfer Process", "How payroll becomes a bank transfer.", ["Payroll validates payslips before finance prepares transfer.", "Bank transfer lines come from net wage on payslips.", "Finance reviews missing bank accounts and payment statuses.", "Approved transfers are sent to bank.", "Reconciled transfers close the payment loop."]),
                ("knowledge_finance_rejected_payment", "Rejected Salary Payment FAQ", "What happens if a salary payment is rejected.", ["Finance records the rejected payment as an exception.", "Employee bank details are checked before reissue.", "Payroll payable may remain open until corrected.", "Employee should contact HR and Finance with bank reference.", "Reissue timing depends on bank and approval process."]),
                ("knowledge_finance_payroll_accounting", "Payroll Accounting Explained", "Plain-language explanation of payroll journal entries.", ["Payroll accrual records salary expense and payroll payable.", "Salary bank payment clears payable against bank.", "Expense reimbursement creates employee payable and payment entries.", "Leave accrual records leave expense and liability.", "Draft entries are reviewed before posting."]),
                ("knowledge_finance_reconciliation", "Payroll Reconciliation Checklist", "Finance checklist after salary payment.", ["Compare payslip net total with bank transfer total.", "Review missing, rejected or difference lines.", "Match bank statement entries to salary transfer batch.", "Investigate payroll clearing differences.", "Mark reconciliation complete only when exceptions are explained."]),
                ("knowledge_finance_chart_accounts", "Payroll Chart of Accounts Guide", "Accounts used in the demo payroll close.", ["Salaries and Wages Expense records gross payroll cost.", "Payroll Payable tracks amounts owed to employees.", "Employee Expense Payable tracks reimbursements.", "Accrued Leave Liability tracks earned leave exposure.", "Salary Bank Clearing supports payment reconciliation."]),
            ],
        ),
        (
            "knowledge_section_manager_playbooks",
            "Manager Playbooks and Approvals",
            "✅",
            [
                ("knowledge_manager_payroll_cutoff", "Manager Payroll Cutoff Checklist", "What managers must complete before payroll runs.", ["Review attendance exceptions.", "Approve or refuse pending leave.", "Confirm approved overtime.", "Escalate missing bank or contract issues to HR.", "Answer payroll questions before validation."]),
                ("knowledge_manager_leave_approval", "Leave Approval Playbook", "How managers approve leave without harming operations.", ["Check team coverage and peak work periods.", "Approve valid leave quickly.", "Refuse with clear business reason when needed.", "Escalate emergency leave to HR.", "Resolve pending leaves before payroll cutoff."]),
                ("knowledge_manager_overtime_approval", "Overtime Approval Playbook", "How managers justify overtime and weekend work.", ["Confirm business need before overtime is worked when possible.", "Document emergency coverage reasons.", "Check attendance records for worked hours.", "Tell payroll which employees are approved.", "Review overtime cost in department payroll summary."]),
                ("knowledge_manager_department_cost", "Department Payroll Cost Review", "How managers explain department payroll totals.", ["Review headcount, overtime, leave, bonuses and commissions.", "Compare warehouse bi-weekly costs with office monthly costs.", "Investigate unusual net pay changes.", "Use department summary for executive discussion.", "Coordinate corrections with payroll and finance."]),
            ],
        ),
        (
            "knowledge_section_employee_faq",
            "Employee FAQ",
            "❓",
            [
                ("knowledge_faq_payslip_empty", "Why Can't I See My Payslip?", "Common reasons an employee cannot find a payslip.", ["The payslip may not be generated yet.", "The employee may be in the wrong company context.", "Payroll batch may still be draft.", "Ask payroll with your employee name and pay period.", "Managers cannot promise payslip release before payroll validation."]),
                ("knowledge_faq_salary_amount", "Why Is My Salary Amount Different?", "Common reasons for net pay differences.", ["Overtime, bonus or commission can increase net pay.", "Loan recovery, absence or unpaid leave can reduce net pay.", "Mid-month joins may be prorated.", "Retroactive adjustment may correct prior period pay.", "Review payslip input lines before escalating."]),
                ("knowledge_faq_expense_status", "Why Is My Expense Not Paid Yet?", "Common reasons employee expenses are delayed.", ["Expense may still be draft or submitted.", "Manager or finance approval may be pending.", "Receipt or category may be missing.", "Payment mode may be company-paid instead of employee-paid.", "Finance processes reimbursements after approval."]),
                ("knowledge_faq_leave_balance", "Why Is My Leave Balance Different?", "Common reasons leave balance changes.", ["Accrual plan may add leave monthly or by worked time.", "Approved leave reduces available balance.", "Refused leave should not reduce balance.", "Unpaid leave may not use paid leave balance.", "Ask HR to review accrual plan and leave history."]),
                ("knowledge_faq_bank_payment", "What If My Salary Is Not in the Bank?", "Employee steps when salary payment is delayed.", ["Confirm payroll has validated the payslip.", "Confirm bank account details are correct.", "Ask Finance whether the transfer was generated, sent or rejected.", "Rejected payments require bank data correction.", "Do not submit the same issue to multiple departments without reference."]),
                ("knowledge_faq_training", "Do I Need to Attend This Training?", "How to know whether training is required.", ["Mandatory training is assigned by HR, manager or compliance.", "Safety and certification training may be required before operational work.", "Absent training attendance should be explained.", "Failed certification may require retake.", "Training records support compliance audit."]),
            ],
        ),
    ]

    sequence = 10
    for section_xmlid, section_name, section_icon, child_defs in sections:
        section = _article(
            section_xmlid,
            section_name,
            _html(
                section_name,
                f"Index page for {section_name.lower()} articles used by employees and managers.",
                [
                    "Open the child articles below for detailed employee guidance.",
                    "Use these pages during the live demo to answer realistic employee questions.",
                    "When the policy affects an Odoo workflow, the article names the responsible team.",
                ],
            ),
            parent=root,
            sequence=sequence,
            icon=section_icon,
        )
        for child_sequence, (xmlid, title, purpose, bullets) in enumerate(child_defs, start=1):
            _article(
                xmlid,
                title,
                _html(title, purpose, bullets),
                parent=section,
                sequence=child_sequence * 10,
                icon=section_icon,
            )
        sequence += 10

    _create_knowledge_ai_agent(env, root)


def _create_knowledge_ai_agent(env, root_article):
    if "ai.agent" not in env.registry.models or "ai.agent.source" not in env.registry.models:
        return

    Agent = env["ai.agent"].sudo()
    Source = env["ai.agent.source"].sudo()
    agent = _xmlid_record(env, "ai_agent_allnetworks_knowledge")
    values = {
        "name": "ALLNETWORKS Knowledge AI Assistant",
        "subtitle": "Answers employee HR, payroll, attendance, leave, expense and accounting questions from the ALLNETWORKS Knowledge base.",
        "system_prompt": (
            "You are the ALLNETWORKS employee policy assistant. Answer using the ALLNETWORKS Knowledge base. "
            "Be concise, practical and employee-friendly. If the policy is not covered, direct the employee to HR, Payroll, Finance or their manager. "
            "Do not invent company policies."
        ),
        "response_style": "analytical",
        "restrict_to_sources": True,
    }
    if not agent:
        agent = Agent.create(values)
        _register_xmlid(env, agent, "ai_agent_allnetworks_knowledge")
    else:
        agent.write(values)

    if root_article and not Source.search([("agent_id", "=", agent.id), ("article_id", "=", root_article.id)], limit=1):
        Source.create(
            {
                "name": root_article.name,
                "agent_id": agent.id,
                "article_id": root_article.id,
                "url": root_article.article_url,
                "type": "knowledge_article",
            }
        )

    cron = env.ref("ai.ir_cron_process_sources", raise_if_not_found=False)
    if cron:
        cron._trigger()


def _create_knowledge_ai_questions(env, company):
    if "hr.payroll.demo.knowledge.ask" not in env.registry.models:
        return
    Question = env["hr.payroll.demo.knowledge.ask"].sudo()
    sample_questions = [
        ("knowledge_question_salary_rejected", "What should I do if my salary payment is rejected by the bank?"),
        ("knowledge_question_unpaid_leave", "How does unpaid leave affect my payroll?"),
        ("knowledge_question_overtime", "When is overtime paid and who approves it?"),
        ("knowledge_question_expense_reimbursement", "When will I be reimbursed for an employee-paid expense?"),
        ("knowledge_question_holidays", "How are public holidays treated in payroll?"),
        ("knowledge_question_training_required", "Do I need to attend safety or certification training before warehouse work?"),
        ("knowledge_question_leave_balance", "Why is my leave balance different from last month?"),
        ("knowledge_question_bank_details", "When should I update my salary bank account details?"),
        ("knowledge_question_payslip_difference", "Why is my net salary different this month?"),
        ("knowledge_question_manager_cutoff", "What must a manager review before payroll cutoff?"),
    ]
    for xmlid, question in sample_questions:
        if _xmlid_record(env, xmlid):
            continue
        record = Question.create({"company_id": company.id, "question": question})
        record.action_ask_ai()
        _register_xmlid(env, record, xmlid)

