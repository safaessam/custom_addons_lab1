from odoo import models, fields


class Doctor(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'First_name'

    First_name = fields.Char(size=100, string="Doctor First Name")
    Last_name = fields.Char(size=100, string="Doctor Last Name")
    image = fields.Image()
