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
        form_view = [(self.env.ref('odoo_budget_quotation.quotation_budget_form_view').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = self.quotation_budget_id.id
        return action
