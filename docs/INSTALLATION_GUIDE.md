# Installation Guide

## Addons Path

Add the parent folder to your Odoo 19 config:

```text
D:\odoo\odoo19\projects\allnetworks_wood_demo19
```

## Install From UI

1. Start Odoo 19 with Enterprise addons enabled.
2. Enable developer mode.
3. Apps > Update Apps List.
4. Search `HR Payroll Demo Enterprise`.
5. Install.

## Install From Command Line

```powershell
& "C:/Users/HP/AppData/Local/Programs/Python/Python312/python.exe" `
  "D:/odoo/odoo19/odoo19/odoo-bin" `
  -c "D:/odoo/odoo19/odoo_conf/odoo19.conf" `
  -d YOUR_DB `
  -i hr_payroll_demo_enterprise `
  --stop-after-init
```

## Expected Result

After installation:

- New app menu: `Payroll Demo Enterprise`
- Dashboard record: `ALLNETWORKS Payroll Operations Dashboard`
- 48 demo employees
- 3 months of attendance records
- Payroll batches and payslips
- Bank transfers and reconciliation examples

## Troubleshooting

- If module is missing, confirm `addons_path`.
- If payroll dependencies fail, confirm Enterprise path is enabled.
- If Python errors appear, use the Python 3.12 runtime used by your Odoo 19 instance.
