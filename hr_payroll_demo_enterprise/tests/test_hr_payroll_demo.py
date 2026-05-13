from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayrollDemo(TransactionCase):
    def test_demo_company_and_employees_exist(self):
        company = self.env.ref("hr_payroll_demo_enterprise.company_allnetworks_caribbean")
        employees = self.env["hr.employee"].search([("company_id", "=", company.id)])
        self.assertGreaterEqual(len(employees), 40)

    def test_payroll_batches_exist(self):
        company = self.env.ref("hr_payroll_demo_enterprise.company_allnetworks_caribbean")
        batches = self.env["hr.payslip.run"].search([("company_id", "=", company.id)])
        self.assertGreaterEqual(len(batches), 3)
        self.assertTrue(batches.mapped("slip_ids"))

    def test_bank_transfer_generation(self):
        transfer = self.env["hr.payroll.demo.bank.transfer"].search([], limit=1)
        self.assertTrue(transfer)
        self.assertTrue(transfer.line_ids)
        self.assertGreater(transfer.total_amount, 0)

    def test_mass_operation_attendance_adjustment(self):
        company = self.env.ref("hr_payroll_demo_enterprise.company_allnetworks_caribbean")
        operation = self.env["hr.payroll.demo.mass.operation"].create(
            {
                "name": "Test Attendance Adjustment",
                "company_id": company.id,
                "operation_type": "attendance_adjustment",
            }
        )
        operation.action_execute()
        self.assertEqual(operation.state, "done")

    def test_scenario_catalog(self):
        scenarios = self.env["hr.payroll.demo.scenario"].search([])
        self.assertGreaterEqual(len(scenarios), 17)
