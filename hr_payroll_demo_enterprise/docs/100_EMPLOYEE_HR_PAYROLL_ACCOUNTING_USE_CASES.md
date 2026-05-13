# 100 Employee HR, Payroll and Accounting Use Case Scenarios

This document defines a complete Odoo 19 demo story for a company with 100 employees. It is designed to cover the main HR, Attendance, Time Off, Payroll, Expenses, Accounting, Banking and reporting flows in one realistic company cycle.

## Demo Company

Company: `ALLNETWORKS Caribbean Holdings Ltd`

Business profile: regional distribution, support and services company with office, warehouse, field service and sales teams.

Demo period: one quarter, with the main presentation focused on one payroll month.

Payroll policy:

- Monthly payroll for salaried staff.
- Bi-weekly payroll for hourly and warehouse staff.
- Overtime paid for eligible operational roles.
- Unpaid absence and late penalties deducted from payroll.
- Commissions paid to sales employees.
- Bonuses paid to selected managers and high performers.
- Loans and advances deducted in installments.
- Final settlement for resigned employees.
- Payroll journal entries posted to accounting.
- Salary payments exported and reconciled through bank journals.

## Employee Population

The 100 employees are grouped by department, category, contract type, payroll frequency and work schedule.

| Department | Headcount | Example Positions | Main Employee Categories |
| --- | ---: | --- | --- |
| Executive and Administration | 6 | General Manager, Office Manager, Executive Assistant | Salaried, full-time |
| Human Resources | 8 | HR Manager, HR Officer, Recruiter, Payroll Specialist | Salaried, full-time |
| Finance and Accounting | 10 | Finance Manager, Accountant, AP Officer, AR Officer, Payroll Accountant | Salaried, full-time |
| Sales | 18 | Sales Manager, Account Executive, Sales Representative, Sales Coordinator | Salaried plus commission |
| Customer Support | 16 | Support Manager, Team Lead, Support Agent, Quality Analyst | Shift-based salaried |
| Operations | 14 | Operations Manager, Dispatcher, Field Supervisor, Field Technician | Mixed salaried and hourly |
| Warehouse and Logistics | 20 | Warehouse Manager, Inventory Clerk, Picker, Driver, Forklift Operator | Hourly, bi-weekly |
| IT and Systems | 5 | IT Manager, System Admin, Helpdesk Analyst | Salaried, full-time |
| Temporary and Interns | 3 | HR Intern, Warehouse Temp, Finance Intern | Fixed-term or internship |

## Employee Categories

Use these employee categories to demonstrate filtering, contracts, payroll rules and reporting.

| Category | Count | Payroll Treatment | Typical Scenarios |
| --- | ---: | --- | --- |
| Full-time salaried | 48 | Monthly salary with allowances and standard deductions | Normal payroll, leave, bonus, salary increment |
| Hourly operations | 18 | Paid by worked hours, overtime eligible | Overtime, missing checkout, shift changes |
| Warehouse bi-weekly | 14 | Bi-weekly payroll, overtime and late deductions | Bi-weekly batch, weekend work, attendance corrections |
| Sales commission | 10 | Base salary plus commission inputs | Commission payroll, sales bonus, expense reimbursement |
| Managers | 5 | Monthly salary, bonus, approval responsibilities | Approvals, department reporting, dashboard actions |
| Fixed-term contract | 3 | Contract end date and renewal tracking | Contract renewal, final payout |
| Interns | 2 | Fixed allowance, limited benefits | New hire onboarding, unpaid leave |

## Work Schedules and Time Patterns

Use different calendars to prove that Odoo can calculate attendance, work entries and payroll from real working patterns.

| Schedule | Employees | Working Pattern | Demo Purpose |
| --- | ---: | --- | --- |
| Office standard | 45 | Monday to Friday, 8:30 AM to 5:00 PM | Normal attendance, annual leave, public holidays |
| Customer support shift A | 8 | 7:00 AM to 3:00 PM | Early shift and handover coverage |
| Customer support shift B | 8 | 3:00 PM to 11:00 PM | Evening shift and late premiums |
| Warehouse day shift | 12 | 6:00 AM to 2:00 PM | Hourly work, overtime, late check-in |
| Warehouse night shift | 8 | 10:00 PM to 6:00 AM | Night shift and cross-day attendance |
| Field operations flexible | 11 | Planned visits with overtime | Field overtime and remote attendance |
| Part-time interns | 2 | 4 hours per day, 3 days per week | Part-time payroll and leave limitations |
| Remote IT support | 6 | Hybrid calendar | Remote work and attendance exceptions |

## Holiday and Time Off Setup

