# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    crm_lead_id = fields.Many2one('crm.lead', string='Crm Oportunidad')
    
    
    def action_generate_purchase_orders(self):
        return {
            'name': 'Generar Presupuestos',
            'res_model': 'wizard.purchase.requisition.generate.po',
            'view_mode': 'form',
            'context': {
                'active_model': 'purchase.requisition',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }