from odoo import SUPERUSER_ID, _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('x_studio_address_id'):
    #             vals['name'] = vals.get('x_studio_address_id')
    #     return super().create(vals_list)
    #
    # def write(self, vals):
    #     if vals.get('x_studio_address_id'):
    #         vals['name'] = vals.get('x_studio_address_id')
    #     return super().write(vals)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Start with x_studio_address_id if exists
            name_parts = []
            if vals.get('x_studio_address_id'):
                name_parts.append(vals['x_studio_address_id'])

            # Append attention if exists
            if vals.get('x_studio_attention'):
                name_parts.append(f"ATTN: {vals['x_studio_attention']}")

            # Combine into final name
            if name_parts:
                vals['name'] = ', '.join(name_parts)

        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            # Build name from scratch
            name_parts = []

            # Use new x_studio_address_id if in vals, else existing value
            address = vals.get('x_studio_address_id', record.x_studio_address_id)
            if address:
                name_parts.append(address)

            # Use new x_studio_attention if in vals, else existing value
            attention = vals.get('x_studio_attention', record.x_studio_attention)
            if attention:
                name_parts.append(f"ATTN: {attention}")

            # Set final name
            if name_parts:
                vals['name'] = ', '.join(name_parts)

        return super().write(vals)



