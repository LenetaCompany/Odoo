
from decimal import Decimal
from odoo import api, fields, models


# Sales Order Unit Price – Always Round Up to Two Decimal Places (#44266) , Fawad , 15 Oct 2026
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _reset_price_unit(self):
        self.ensure_one()

        line = self.with_company(self.company_id)

        price = line._get_display_price()

        product_taxes = line.product_id.taxes_id._filter_taxes_by_company(
            line.company_id
        )

        price_unit = line.product_id._get_tax_included_unit_price_from_price(
            price,
            product_taxes=product_taxes,
            fiscal_position=line.order_id.fiscal_position_id,
        )

        # Custom rule: increase price by 0.01
        price_unit = float(
            Decimal(str(price_unit)) + Decimal('0.01')
        )

        line.update({
            'price_unit': price_unit,
            'technical_price_unit': price_unit,
        })




# import math
#
# from odoo import api, models
# #
#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     def _reset_price_unit(self):
#         self.ensure_one()
#
#         line = self.with_company(self.company_id)
#
#         # Get the normal Odoo price first
#         price = line._get_display_price()
#
#         product_taxes = line.product_id.taxes_id._filter_taxes_by_company(
#             line.company_id
#         )
#
#         price_unit = line.product_id._get_tax_included_unit_price_from_price(
#             price,
#             product_taxes=product_taxes,
#             fiscal_position=line.order_id.fiscal_position_id,
#         )
#
#         # ---------------------------------------------------------
#         # Custom price rounding rule
#         #
#         # 2.00 -> 2.00
#         # 2.10 -> 2.10
#         # 2.11 -> 2.20
#         # 2.20 -> 2.20
#         # 2.21 -> 2.30
#         # 2.30 -> 2.30
#         # 2.89 -> 2.90
#         # 2.90 -> 2.90
#         # 2.91 -> 2.91
#         # 2.92 -> 2.92
#         # 3.00 -> 3.00
#         #
#         # If tenths digit is 0-8 and there are additional decimals,
#         # increase to the next tenth.
#         #
#         # If tenths digit is 9, keep the original price.
#         # ---------------------------------------------------------
#
#         if price_unit >= 0:
#             whole_part = int(price_unit)
#             decimal_part = price_unit - whole_part
#
#             tenths_digit = int(decimal_part * 10)
#
#             # Remaining amount after the tenths digit
#             hundredths_remainder = decimal_part - (tenths_digit / 10)
#
#             if tenths_digit < 9 and hundredths_remainder > 0.0000001:
#                 price_unit = whole_part + ((tenths_digit + 1) / 10)
#
#         line.update({
#             'price_unit': price_unit,
#             'technical_price_unit': price_unit,
#         })


###############################################################################################################

# from odoo import models
# from odoo.tools import float_round


# class ProductPricelistItem(models.Model):
#     _inherit = 'product.pricelist.item'
#
#     def _compute_price(self, *args, **kwargs):
#         """Apply Leneta's pricing rule: the final price computed by a
#         pricelist rule is always rounded UP to the next cent (CEILING),
#         e.g. 85.025 -> 85.03, 57.494775 -> 57.50.
#
#         The precision follows the 'Product Price' decimal accuracy, so the
#         value stored on sale order lines, eCommerce and POS is already
#         rounded and subtotals are computed from the rounded unit price.
#         """
#         price = super()._compute_price(*args, **kwargs)
#         # Empty self = no pricelist rule matched (plain list price): leave as is.
#         if not self or not price:
#             return price
#         digits = self.env['decimal.precision'].precision_get('Product Price')
#         # float_round's 'UP' method already corrects floating-point noise
#         # (e.g. 4.784000000000001 -> 4.79, 2.8199999999 -> 2.82).
#         return float_round(price, precision_digits=digits, rounding_method='UP')