The quarter includes public holidays, company holidays and individual leave cases.

| Leave or Holiday Type | Example Scenario | Payroll Effect |
| --- | --- | --- |
| Public holiday | National holiday during payroll month | Paid non-working day |
| Annual leave | Approved 5-day vacation for a finance employee | Paid leave work entries |
| Sick leave | Support agent takes 2 sick days | Paid or partially paid depending on policy |
| Casual leave | One-day urgent absence for admin employee | Paid leave if balance exists |
| Emergency leave | Field technician has emergency leave request | Manager approval flow |
| Unpaid leave | Warehouse employee takes 3 unpaid days | Deduction from payroll |
| Leave refusal | Employee requests leave during inventory count | Refused request and audit trail |
| Pending leave | Manager has not approved a request before cutoff | Payroll warning before validation |
| Leave allocation | HR grants annual leave balance to new employees | Balance creation and reporting |

## End-to-End Monthly Story

The demo month can be presented as a single business story.

1. HR hires new employees and updates contracts.
2. Department managers review attendance exceptions.
3. Employees submit time off requests.
4. HR approves valid leaves and refuses conflicting requests.
5. Payroll reviews work entries and input lines.
6. Payroll generates monthly and bi-weekly payslips in batches.
7. Payroll corrects exceptions such as unpaid leave, missing checkout and loans.
8. Finance validates payroll batches.
9. Accounting posts payroll journal entries.
10. Finance creates salary bank transfer batches.
11. Bank statement lines are imported or simulated.
12. Accounting reconciles salary payments and investigates exceptions.
13. Management reviews department payroll cost, overtime, leaves and headcount.

## Core Use Case Scenarios

### 1. New Hire Onboarding Before Payroll Cutoff

Employee: `Maya Clarke`, HR Officer.

Flow:

- HR creates employee profile.
- HR creates work contact, department, job position and manager.
- HR creates contract starting on the first day of the month.
- HR assigns salary structure, work schedule and bank account.
- Payroll includes employee in the current monthly batch.

Expected result:

- Employee appears in HR headcount.
- Contract is active.
- Payslip is generated with full monthly salary.
- Payroll journal includes salary and employer costs.

### 2. New Hire Mid-Month Proration

Employee: `Owen Miller`, Support Agent.

Flow:

- Employee contract starts on the 16th of the month.
- Attendance records begin from start date.
- Payroll generates a payslip for the partial month.

Expected result:

- Payslip reflects prorated salary or worked days.
- Payroll dashboard highlights the new hire scenario.
- Accounting posts only the earned payroll cost.

### 3. Employee Category Change

Employee: `Daniel Brooks`, Warehouse Temp.

Flow:

- HR changes employee from fixed-term temp to full-time hourly.
- Contract is renewed with new wage and benefits.
- Work schedule changes from temporary roster to warehouse day shift.

Expected result:

- Employee category history is visible.
- New payroll batch uses the updated wage and schedule.
- Reporting separates temp cost from full-time cost.

### 4. Department Transfer

Employee: `Lina Roberts`, Customer Support Agent.

Flow:

- HR transfers employee from Customer Support to Sales Coordination.
- Manager and department are updated.
- Payroll analytic distribution changes to Sales.

Expected result:

- Department payroll report reflects cost in the new department.
- Employee hierarchy updates.
- Accounting analytic allocation follows the new department.

### 5. Promotion and Salary Increment

Employee: `Rafael Grant`, Sales Representative.

Flow:

- Manager approves promotion to Senior Sales Representative.
- HR updates job position and salary.
- Payroll creates salary increment effective from a specific date.

Expected result:

- Payslip uses the new wage from the effective date.
- Retroactive difference can be handled if approval is late.
- Salary history supports audit review.

### 6. Contract Renewal

Employee: `Alicia Bennett`, Field Technician.

Flow:

- Fixed-term contract is close to expiration.
- HR renews the contract for another year.
- Payroll continues processing without interruption.

Expected result:

- Contract renewal activity is completed.
- Payroll warning disappears.
- Employee remains included in the correct payroll batch.

### 7. Resignation and Final Payoff

Employee: `Sofia Campbell`, Accountant.

Flow:

- HR records resignation date.
- Remaining unpaid salary is calculated.
- Unused annual leave is paid out.
- Loan balance or advances are deducted.
- Final payslip is generated and posted.

Expected result:

- Employee status is archived after last working day.
- Final settlement payslip includes salary, leave payoff and deductions.
- Accounting posts final payroll liability and payment.

### 8. Termination With Deductions

Employee: `Marcus King`, Warehouse Driver.

Flow:

