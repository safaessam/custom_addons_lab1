from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class Hmspatient(models.Model):
    _name = "hms.patient"
    _rec_name = "fname"

    fname = fields.Char()
    lname = fields.Char()
    email = fields.Char()
    birthdate = fields.Date()
    age = fields.Integer()
    age2 = fields.Integer(compute="compute_age")
    address = fields.Text()
    history = fields.Text()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A', 'Type A'),
        ('B', 'Type B'),
        ('AB', 'Type AB'),
        ('O', 'Type O')
    ], string='Blood Type')

    pcr_test = fields.Boolean(string='PCR', default=False)
    image = fields.Binary(string='Image')
    patient_status = fields.Selection([
        ('undetermined', 'un'),
        ('good', 'g'),
        ('fair', 'f'),
        ('serious', 's')
    ], string='patient_status')

    depart_name = fields.Many2one("hms.department")
    depart_capcity = fields.Integer(related='depart_name.capcity')
    doctors_patient = fields.Many2many("hms.doctor")
    level_log = fields.One2many("hms.patient.history.log", "patient_name")
    partner_id = fields.Many2one(
        'res.partner', string='Customer', required=True, ondelete='restrict')

    @api.onchange('age')
    def onchange_age(self):
        if self.age and self.age < 30:
            self.pcr_test = True
            return {
                'warning': {
                    "title": "PCR CHECKED",
                    "message": "PCR has been checked automatically because age is less than 30"
                }
            }

    @api.onchange("patient_status")
    def onchange_status(self):
        if self.patient_status:
            return {
                'warning': {
                    "title": "State Changed",
                    "message": "State is changed %s" % (self.patient_status)
                }
            }

    @api.depends("birthdate")
    def compute_age(self):
        for record in self:
            if record.birthdate:
                today = date.today()
                birthdate = record.birthdate
                age2 = (today.year - birthdate.year) - ((today.month,
                                                        today.day) < (birthdate.month, birthdate.day))
                record.age2 = age2
            else:
                record.age2 = 0

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not self._validate_email(record.email):
                    raise ValidationError('Invalid email address')
                if self.search([('email', '=', record.email), ('id', '!=', record.id)]):
                    raise ValidationError('Email address must be unique')

    def _validate_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    _sql_constraints = [
        ("check_email", "UNIQUE(email)",
            "email should be unique choose another email")
    ]

    @api.onchange("history")
    def patient_history(self):
        vals = {
            "description": "history changed to %s" % (self.history),
            "patient_name": self.id
        }

        self.env["hms.patient.history.log"].create(vals)
