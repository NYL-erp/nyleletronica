# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_budget_id = fields.Many2one(
        'quotation.budget',
        string='Quotation Budget',
        copy=False,
    )

    def action_view_quotation_budget(self):
        action = self.env["ir.actions.actions"]._for_xml_id("odoo_budget_quotation.action_quotations_budget")
        action['domain'] = [('id', '=', self.quotation_budget_id.id)]
        return action
