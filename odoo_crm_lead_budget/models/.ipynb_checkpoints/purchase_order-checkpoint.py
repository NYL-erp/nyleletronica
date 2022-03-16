# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    crm_lead_id = fields.Many2one('crm.lead', string='Crm Oportunidad')
    
    
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    requisition_line_id = fields.Many2one('purchase.requisition.line', string='Linea de Requisición')