- HR records termination.
- Payroll calculates unpaid absence and equipment deduction.
- Final payment is reviewed by HR and Finance.

Expected result:

- Final payslip shows deductions clearly.
- Accounting liability equals net payable.
- Employee no longer appears in future payroll batches.

### 9. Standard Monthly Payroll

Employees: office, HR, finance, IT and management.

Flow:

- Payroll officer creates monthly payroll batch.
- Payslips are generated for all eligible salaried employees.
- Payroll validates payslips after checking warnings.

Expected result:

- Gross, deductions and net salary are calculated.
- Payroll register is available by department.
- Journal entry is posted to accounting.

### 10. Bi-Weekly Warehouse Payroll

Employees: warehouse and logistics team.

Flow:

- Payroll officer creates a bi-weekly payroll batch.
- Attendance hours are reviewed.
- Overtime and absence deductions are included.

Expected result:

- Warehouse employees are paid for the correct two-week period.
- Hourly payroll is separated from monthly payroll.
- Bank transfer batch can be created independently.

### 11. Overtime Approval and Payment

Employee: `Tanya Lewis`, Warehouse Picker.

Flow:

- Employee works 10 extra hours during month-end inventory.
- Supervisor approves overtime.
- Payroll includes approved overtime input in payslip.

Expected result:

- Overtime analysis report shows hours and cost.
- Payslip includes overtime allowance.
- Accounting posts overtime to payroll expense.

### 12. Weekend Work

Employee: `Andre Nelson`, Field Technician.

Flow:

- Employee works on Saturday for emergency customer support.
- Attendance is recorded on a non-standard day.
- Payroll calculates weekend premium or overtime.

Expected result:

- Work entry is visible as exception or overtime.
- Payslip includes weekend work pay.
- Manager can justify the cost from operations report.

### 13. Night Shift Attendance

Employee: `Keisha Brown`, Warehouse Operator.

Flow:

- Employee checks in at 10:00 PM and checks out at 6:00 AM next day.
- Payroll period includes cross-day attendance.
- Night shift premium is reviewed.

Expected result:

- Attendance is correctly linked to the shift.
- Worked hours are correct.
- Payroll includes night shift allowance if configured.

### 14. Late Check-In Penalty

Employee: `Jamal Price`, Support Agent.

Flow:

- Employee arrives late several times during the month.
- Attendance violations are reviewed by manager.
- Payroll applies late penalty deduction.

Expected result:

- Attendance violation report shows repeated lateness.
- Payslip includes penalty deduction.
- HR can discuss attendance trend with employee.

### 15. Missing Checkout Correction

Employee: `Nadia Foster`, Customer Support Agent.

Flow:

- Employee forgets to check out.
- Attendance record is flagged.
- Manager corrects checkout time before payroll cutoff.

Expected result:

- Payroll warning is resolved before payslip validation.
- Work entries are recalculated.
- Audit trail shows correction.

### 16. Remote Work Attendance

Employee: `Ethan Morris`, IT System Admin.

Flow:

- Employee works remotely for 3 days.
- Attendance source or note marks remote work.
- Manager reviews normal hours with no penalty.

Expected result:

- Remote work appears in attendance analysis.
- Payroll remains normal.
- HR can report hybrid work patterns.

### 17. Approved Annual Leave

Employee: `Priya Singh`, Finance Officer.

Flow:

- Employee requests 5 annual leave days.
- Manager approves.
- Payroll generates paid leave work entries.

Expected result:

- Leave balance decreases.
- Payslip includes paid leave without salary deduction.
- Leave report shows department absence coverage.

### 18. Sick Leave During Payroll Month

Employee: `Omar Johnson`, Support Agent.

Flow:

- Employee submits 2 sick leave days.
- HR validates medical leave.
- Payroll processes sick leave according to policy.

Expected result:

- Sick leave is reflected in Time Off.
- Payslip shows paid or partially paid sick leave.
- HR dashboard shows sick leave trend.

### 19. Unpaid Leave Deduction

Employee: `Camila Wright`, Warehouse Clerk.

Flow:

- Employee requests unpaid leave for 3 days.
- Manager approves because balance is unavailable.
- Payroll deducts unpaid days.

Expected result:

- Payslip net salary is reduced.
- Payroll report explains the deduction.
- Accounting payroll liability is lower.

### 20. Leave Request Refused Due to Business Need

Employee: `Noah Edwards`, Inventory Supervisor.

Flow:

- Employee requests leave during inventory closing week.
- Manager refuses request.
- Employee remains scheduled and attendance is expected.

Expected result:

- Refused request is visible in Time Off history.
- No payroll effect occurs.
- Manager can explain operational coverage.

