from odoo import models , fields


class Hmsdoctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "fname"
    
    
    
    
    fname = fields.Char(required=True)
    lname = fields.Char(required=True)
    image = fields.Binary(string="Image")
    
    doctors_patient = fields.Many2many("hms.patient")
    doctors_depart = fields.Many2many("hms.department",readonly=True)