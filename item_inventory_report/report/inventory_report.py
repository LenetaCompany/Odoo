from odoo import models, fields, api

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import calendar
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class ItemInventoryReportDocuments(models.AbstractModel):
    _name = 'report.item_inventory_report.inventory_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data", data)
        start_date = False
        end_date = False

        if data['start_date']:
            start_date = datetime.strptime(str(data['start_date']), '%Y-%m-%d').date()
        if data['end_date']:
            end_date = datetime.strptime(str(data['end_date']), '%Y-%m-%d').date()
        data_dict = []

        product_ids = self.env['product.product'].with_context(from_date=start_date, to_date=end_date).browse(
            data['product_ids'])

        for product in product_ids:
            default_code = product.default_code

            location_ids = self.env['stock.location'].search([('usage', '=', 'internal')], limit=2)

            move_lines = self.env['stock.move.line'].search(
                ["&", ("product_id", "=", product.id),
                 "&", ("date", ">=", "2010-11-30 19:00:00"),
                 ("date", "<=", end_date + timedelta(hours=59, minutes=59, seconds=59)),

                 ])
            w01_in = sum(
                move_lines.filtered(lambda x: x.location_dest_id.id == location_ids[0].id and x.state == 'done').mapped(
                    'qty_done'))
            w01_out = sum(
                move_lines.filtered(lambda x: x.location_id.id == location_ids[0].id and x.state == 'done').mapped(
                    'qty_done'))
            w02_in = sum(
                move_lines.filtered(lambda x: x.location_dest_id.id == location_ids[1].id and x.state == 'done').mapped(
                    'qty_done'))
            w02_out = sum(
                move_lines.filtered(lambda x: x.location_id.id == location_ids[1].id and x.state == 'done').mapped(
                    'qty_done'))

            warehouse1_qty = w01_in - w01_out
            warehouse2_qty = w02_in - w02_out

            available_qty = warehouse1_qty + warehouse2_qty

            qty_sold_last_12_mo = sum(self.env['sale.report'].search(
                [('date', '>=', data['start_date']), ('date', '<=', data['end_date']),
                 ('product_id', '=', product.id), ('state', 'not in', ['draft', 'cancel', 'sent'])]).mapped(
                'product_uom_qty'))

            avg_use_per_month = round(qty_sold_last_12_mo / 12, 2)

            if avg_use_per_month > 0 and available_qty > 0:
                months_of_stock = round((available_qty / avg_use_per_month),
                                        2)  # fixme available qty should be between start date and end date
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
