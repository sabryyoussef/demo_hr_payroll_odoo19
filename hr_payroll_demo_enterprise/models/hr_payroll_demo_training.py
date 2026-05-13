from odoo import _, api, fields, models


TRAINING_TYPE_SELECTION = [
    ("induction", "Induction / Onboarding"),
    ("safety", "Safety & Compliance"),
    ("technical", "Technical Skills"),
    ("leadership", "Leadership Development"),
    ("hr_payroll", "HR & Payroll Systems"),
    ("customer_service", "Customer Service"),
    ("it_digital", "IT & Digital Tools"),
    ("certification_prep", "Certification Preparation"),
    ("soft_skills", "Soft Skills & Communication"),
]

ATTENDANCE_STATUS_SELECTION = [
    ("present", "Present"),
    ("absent", "Absent"),
    ("late", "Late Arrival"),
    ("excused", "Excused Absence"),
    ("incomplete", "Incomplete Attendance"),
]

TRAINING_STATE_SELECTION = [
    ("planned", "Planned"),
    ("ongoing", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]


class HrPayrollDemoTraining(models.Model):
    _name = "hr.payroll.demo.training"
    _description = "HR Demo Training Session"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc"
    _rec_name = "name"

    name = fields.Char(required=True)
    training_type = fields.Selection(TRAINING_TYPE_SELECTION, required=True, default="technical")
    trainer_name = fields.Char("Trainer / Facilitator")
    trainer_employee_id = fields.Many2one("hr.employee", "Internal Trainer")
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    duration_hours = fields.Float("Duration (Hours)", default=8.0)
    location = fields.Char("Venue / Location")
    max_participants = fields.Integer("Max Participants", default=20)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    state = fields.Selection(TRAINING_STATE_SELECTION, default="planned", required=True)
    notes = fields.Text("Notes / Objectives")
    attendance_ids = fields.One2many("hr.payroll.demo.training.attendance", "training_id", "Attendance")

    participant_count = fields.Integer("Participants", compute="_compute_stats")
    present_count = fields.Integer("Present", compute="_compute_stats")
    absent_count = fields.Integer("Absent", compute="_compute_stats")
    pass_rate = fields.Float("Pass Rate (%)", compute="_compute_stats")
    certified_count = fields.Integer("Certified", compute="_compute_stats")

    @api.depends("attendance_ids", "attendance_ids.attendance_status", "attendance_ids.passed", "attendance_ids.certification_issued")
    def _compute_stats(self):
        for rec in self:
            att = rec.attendance_ids
            rec.participant_count = len(att)
            rec.present_count = len(att.filtered(lambda a: a.attendance_status in ("present", "late")))
            rec.absent_count = len(att.filtered(lambda a: a.attendance_status in ("absent", "excused", "incomplete")))
            passed = att.filtered(lambda a: a.passed)
            rec.pass_rate = (len(passed) / len(att) * 100) if att else 0.0
            rec.certified_count = len(att.filtered(lambda a: a.certification_issued))

    def action_mark_completed(self):
        self.write({"state": "completed"})

    def action_mark_cancelled(self):
        self.write({"state": "cancelled"})

    def action_mark_ongoing(self):
        self.write({"state": "ongoing"})


class HrPayrollDemoTrainingAttendance(models.Model):
    _name = "hr.payroll.demo.training.attendance"
    _description = "HR Demo Training Attendance Record"
    _order = "training_id, employee_id"

    training_id = fields.Many2one("hr.payroll.demo.training", required=True, ondelete="cascade", index=True)
    employee_id = fields.Many2one("hr.employee", required=True, ondelete="cascade", index=True)
    department_id = fields.Many2one(related="employee_id.department_id", store=True, readonly=True)
    job_id = fields.Many2one(related="employee_id.job_id", store=True, readonly=True)
    attendance_status = fields.Selection(ATTENDANCE_STATUS_SELECTION, default="present", required=True)
    score = fields.Float("Assessment Score (%)", digits=(5, 1))
    passed = fields.Boolean("Passed")
    certification_issued = fields.Boolean("Certificate Issued")
    certificate_number = fields.Char("Certificate No.")
    notes = fields.Text()

    training_type = fields.Selection(related="training_id.training_type", store=True, readonly=True)
    training_date_start = fields.Date(related="training_id.date_start", store=True, readonly=True)
    company_id = fields.Many2one(related="training_id.company_id", store=True, readonly=True)
