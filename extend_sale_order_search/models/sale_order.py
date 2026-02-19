
from odoo import models, api
# 3406 , Fawad , 6 feb 2026
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if not name:
            return super().name_search(name, args, operator, limit)

        name_lower = name.strip().lower()

        Product = self.env['product.product']

        # -------------------------------------------------
        # STEP 1 : EXACT MATCH (default_code OR name)
        # -------------------------------------------------
        exact_products = Product.search([
            '|',
            ('default_code', '=ilike', name),
            ('name', '=ilike', name),
        ], limit=1)

        if exact_products:
            templates = exact_products.mapped('product_tmpl_id')
            return templates.name_get()

        # -------------------------------------------------
        # STEP 1: PREFIX MATCH (while typing)
        # -------------------------------------------------
        prefix_products = Product.search([
            '|',
            ('default_code', 'ilike', name + '%'),
            ('name', 'ilike', name + '%'),
        ], limit=limit)

        templates = prefix_products.mapped('product_tmpl_id')

        if templates:
            return templates.name_get()

        # -------------------------------------------------
        # STEP 3: fallback
        # -------------------------------------------------
        return super().name_search(name, args, operator, limit)

    def name_get(self):
        result = []
        for t in self:
            variant = t.product_variant_ids[:1]
            if variant and variant.default_code:
                result.append((t.id, f"[{variant.default_code}] {t.name}"))
            else:
                result.append((t.id, t.name))
        return result


#################################################################
###################################################################3
from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []

        if not name:
            return super().name_search(name, args, operator, limit)

        name = name.strip()

        # -------------------------------------------------
        # STEP 1 : EXACT MATCH (default_code OR name)
        # -------------------------------------------------
        exact_products = self.search([
            '|',
            ('default_code', '=ilike', name),
            ('name', '=ilike', name),
        ], limit=1)

        if exact_products:
            return exact_products.name_get()

        # -------------------------------------------------
        # STEP 2 : PREFIX MATCH (while typing)
        # -------------------------------------------------
        prefix_products = self.search([
            '|',
            ('default_code', 'ilike', name + '%'),
            ('name', 'ilike', name + '%'),
        ], limit=limit)

        if prefix_products:
            return prefix_products.name_get()

        # -------------------------------------------------
        # STEP 3 : FALLBACK
        # -------------------------------------------------
        return super().name_search(name, args, operator, limit)

    def name_get(self):
        result = []
        for product in self:
            if product.default_code:
                result.append(
                    (product.id, f"[{product.default_code}] {product.name}")
                )
            else:
                result.append((product.id, product.name))
        return result








