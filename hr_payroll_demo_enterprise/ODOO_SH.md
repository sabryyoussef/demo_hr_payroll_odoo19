# Odoo.sh deployment — ALLNETWORKS HR Payroll Demo

Odoo.sh creates a **new PostgreSQL database** when a development branch is reset or ages out (~1 month on trial tiers). Demo data is **not** stored in git; it is recreated by installing this module on a fresh database.

## What loads automatically

On **first install** of `hr_payroll_demo_enterprise`, Odoo runs `post_init_hook` → `bootstrap_all_demo_data()` in `hooks.py`. That creates in one pass:

- ALLNETWORKS Caribbean Holdings Ltd (demo company)
- ~97 employees, 9 departments, contracts, attendance (~7k rows)
- Time off, accruals, payroll batches & payslips
- Salary adjustments, Approvals requests, bank transfers, expenses
- Training, certifications, scenarios, knowledge base
- Employee scheduled activities, To-Do tasks, attendance alerts
- Dashboards and workflow configuration

No separate `tools/load_*.py` scripts are required on Odoo.sh if you use a **fresh database + install**.

## Repository layout on Odoo.sh

Ensure the project **addons path** includes the folder that contains this module, for example:

```text
hr_payroll_demo_enterprise_odoo19/   ← addons path entry
  hr_payroll_demo_enterprise/        ← module technical name
```

In Odoo.sh: **Settings → Submodules / Addons path** (or `odoo.conf` in the repo) must list that directory.

## Fresh database checklist

1. Push this branch to GitHub and link the repo to Odoo.sh.
2. Wait for the build (Enterprise + dependencies must be available on the platform).
3. Open the branch database (new or after reset).
4. **Apps** → update apps list → install **HR Payroll Demo Enterprise**.
5. Log in as admin → switch company to **ALLNETWORKS Caribbean Holdings Ltd**.
6. Open **Payroll Demo Enterprise** menu or **To-Do** / **HR** apps to verify data.

`--without-demo` on database creation does **not** skip this module’s bootstrap; `post_init_hook` always runs on module **install**.

## After a module upgrade (same database)

`post_init_hook` does **not** run again on `-u`. To add newer demo slices without reinstalling:

```bash
python hr_payroll_demo_enterprise/scripts/bootstrap_demo.py -c odoo.conf -d YOURDB --supplementary
```

Or from Odoo shell:

```python
from odoo.addons.hr_payroll_demo_enterprise.hooks import bootstrap_supplementary_demo_data
bootstrap_supplementary_demo_data(env)
env.cr.commit()
```

## Dependencies

The module manifest requires Enterprise apps: payroll, attendance, holidays, expenses, approvals, knowledge, `project_todo`, etc. The Odoo.sh project must use an **Enterprise** Odoo 19 image with these apps available.

## Troubleshooting

| Symptom | Fix |
|--------|-----|
| Empty HR after install | Company still “My Company” — switch to ALLNETWORKS |
| No time off in list | Use **Time Off** (all), not **My Time Off**; check company filter |
| No To-Do tasks | Install **To-Do** (`project_todo`); it is a manifest dependency |
| Install skipped bootstrap | Demo company XML id already exists — new DB or `--supplementary` |
