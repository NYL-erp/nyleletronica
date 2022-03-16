# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    budget_order_line_id = fields.Many2one(
        'sale.order.line',
        string='Budget Order Line',
        copy=False
    )

    def name_get(self):
        result = []
        if self._context.get('quotation_budget_po_line') or self._context.get('params') and self._context.get('params').get('model') == 'quotation.budget':
            for line in self:
                currency = line.order_id.currency_id
                formated_amount = tools.format_decimalized_amount(line.price_unit, currency)
                line_name = str(formated_amount) +' ('+ line.order_id.partner_id.name + ')'
                result.append((line.id, line_name))
        return result

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('order_display_bdgt'):
            ctx = self._context.copy()
            order = ctx['order_display_bdgt']
        return super(PurchaseOrderLine, self)._search(args=args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
