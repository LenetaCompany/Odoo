from odoo import models, fields, api

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
import calendar
from odoo.exceptions import UserError


class ItemInventoryReportDocuments(models.AbstractModel):
    _name = 'report.item_inventory_report.inventory_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data", data)
        start_date = False
        end_date = False

        if data['start_date']:
            start_date = datetime.datetime.strptime(str(data['start_date']), '%Y-%m-%d').date()
        if data['end_date']:
            end_date = datetime.datetime.strptime(str(data['end_date']), '%Y-%m-%d').date()
        data_dict = []

        product_ids = self.env['product.product'].with_context(from_date=start_date, to_date=end_date).browse(
            data['product_ids'])

        # res = product_ids._compute_quantities_dict()

        for product in product_ids:
            default_code = product.default_code
            location_ids = self.env['stock.location'].search([('usage', '=', 'internal')], limit=2)
            move_lines = self.env['stock.move.line'].search([('date', '>=', data['start_date']), ('date', '<=', data['end_date']),
                                                  ('product_id','=',product.id),('state','=','done')])
            warehouse1_in_qty = sum(move_lines.filtered(lambda x:x.location_dest_id.id == location_ids[1].id).mapped('qty_done'))
            warehouse1_out_qty = sum(move_lines.filtered(lambda x:x.location_id.id == location_ids[1].id).mapped('qty_done'))

            warehouse2_in_qty = sum(move_lines.filtered(lambda x:x.location_dest_id.id == location_ids[0].id).mapped('qty_done'))
            warehouse2_out_qty = sum(move_lines.filtered(lambda x:x.location_id.id == location_ids[0].id).mapped('qty_done'))

            warehouse1_qty = warehouse1_in_qty - warehouse1_out_qty
            warehouse2_qty = warehouse2_in_qty - warehouse2_out_qty

            available_qty = warehouse1_qty + warehouse2_qty

            qty_sold_last_12_mo = sum(self.env['sale.report'].search(
                [('date', '>=', data['start_date']), ('date', '<=', data['end_date']),
                 ('product_id', '=', product.id)]).mapped('product_uom_qty'))

            avg_use_per_month = round(qty_sold_last_12_mo / 12, 2)

            if avg_use_per_month > 0 and available_qty > 0:
                months_of_stock = round((available_qty / avg_use_per_month),2)  # fixme available qty should be between start date and end date
            else:
                months_of_stock = available_qty if available_qty >= 0 else 0

            data_dict.append({
                'default_code': default_code,
                'available_qty': available_qty,
                'warehouse1_qty': warehouse1_qty,
                'warehouse2_qty': warehouse2_qty,
                'qty_sold_last_12_mo': qty_sold_last_12_mo,
                'avg_use_per_month': avg_use_per_month,
                'months_of_stock': months_of_stock,
            })

        return {
            'doc_ids': docids,
            'doc_model': 'item.inventory.report.wizard',
            'docs': data_dict,
            'start_date': start_date,
            'end_date': end_date,
        }