### 21. Pending Leave Before Payroll Cutoff

Employee: `Ella Morgan`, Sales Coordinator.

Flow:

- Employee submits leave close to payroll cutoff.
- Request remains pending.
- Payroll dashboard highlights pending approval.

Expected result:

- Payroll officer can follow up before validation.
- If not approved, payslip is held or reviewed.
- Demonstrates workflow control before payroll closing.

### 22. Employee Loan Deduction

Employee: `Victor Allen`, Field Supervisor.

Flow:

- Finance grants employee loan.
- Payroll deducts monthly installment.
- Remaining balance is tracked.

Expected result:

- Payslip includes loan deduction.
- Accounting recognizes receivable recovery.
- Employee net salary is reduced correctly.

### 23. Salary Advance Recovery

Employee: `Rina Cole`, Support Team Lead.

Flow:

- Employee receives mid-month salary advance.
- Payroll deducts the advance from net pay.
- Finance reconciles advance account.

Expected result:

- Payslip shows advance deduction.
- Employee payable is reduced.
- Accounting advance clearing is traceable.

### 24. Sales Commission Payroll

Employees: sales team.

Flow:

- Sales manager approves monthly commission file.
- Payroll imports or enters commission input lines.
- Commission appears on payslips.

Expected result:

- Sales employees receive base plus commission.
- Commission cost is reported by department.
- Accounting posts commission expense.

### 25. Performance Bonus

Employees: selected managers and top performers.

Flow:

- Management approves one-time bonus.
- Payroll adds bonus input to selected employees.
- Finance reviews gross payroll increase.

Expected result:

- Bonus is included in payslip.
- Bonus cost is visible in payroll analysis.
- Journal entry separates salary and bonus cost if configured.

### 26. Expense Reimbursement With Payroll Coordination

Employee: `Leo Martin`, Sales Executive.

Flow:

- Employee submits travel expense.
- Expense is approved by manager and finance.
- Payroll confirms it is not double paid as salary.

Expected result:

- Expense accounting remains separate from payroll salary.
- Employee reimbursement is traceable.
- Finance can compare payroll payment and expense payment.

### 27. Payroll Correction After Validation

Employee: `Grace Adams`, HR Officer.

Flow:

- Payslip is validated.
- HR finds missing unpaid leave.
- Payroll creates correction entry or adjustment in next payroll.

Expected result:

- Original payroll remains auditable.
- Correction is posted with explanation.
- Payroll report shows adjustment reason.

### 28. Retroactive Salary Adjustment

Employee: `Benjamin Scott`, IT Helpdesk Analyst.

Flow:

- Salary increment is approved late but effective from previous month.
- Payroll calculates retroactive difference.
- Difference is paid in current payslip.

Expected result:

- Payslip includes retroactive adjustment.
- Payroll cost report identifies back pay.
- Accounting posts adjustment in current period.

### 29. Payroll Batch Validation With Exceptions

Employees: all monthly payroll employees.

Flow:

- Payroll generates payslips for 78 monthly employees.
- System flags exceptions: missing contract, pending leave, missing checkout.
- Payroll fixes valid exceptions and holds unresolved payslips.

Expected result:

- Clean payslips are validated in batch.
- Problem payslips remain for correction.
- Dashboard shows pending payroll exceptions.

### 30. Mass Attendance Adjustment

Employees: warehouse day shift.

Flow:

- Time clock outage affects 12 employees.
- HR creates mass attendance correction.
- Payroll recalculates worked hours.

Expected result:

- Bulk correction reduces manual work.
- Attendance report shows adjusted entries.
- Payslips use corrected time.

### 31. Bulk Leave Approval

Employees: support team.

Flow:

- Manager reviews multiple casual leave requests.
- Valid requests are approved in bulk.
- Conflicting requests remain pending or refused.

Expected result:

- Time Off workflow is handled quickly.
- Payroll receives paid or unpaid leave data.
- Department coverage is protected.

### 32. Multi-Department Payroll Batch

Employees: full company.

Flow:

- Payroll creates one company-wide payroll run.
- Filters are used by department for review.
- Finance reviews total cost by department before posting.

Expected result:

- Department cost summary is available.
- Managers can validate their own exceptions.
- Payroll can still post one consolidated journal.

### 33. Payroll Journal Entry Posting

Employees: all paid employees.

Flow:

- Payroll validates payslips.
- Odoo generates accounting entry.
- Salaries, allowances, deductions, taxes and liabilities are posted.

Expected result:

- Payroll expense appears in profit and loss.
- Salary payable appears in balance sheet.
- Deductions and employer contributions are posted to liability accounts.

