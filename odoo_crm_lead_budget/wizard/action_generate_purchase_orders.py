# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class WizardPurchaseRequisitionGeneratePo(models.TransientModel):
    _name = 'wizard.purchase.requisition.generate.po'

    partner_ids = fields.Many2many('res.partner', string='Proveedor')
    requisition_line_ids = fields.One2many('wizard.purchase.requisition.generate.po.line', 'wizard_id', 'Productos a Cotizar', readonly=False, required=True)

    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        requisition_id = self.env[active_model].browse(active_ids)[0]
        
        line_list = []
        rec = {}
        for line in requisition_id.line_ids:
            line_list.append((0,0,{
				'requisition_line_id' : line.id,
                'requisition_id' : line.requisition_id.id,
				'product_name' : line.product_id.product_tmpl_id.name,
                'product_id' : line.product_id.id,
				'product_qty' : line.product_qty,
                'product_uom' : line.product_id.product_tmpl_id.uom_po_id.id\
                    if line.product_id.product_tmpl_id.uom_po_id else line.product_id.product_tmpl_id.uom_id.id,
				'unit_price' : line.product_id.standard_price,
                'product_description': line.product_id.product_tmpl_id.description_purchase\
                    if line.product_id.product_tmpl_id.description_purchase else line.product_id.product_tmpl_id.name
			}))
        rec.update({'requisition_line_ids':line_list})
        
        partner_ids = []
        for line in requisition_id.line_ids:
            for seller in line.product_id.seller_ids:
                if seller.name.id not in partner_ids:
                    partner_ids.append((4,seller.name.id))
        
        rec.update({'partner_ids':partner_ids})
        return rec


    def purchase_requisition_generate_create_po(self):
        purchase_obj = self.env['purchase.order']
        values = []
        for supplier in self.partner_ids:
            order_line_values = []
            for product in self.requisition_line_ids:
                self.env
                if any(x.name.id == supplier.id for x in product.product_id.seller_ids):
                    order_line_values.append((0,0,{
                        'name': product.product_description,
                        'product_id': product.product_id.id,
                        'product_uom': product.product_uom,
                        'product_qty': product.product_qty,
                        'price_unit': product.unit_price,
                        'requisition_line_id': product.requisition_line_id.id
                    }))
                values = {
                    'partner_id': supplier.id,
                    'crm_lead_id': product.requisition_id.crm_lead_id.id,
                    'requisition_id': product.requisition_id.id,
                    'origin': self.env['purchase.requisition'].browse(product.requisition_id.id).name
                }
            values.update({'order_line':order_line_values})
            purchase_obj.create(values)
            #for line in self.requisition_line_ids:
            #    self.env['purchase.requisition.line'].browse(line.requisition_line_id).write({'state': 'quoted'})
        
        
    
    
class WizardPurchaseRequisitionGeneratePoLine(models.TransientModel):
    _name = 'wizard.purchase.requisition.generate.po.line'

    wizard_id = fields.Many2one('wizard.purchase.requisition.generate.po',string='Wizard ID')
    requisition_line_id = fields.Many2one('purchase.requisition.line', string="Linea de Requisición", readonly='False')
    requisition_id = fields.Many2one('purchase.requisition', string="Requisición", readonly='False')
    product_name = fields.Char('Producto a Cotizar')
    product_description = fields.Char('Producto a Cotizar')
    product_id = fields.Many2one('product.product', 'Producto')
    product_uom = fields.Integer('ID Unidad de Medida')
    product_qty = fields.Float('Cantidad Aprobada')
    unit_price = fields.Float('Precio Unitario')
    
