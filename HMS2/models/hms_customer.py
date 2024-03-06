from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class HmsCustomer(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(required=True)
    related_patient_id = fields.Many2one("hms.patient", "Related ID Patient")

    @api.constrains('email', 'related_patient_id')
    def _check_unique_email(self):
        for partner in self:
            if partner.related_patient_id:
                domain = [('id', '!=', partner.id),
                          ('related_patient_id', '=', partner.related_patient_id.id)]
                if self.env['res.partner'].search_count(domain) > 0:
                    raise ValidationError(
                        _('This email is already assigned to a different customer.'))

    # @api.multi
    # def unlink(self):
    #     for partner in self:
    #         # Check if the partner is linked to any patient
    #         if partner.patient_ids:
    #             raise UserError(_("You cannot delete a customer linked to a patient."))
    #     return super(ResPartner, self).unlink()

        # def unlink(self)
        # for rec in self:
        #     if len(rec.related_patient_id) != 0 :
        #         raise UserError('You can\'t delete a customer that is related to patient')
        #     return super().unlink()

# from odoo import models , fields , api
# from odoo.exceptions import ValidationError
# from datetime import date


# class ITIProductTemplate(models.Model):

#     _inherit = 'product.template'


#     barcode = fields.Char(required=True)
#     barcode2 = fields.Char()
#     standard_price = fields.Float(default = 10.5)