### 34. Multi-Bank Salary Transfer

Employees: all paid employees.

Flow:

- Employee bank accounts belong to different banks.
- Finance creates bank transfer batches by bank.
- Export files are prepared or simulated.

Expected result:

- Bank transfer summary shows totals per bank.
- Employees without bank accounts are flagged.
- Finance can send salary files with fewer clicks.

### 35. Cash Payment Exception

Employee: `Warehouse Temp`.

Flow:

- Employee has no bank account.
- Finance marks salary payment as cash or manual payment.
- Payroll report highlights non-bank payment.

Expected result:

- Exception is visible before bank export.
- Manual payment is tracked.
- Accounting can reconcile cash payment separately.

### 36. Bank Reconciliation of Salary Payments

Employees: payroll batch.

Flow:

- Bank statement is imported or simulated.
- Salary transfer line is matched to payroll payable.
- Difference is investigated if bank charge or rejected payment exists.

Expected result:

- Salary payable is cleared.
- Bank journal is reconciled.
- Payroll reconciliation report shows matched and unmatched items.

### 37. Rejected Bank Payment

Employee: `Iris Walker`, Sales Representative.

Flow:

- Bank rejects payment due to invalid account number.
- Finance updates employee bank account.
- Payment is reissued.

Expected result:

- Bank transfer exception is documented.
- Employee receives corrected payment.
- Accounting reconciliation has clear audit trail.

### 38. Payroll Accrual at Month End

Employees: all employees when payroll is paid next month.

Flow:

- Payroll is calculated before month close.
- Accounting accrues payroll expense and liability.
- Payment is made in the next period.

Expected result:

- Expense is recognized in correct month.
- Salary payable remains open until payment.
- Management reports reflect true cost.

### 39. Department Payroll Budget Review

Departments: Sales, Warehouse, Support.

Flow:

- Finance compares actual payroll cost against budget.
- Overtime and commission are reviewed as cost drivers.
- Managers explain variances.

Expected result:

- Department payroll summary supports budget control.
- Overtime and commission are visible.
- Management can reduce future cost leakage.

### 40. Payroll Audit and Security Review

Users: HR Officer, Payroll Officer, Finance Manager, Department Manager.

Flow:

- Different users access the same payroll process.
- HR manages employees and leaves.
- Payroll manages payslips.
- Finance posts accounting and bank payments.
- Department managers approve only their team's requests.

Expected result:

- Access rights restrict sensitive salary data.
- Approval responsibilities are separated.
- Audit trail supports compliance.

## Reporting Coverage

Use these reports and dashboards during the demo.

| Report | Business Question |
| --- | --- |
| HR Headcount by Department | How many employees are active by department and category? |
| Attendance Violations | Who was late, absent or missing checkout? |
| Overtime Analysis | Which departments generated overtime cost? |
| Leave Balance Report | Who has remaining annual leave and who exceeded balance? |
| Payroll Batch Summary | What is the gross, deduction and net salary by batch? |
| Department Payroll Summary | Which department has the highest payroll cost? |
| Employee Payroll Analysis | What changed in an employee's payslip month over month? |
| Bank Transfer Summary | How much will be transferred per bank? |
| Payroll Accounting Impact | What journal entries were posted from payroll? |
| Payroll Reconciliation | Which salary payments are matched or still open? |

## Recommended Demo Sequence

1. Open HR dashboard and show 100 employees by department and category.
2. Open employee profile and explain contract, salary, bank and schedule.
3. Show attendance exceptions: late check-in, overtime, missing checkout.
4. Show time off: approved annual leave, unpaid leave, refused leave, pending leave.
5. Generate monthly payroll batch.
6. Generate bi-weekly warehouse payroll batch.
7. Review payslip examples: normal, overtime, commission, loan, unpaid leave, final payoff.
8. Validate clean payslips and keep exception payslips for correction.
9. Post payroll accounting entries.
10. Create bank transfer batches by bank.
11. Reconcile salary payment in bank journal.
12. Review department payroll summary and accounting impact.

## Scenario Checklist

- 100 active or recently active employees are represented.
- At least 7 employee categories are covered.
- At least 8 work schedules are covered.
- Monthly and bi-weekly payrolls are covered.
- Salaried and hourly payrolls are covered.
- Overtime, weekend and night shift cases are covered.
- Paid leave, unpaid leave, sick leave, refused leave and pending leave are covered.
- New hire, promotion, transfer, contract renewal, resignation and termination are covered.
- Bonus, commission, loan, advance, retroactive adjustment and correction are covered.
- Payroll posting, salary payable, bank transfer and reconciliation are covered.
- Security roles and approval separation are covered.
