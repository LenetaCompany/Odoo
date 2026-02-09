from odoo import SUPERUSER_ID, _, api, fields, models
# 3406 , Puran , 6 feb 2026
class Picking(models.Model):
    _inherit = "stock.picking"

    has_packages = fields.Boolean(
        'Has Packages', compute='_compute_has_packages',
        help='Check the existence of destination packages on move lines')

    def _compute_has_packages(self):
        domain = [('picking_id', 'in', self.ids), ('result_package_id', '!=', False)]
        cnt_by_picking = self.env['stock.move.line']._read_group(domain, ['picking_id'], ['__count'])
        cnt_by_picking = {picking.id: count for picking, count in cnt_by_picking}
        for picking in self:
            picking.has_packages = bool(cnt_by_picking.get(picking.id, False))
