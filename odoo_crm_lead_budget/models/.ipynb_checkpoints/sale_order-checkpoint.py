# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        res = super(SaleOrderLine, self)._compute_margin()
        for line in self:
            if line.order_id.quotation_budget_id:
                for budget_line in line.order_id.quotation_budget_id.order_line:
                    if budget_line.product_id == line.product_id:
                        line.margin = (line.price_unit - (budget_line.po_line_cost + (budget_line.po_line_cost * budget_line.import_cost_term/100))) * line.product_uom_qty
                        line.margin_percent = line.price_subtotal and line.margin/line.price_subtotal
        return res
