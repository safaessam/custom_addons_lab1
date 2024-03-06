# models/hms_patient.py


from odoo import fields, models, api


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char(string='Name')
    capacity = fields.Integer(string='Capacity')
    is_opened = fields.Boolean(string='Is Opened')
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')


class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = "first_name"

    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    image = fields.Binary(string='Image')


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = "first_name"

    STATES = [
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ]

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History', compute='_compute_history', store=True)
    cr_ratio = fields.Float(string='CR Ratio', required=False)
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], string='Blood Type')
    pcr = fields.Boolean(string='PCR', compute='_compute_pcr', store=True)
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True, readonly=False)
    department_id = fields.Many2one('hms.department', string='Department')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', readonly=True)
    state = fields.Selection(STATES, string='State', default='undetermined', track_visibility='onchange')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log')
    active = fields.Boolean(default=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                patient.age = today.year - patient.birth_date.year
            else:
                patient.age = 0

    @api.depends('age')
    def _compute_history(self):
        for patient in self:
            if patient.age >= 50:
                patient.history = patient.history  # Define the patient's history logic here

    @api.depends('age')
    def _compute_pcr(self):
        for patient in self:
            if patient.age < 30:
                patient.pcr = True
            else:
                patient.pcr = False

    def write(self, values):
        if 'state' in values:
            self._create_log_record(values['state'])
        return super(HmsPatient, self).write(values)

    def _create_log_record(self, state):
        for patient in self:
            log_vals = {
                'patient_id': patient.id,
                'created_by': self.env.user.id,
                'date': fields.Datetime.now(),
                'description': f'State changed to {state}'
            }
            self.env['hms.patient.log'].create(log_vals)


class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'
    _rec_name = "patient_id"

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created By', readonly=True, required=True,
                                 default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', default=fields.Datetime.now(), readonly=True, required=True)
    description = fields.Text(string='Description')