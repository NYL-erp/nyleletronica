# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    is_created_from_budget_quotation = fields.Boolean(
        string='Created From Budget Quotation',
        default=False,
        copy=False,
    )

    def _prepare_budget_po_vals(self, supplier):
        return {
            'partner_id': supplier.id,
            'date_order': fields.Datetime.now(),
            'currency_id': self.currency_id.id,
            'picking_type_id': self.picking_type_id.id,
            'user_id': self.user_id.id,
            'requisition_id': self.id,
        }

    def _prepare_budget_po_line_vals(self, line, purchase_order, supplier):
        domain = [
            ('product_tmpl_id', '=', line.product_id.id),
            ('name', '=', supplier.id)
        ]
        price = self.env['product.supplierinfo'].search(domain, limit=1).mapped('price')[0]
        return {
            'name': line.product_description_variants,
            'product_id': line.product_id.id,
            'product_uom': line.product_id.uom_po_id.id,
            'product_qty': line.product_qty,
            'price_unit': price,
            'order_id': purchase_order.id,
            'budget_order_line_id': line.budget_order_line_id.id,
        }

    def _create_budget_purchase_order(self):
        suppliers  = self.line_ids.mapped('product_id.seller_ids.name')
        purchase_order_dict = {}
        PurchaseOrderObj = self.env['purchase.order']
        PurchaseOrderLineObj = self.env['purchase.order.line']
        for line in self.line_ids:
            suppliers = line.mapped('product_id.seller_ids.name')
            for supplier in suppliers:
                if supplier.id not in purchase_order_dict:
                    po_vals = self._prepare_budget_po_vals(supplier)
                    purchase_order = PurchaseOrderObj.create(po_vals)
                    purchase_order_dict.update({
                        supplier.id: purchase_order
                    })
                    po_line_vals = self._prepare_budget_po_line_vals(line, purchase_order,supplier)
                    PurchaseOrderLineObj.create(po_line_vals)
                else:
                    purchase_order = purchase_order_dict[supplier.id]
                    po_line_vals = self._prepare_budget_po_line_vals(line, purchase_order,supplier)
                    PurchaseOrderLineObj.create(po_line_vals)
        return purchase_order_dict

    def action_in_progress(self):
        res = super(PurchaseRequisition, self).action_in_progress()
        if self.is_created_from_budget_quotation:
            self._create_budget_purchase_order()
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.requisition.line'

    budget_order_line_id = fields.Many2one(
        'sale.order.line',
        string='Budget Order Line',
        copy=False
    )


