from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'First_name'

    First_name = fields.Char(size=100, string="Patient First Name")
    Last_name = fields.Char(size=100, string="Patient Last Name")
    Email = fields.Char()
    birth_date = fields.Date()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('Blood_type_A','A'),
        ('Blood_type_B','B'),
        ('Blood_type_O','O'),
        ('Blood_type_AB','AB'),
    ])
    history = fields.Html()
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer()
    state = fields.Selection([
        ('undetermined', 'undetermined'),
        ('good', 'good'),
        ('fair', 'fair'),
        ('serious', 'serious'),
    ], default='undetermined')
# ----------------------------

    doctor_name_id = fields.Many2many('hms.doctors')
    department_name_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='department_name_id.Capacity')
    log_history_id = fields.One2many('hms.log.history', 'patient_id')

# ----------------------------
    @api.onchange('Email')
    def validate_mail(self):
        if self.Email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.Email)
            if match == None:
                raise ValidationError('Not a valid E-mail ')
# ----------------------------
    @api.model
    def create(self, vals_list):
        if not vals_list['Email']:
            vals_list['Email'] = f"{vals_list['First_name']}@gmail.com"
        patient = self.search([('Email', '=', vals_list['Email'])])
        if patient:
            raise UserError(f"{vals_list['Email']} already exists")
        return super().create(vals_list)
# ----------------------------
    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            self.age = date.today().year - self.birth_date.year
# ----------------------------
    def create_log(self):
        self.env['hms.log.history'].create({
            'created_by': self.First_name,
            'Date': date.today(),
            'Description': f'State changed to {self.state} ',
            'patient_id': self.id
        })
# ----------------------------
    @api.onchange('age')
    def changeAge(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning' : {
                    'title' : 'Age' ,
                    'message' : 'Pcr Automatic select if age < 30 ' ,
                }
            }
# ----------------------------
    @api.onchange('department_name_id')
    def changeDept(self):
            domain = [('is_opened','=',True)]
            return {
                'domain' : { 'department_name_id' : domain },
                'warning' : {
                    'title' : 'Dept' ,
                    'message' : 'you can choose with only opened dept' ,
                }
            }
# ----------------------------
    def action_undetermined(self):
        self.state = 'undetermined'
        newLog = self.env['hms.log.history'].create({'Description':'undetermined','patient_id':self.id,'Date':date.today().strftime('%Y-%m-%d')})
        self.env.cr.commit()

    def action_good(self):
        self.state = 'good'
        newLog = self.env['hms.log.history'].create({'Description':'good','patient_id':self.id,'Date':date.today().strftime('%Y-%m-%d')})
        self.env.cr.commit()

    def action_fair(self):
        self.state = 'fair' 
        newLog = self.env['hms.log.history'].create({'Description':'fair','patient_id':self.id,'Date':date.today().strftime('%Y-%m-%d')})
        self.env.cr.commit()

    def action_serious(self):
        self.state = 'serious'
        newLog = self.env['hms.log.history'].create({'Description':'serios','patient_id':self.id,'Date':date.today().strftime('%Y-%m-%d')})
        self.env.cr.commit()