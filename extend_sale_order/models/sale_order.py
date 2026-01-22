from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_description_always = fields.Text(
        string="Description",
        compute="_compute_description_always",
        store=False
    )

    @api.depends('product_id', 'name')
    def _compute_description_always(self):
        for line in self:
            product_name = line.product_id.display_name if line.product_id else ''
            line_name = line.name or ''

            if product_name and line_name:
                # Avoid duplication
                if line_name.strip() == product_name.strip():
                    line.x_description_always = product_name
                else:
                    line.x_description_always = f"{product_name}: {line_name}"
            else:
                line.x_description_always = product_name or line_name

##############################################################################################
# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     @api.model
#     def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
#         args = args or []
#
#         if name:
#             args = ['|', ('default_code', operator, name), ('name', operator, name)] + args
#
#         return super()._name_search(
#             name='',
#             args=args,
#             operator=operator,
#             limit=limit,
#             name_get_uid=name_get_uid
#         )
#
# class ProductProduct(models.Model):
#         _inherit = "product.product"
#
#         def name_get(self):
#             result = []
#             for product in self:
#                 name = product.name or ''
#                 if product.default_code:
#                     name = f"[{product.default_code}] {name}"
#                 result.append((product.id, name))
#             return result

from odoo import models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if name:
            args = ['|', ('default_code', operator, name), ('name', operator, name)] + args

        products = self.search(args, limit=limit)
        return products.name_get()

    def name_get(self):
        result = []
        for product in self:
            name = product.name or ''
            if product.default_code:
                name = f"[{product.default_code}] {name}"
            result.append((product.id, name))
        return result
