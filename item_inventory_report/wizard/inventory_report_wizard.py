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

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="Inventory At Date",required=True)
    type = fields.Selection([('all_products','All Products'),
                             ('specific_products','Specific Products'),
                             ('special_products','Special Products'),
                             ('standard_products','Standard Products')],
                            default="all_products",string="Type",required=True)
    product_ids = fields.Many2many('product.product', string='Products')

    @api.onchange('start_date')
    def onchange_start_date(self):
        if self.start_date:

            self.end_date  = self.start_date+ relativedelta(years=1,days=-1)
            # self.end_date  = self.start_date + relativedelta(months=12, days=-1)
    @api.onchange('end_date')
    def onchange_end_date(self):
        if  self.end_date:
            # self.start_date  = self.end_date + relativedelta(months=-12, days=1)
            self.start_date  = self.end_date + relativedelta(years=-1,days=1)
            # self.start_date  = self.end_date + relativedelta(months=-12, days=1)

# end date should be greater than start date
# end date shouldn't be exceed from current date.
#difference should be of 12 months.
    def print_inventory_report(self):
        data = {}

        if self.start_date > self.end_date:
            raise UserError(_("End date must be after start date."))
        if self.end_date > fields.Date.today():
            raise UserError(_("End date shouldn't exceed the current date."))
        if (self.end_date - self.start_date) != relativedelta(years=1, days=-1):
            raise UserError(_("The difference between Start Date and End Date must be exactly 12 months."))

        if self.type == 'all_products':
            product_ids = self.env['product.product'].search([])
        elif self.type == 'standard_products':
            product_ids = self.env['product.product'].search([('x_studio_stdspc', '=', 'STD')])
        elif self.type == 'special_products':
            product_ids = self.env['product.product'].search([('x_studio_stdspc', '=', 'SPC')])
        else:
            product_ids = self.product_ids

        product_ids_list = [p.id for p in product_ids] if product_ids else []

        data.update({
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_ids': product_ids_list,
        })

        return self.env.ref('item_inventory_report.action_report_inventory_template').report_action(self, data=data)





    # def print_inventory_report(self):
    #
    #     data = {}
    #
    #     if self.start_date > self.end_date:
    #         raise UserError(_("End date must be after start date."))
    #
    #     if self.end_date > fields.Date.today():
    #         raise UserError(_("End date shouldn't be exceed from current date."))
    #
    #     if (self.start_date - self.end_date) != relativedelta(months=12):
    #         raise UserError(_("The difference between Start Date and End Date must be exactly 12 months."))
    #
    #     if self.type == 'all_products':
    #         product_ids = self.env['product.product'].search([])
    #
    #     elif self.type == 'standard_products':
    #         product_ids = self.env['product.product'].search([('x_studio_stdspc','=','STD')])
    #
    #     elif self.type == 'special_products':
    #         product_ids = self.env['product.product'].search([('x_studio_stdspc','=','SPC')])
    #     else:
    #         product_ids = self.product_ids
    #
    #
    #
    #     data.update({'start_date': self.start_date, 'end_date': self.end_date,'product_ids':product_ids.ids})
    #
    #
    #     return self.env.ref('item_inventory_report.action_report_inventory_template').report_action(self, data=data)
