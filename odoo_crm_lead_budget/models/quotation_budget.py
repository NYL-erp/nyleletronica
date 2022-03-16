# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Budget(models.Model):
    _inherit = 'quotation.budget'

    crm_lead_id = fields.Many2one('crm.lead', string='Crm Oportunidad')

    
    @api.model
    def default_get(self, fields):
        res = super(Budget, self).default_get(fields)
        context = dict(self._context or {})
        rec = {}
        if self._context.get('charge_order_line_from_budget'):
            lines = []
            if self._context.get('default_crm_lead_id'):
                requisition_id = self.env['purchase.requisition'].search([
                    ('crm_lead_id', '=', context.get('default_crm_lead_id')),
                    ('state', 'not in', ('draft','cancel')),
                ])
                #if not requisition_id or len(requisition_id) > 1:
                #    raise ValidationError('Debe existir un único acuerdo de compra valido para esta oportunidad.')
                for requisition_line in requisition_id.line_ids:
                    line = {
                        'product_id': requisition_line.product_id.id,
                        'name': requisition_line.product_description_variants,
                        'product_uom_qty': requisition_line.product_qty,
                    }
                    lines.append((0, 0, line))
            if lines:
                res.update({'order_line':lines})
        return res