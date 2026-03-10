from odoo import SUPERUSER_ID, _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('x_studio_address_id'):
                vals['name'] = vals.get('x_studio_address_id')
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('x_studio_address_id'):
            vals['name'] = vals.get('x_studio_address_id')
        return super().write(vals)

    # @api.onchange('x_studio_address_id')
    # def _onchange_x_studio_address_id(self):
    #     if self.x_studio_address_id:
    #         self.name = self.x_studio_address_id