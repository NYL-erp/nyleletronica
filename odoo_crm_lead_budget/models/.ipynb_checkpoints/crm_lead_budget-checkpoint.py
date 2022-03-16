# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    budget_count = fields.Integer(
        'Quotations',
        compute='_compute_budget_count',
        readonly=True
    )
    
    purchase_requisition_count = fields.Integer(
        'Acuerdos de Compra',
        compute='_compute_purchase_requisition_count',
        readonly=True
    )
    
    def _compute_budget_count(self):
        for rec in self:
            rec.budget_count = self.env['quotation.budget'].search_count([('crm_lead_id', '=', self.id)])
            
    def _compute_purchase_requisition_count(self):
        for rec in self:
            rec.purchase_requisition_count = self.env['purchase.requisition'].search_count([('crm_lead_id', '=', self.id)])

    def action_view_crm_lead_budget(self):
        context = self.env.context
        budget_ids = self.env['quotation.budget'].search([('crm_lead_id', '=', self.id)])
        view_form_id = [(self.env.ref('odoo_budget_quotation.quotation_budget_form_view').id, 'form')]
        view_mode = 'form'
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Presupuestos',
            'view_type': 'form',
            'view_mode': view_mode,
            'res_model': 'quotation.budget',
            'domain': [('crm_lead_id', '=', self.id)],
            'context': {
                'default_crm_lead_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_partner_invoice_id': self.partner_id.id,
                'default_partner_shipping_id': self.partner_id.id,
                'default_pricelist_id': self.partner_id.property_product_pricelist.id or 1,
                'charge_order_line_from_budget': True,
                'default_team_id': self.team_id.id,
            },
            'target': 'current',
        }
        if len(budget_ids) > 1:
            action.update({
                'view_mode': 'tree,form',
                'views': [
                    (self.env.ref('odoo_crm_lead_budget.quotation_budget_tree_view').id, 'tree'),
                    (self.env.ref('odoo_budget_quotation.quotation_budget_form_view').id, 'form'),
                ],
            })
        else:
            if len(budget_ids) == 1:
                action.update({'res_id': budget_ids[0].id,})
            action.update({
                'view_id': self.env.ref('odoo_budget_quotation.quotation_budget_form_view').id,
            })
        return action

    
    
    def action_view_crm_lead_purchase_requisition(self):
        context = self.env.context
        purchase_requisition_ids = self.env['purchase.requisition'].search([('crm_lead_id', '=', self.id)])
        view_form_id = [(self.env.ref('purchase_requisition.view_purchase_requisition_form').id, 'form')]
        view_mode = 'form'
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Acuerdos de Compra',
            'view_type': 'form',
            'view_mode': view_mode,
            'res_model': 'purchase.requisition',
            'domain': [('crm_lead_id', '=', self.id)],
            'context': {
                'default_crm_lead_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
            'target': 'current',
        }
        if len(purchase_requisition_ids) > 1:
            action.update({
                'view_mode': 'tree,form',
                'views': [
                    (self.env.ref('purchase_requisition.view_purchase_requisition_tree').id, 'tree'),
                    (self.env.ref('purchase_requisition.view_purchase_requisition_form').id, 'form'),
                ],
            })
        else:
            if len(purchase_requisition_ids) == 1:
                action.update({'res_id': purchase_requisition_ids[0].id,})
            action.update({
                'view_id': self.env.ref('purchase_requisition.view_purchase_requisition_form').id,
            })
        return action