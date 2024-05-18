# -*- coding: utf-8 -*-

from odoo import fields, models, _,api
import base64
import datetime
from email.utils import formataddr
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class ItemInventoryReportWizard(models.TransientModel):
    _name = "item.inventory.report.wizard"
    _description = "Item Inventory Report Wizard"

    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)
    type = fields.Selection([('all_products','All Products'),('specific_products','Specific Products')],default="all_products",string="Type",required=True)
    product_ids = fields.Many2many('product.product', string='Products')

    @api.onchange('start_date')
    def onchange_start_date(self):
        if  self.start_date:
            self.end_date  = self.start_date + relativedelta(months=12, days=-1)
        else:
            self.end_date = False


    def print_inventory_report(self):

        data = {}

        if self.type == 'all_products':
            product_ids = self.env['product.product'].search([])
        else:
            product_ids = self.product_ids


        data.update({'start_date': self.start_date, 'end_date': self.end_date,'product_ids':product_ids.ids})


        return self.env.ref('item_inventory_report.action_report_inventory_template').report_action(self, data=data)
