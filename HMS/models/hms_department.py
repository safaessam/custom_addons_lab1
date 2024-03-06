from odoo import models, fields


class Department(models.Model):
    _name = 'hms.department'
    _rec_name = 'Name'

    Name = fields.Char(size=100, string="Dapartment Name")
    Capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_name_id')
