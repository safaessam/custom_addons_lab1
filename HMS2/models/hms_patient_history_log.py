from odoo import models, fields


class HmsPatientHistoryLog(models.Model):
    _name = "hms.patient.history.log"

    # created_by = fields.Char()
    # date = fields.Datetime()
    description = fields.Text()
    patient_name = fields.Many2one("hms.patient")
