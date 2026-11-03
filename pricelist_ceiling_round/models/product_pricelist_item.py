#
# from decimal import Decimal
# from odoo import api, fields, models

from decimal import Decimal, ROUND_DOWN, ROUND_UP
from odoo import models




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

        price_decimal = Decimal(str(price_unit))

        # Get the value at 2 decimal places without rounding up
        price_2 = price_decimal.quantize(
            Decimal('0.01'),
            rounding=ROUND_DOWN
        )

        # Calculate what remains after 2 decimal places
        remainder = price_decimal - price_2

        # If there is a meaningful amount after 2 decimals,
        # round up to the next 0.01.
        #
        # 63.650000000000006 -> remainder is only floating-point noise
        # 63.651              -> remainder is 0.001
        if remainder > Decimal('0.000001'):
            price_decimal = price_decimal.quantize(
                Decimal('0.01'),
                rounding=ROUND_UP
            )
        else:
            price_decimal = price_2

        price_unit = float(price_decimal)

        line.update({
            'price_unit': price_unit,
            'technical_price_unit': price_unit,
        })

################# working code ###############################
    # def _reset_price_unit(self):
    #     self.ensure_one()
    #
    #     line = self.with_company(self.company_id)
    #
    #     price = line._get_display_price()
    #
    #     product_taxes = line.product_id.taxes_id._filter_taxes_by_company(
    #         line.company_id
    #     )
    #
    #     price_unit = line.product_id._get_tax_included_unit_price_from_price(
    #         price,
    #         product_taxes=product_taxes,
    #         fiscal_position=line.order_id.fiscal_position_id,
    #     )
    #
    #     # Custom rounding:
    #     # 2 or fewer decimals -> unchanged
    #     # 3rd decimal > 0     -> round UP to 2 decimals
    #     price_unit = float(
    #         Decimal(str(price_unit)).quantize(
    #             Decimal('0.01'),
    #             rounding=ROUND_UP
    #         )
    #     )
    #
    #     line.update({
    #         'price_unit': price_unit,
    #         'technical_price_unit': price_unit,
    #     })
######## old #############################
    # def _reset_price_unit(self):
    #     self.ensure_one()
    #
    #     line = self.with_company(self.company_id)
    #
    #     price = line._get_display_price()
    #
    #     product_taxes = line.product_id.taxes_id._filter_taxes_by_company(
    #         line.company_id
    #     )
    #
    #     price_unit = line.product_id._get_tax_included_unit_price_from_price(
    #         price,
    #         product_taxes=product_taxes,
    #         fiscal_position=line.order_id.fiscal_position_id,
    #     )
    #
    #     # ---------------------------------------------------------
    #     # Apply custom rounding ONLY if the selected product
    #     # exists in the Sale Order's pricelist.
    #     # ---------------------------------------------------------
    #     pricelist = line.order_id.pricelist_id
    #     product = line.product_id
    #
    #     product_in_pricelist = pricelist.item_ids.filtered(
    #         lambda item:
    #              item.product_tmpl_id == product.product_tmpl_id
    #     )
    #     # item.product_id == product
    #     # or
    #     if product_in_pricelist:
    #         # 2 or fewer decimals -> unchanged
    #         # 3rd decimal = 0  -> unchanged
    #         # 3rd decimal > 0  -> round UP to 2 decimals
    #         #
    #         # Examples:
    #         # 57.41  -> 57.41
    #         # 57.410 -> 57.41
    #         # 57.411 -> 57.42
    #         # 57.419 -> 57.42
    #         # 57.450 -> 57.45
    #         # 57.451 -> 57.46
    #         # 57.490 -> 57.49
    #         # 57.491 -> 57.50
    #
    #         price_unit = float(
    #             Decimal(str(price_unit)).quantize(
    #                 Decimal('0.01'),
    #                 rounding=ROUND_UP
    #             )
    #         )
    #
    #     line.update({
    #         'price_unit': price_unit,
    #         'technical_price_unit': price_unit,
    #     })











#####################################################################################
# Sales Order Unit Price – Always Round Up to Two Decimal Places (#44266) , Fawad , 15 Oct 2026
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     def _reset_price_unit(self):
#         self.ensure_one()
#
#         line = self.with_company(self.company_id)
#
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
#         # Custom rule: increase price by 0.01
#         price_unit = float(
#             Decimal(str(price_unit)) + Decimal('0.01')
#         )
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

