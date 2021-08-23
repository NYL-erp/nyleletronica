# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Budget(models.Model):
    _name = 'quotation.budget'
    _description='Quotation Budget'
    _inherits = {'sale.order': 'sale_order_id'}
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    
    sale_order_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        required=True,
        index=True, ondelete="cascade",auto_join=True,
    )
    import_cost_term = fields.Float(
        'Import Cost %',
    )
    discount_cost_term = fields.Float(
        'Discount Cost %',
    )
    trm_cost_term = fields.Float(
        'TRM Cost %',
    )
    utility_cost_term = fields.Float(
        'Utility Cost %',
    )
    factor_cost_term = fields.Float(
        'Factor Cost %',
    )
    purchase_agreement_prsit_id = fields.Many2one(
        'purchase.requisition',
        string='Budget Purchase Agreement'
    )
    state = fields.Selection(
        selection=[
        ('draft', 'New'),
        ('confirm', 'Confirmed'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),],
        default='draft',readonly=True, copy=False, index=True, tracking=3
    )
    
    @api.onchange('partner_id')
    def _onchange_partner_id_cost_term(self):
        self.sale_order_id.onchange_partner_id()
        self.sale_order_id.onchange_partner_id_warning()
        self.import_cost_term = self.partner_id.import_cost_term
        self.discount_cost_term = self.partner_id.discount_cost_term
        self.trm_cost_term = self.partner_id.trm_cost_term
        self.utility_cost_term = self.partner_id.utility_cost_term
        self.factor_cost_term = self.partner_id.factor_cost_term

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        self.sale_order_id._onchange_pricelist_id()
    
    def _prepare_purchase_agreement_vals(self):
        requisition = self.env['purchase.requisition']
        return {
            'user_id': self.user_id.id,
            'type_id': requisition._get_type_id().id,
            'currency_id': self.currency_id.id,
            'origin': self.name,
            'picking_type_id': requisition._get_picking_in().id,
            'company_id': self.env.company.id,
            'is_created_from_budget_quotation': True,
        }
    
    def _prepare_agreement_line(self, line):
        return {
            'product_id': line.product_id.id,
            'product_description_variants': line.name,
            'product_qty': line.product_uom_qty,
            'product_uom_id': line.product_uom.id,
            'price_unit': line.price_unit,
            'budget_order_line_id': line.id,
        }
    
    def _prepare_purchase_agreement_line_vals(self):
        agreement_line_lst = []
        for line in self.order_line:
            agreement_line_lst.append((0, 0, self._prepare_agreement_line(line)))
        return agreement_line_lst
    
    def _create_purchase_aggreement_prsit(self):
        agreement_vals = self._prepare_purchase_agreement_vals()
        agreement_line_vals = self._prepare_purchase_agreement_line_vals()
        agreement_vals.update({
            'line_ids': agreement_line_vals,
        })
        return self.env['purchase.requisition'].create(agreement_vals)
    
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('quotation.budget', sequence_date=seq_date) or _('New')
        result = super(Budget, self).create(vals)
        purchase_agreement_id = result._create_purchase_aggreement_prsit()
        result.purchase_agreement_prsit_id = purchase_agreement_id.id
        return result
    
    def action_budget_confirm(self):
        self.state = 'confirm'

    def _prepare_sale_order_vals(self):
        return {
            'partner_id': self.partner_id.id,
            'date_order': fields.Datetime.now(),
            'pricelist_id': self.pricelist_id.id,
            'payment_term_id': self.payment_term_id.id,
            'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'quotation_budget_id': self.id,
        }

    def _prepare_sale_order_line_vals(self, sale_order):
        lst_so_line_vals = []
        for line in self.order_line.filtered(lambda l:l.budget_rfq_line_id):
            lst_so_line_vals.append({'name': line.name, 'sequence': 10, 'price_unit': line.price_unit, 'tax_id': [(6, 0, line.tax_id.ids)], 'discount': line.discount, 'product_id': line.product_id.id, 'product_uom_qty': line.product_uom_qty, 'product_uom': line.product_uom.id,'po_line_cost': line.po_line_cost, 'so_customer_cost': line.so_customer_cost, 'price_after_discount': line.price_after_discount, 'landed_cost': line.landed_cost, 'cost_for_quotation': line.cost_for_quotation, 'utility': line.utility, 'budget_quot_unit_price': line.budget_quot_unit_price, 'order_id': sale_order.id})
        return lst_so_line_vals

    def action_budget_create_quotation(self):
        so_vals = self._prepare_sale_order_vals()
        sale_order = self.env['sale.order'].create(so_vals)
        so_line_vals = self._prepare_sale_order_line_vals(sale_order)
        if not so_line_vals:
            raise ValidationError('There is no any budget Lines to add in Quotations.')

        so_line_id = self.env['sale.order.line'].create(so_line_vals)
        return sale_order
    
    def action_view_budget_quotations(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['domain'] = [('quotation_budget_id', '=', self.id)]
        return action

    def action_budget_cancel(self):
        self.state = 'cancel'

    def action_budget_close(self):
        self.state = 'close'
    
    def action_budget_reset_draft(self):
        self.state = 'draft'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    budget_rfq_line_id = fields.Many2one(
        'purchase.order.line',
        copy=False,
    )
    po_line_cost = fields.Float(
        'Cost',
    )
    so_customer_cost = fields.Float(
        'Customer Cost',
        store=True,
        copy=True,
    )
    price_after_discount = fields.Float(
        'Price After Discount',
        store=True,
        copy=True,
    )
    landed_cost = fields.Float(
        'Landed Cost',
    )
    cost_for_quotation = fields.Float(
        'Cost for Quotation',
        store=True,
        copy=True,
    )
    utility = fields.Float(
        'Utility',
    )
    budget_quot_unit_price = fields.Float(
        'Budget Quotation Price',
        store=True,
        copy=True,
    )

    @api.onchange('budget_rfq_line_id')
    def _onchange_budget_rfq_line(self):
        self.po_line_cost = self.budget_rfq_line_id.price_unit

    @api.onchange('budget_rfq_line_id', 'po_line_cost')
    def _onchange_so_customer_cost(self):
        for rec in self:
            rec.so_customer_cost  = 0.0
            quotation_budget_id = self.env['quotation.budget'].search([('sale_order_id', '=', rec.order_id.id)])
            if quotation_budget_id.currency_id.id == rec.budget_rfq_line_id.order_id.currency_id.id:
                rec.so_customer_cost = rec.po_line_cost * quotation_budget_id.factor_cost_term
            elif quotation_budget_id.currency_id.id != rec.budget_rfq_line_id.order_id.currency_id.id:
                rec.so_customer_cost = rec.po_line_cost * quotation_budget_id.trm_cost_term * quotation_budget_id.factor_cost_term

    @api.onchange('so_customer_cost', 'discount')
    def _onchange_price_after_discount(self):
        for line in self:
            line.price_after_discount = (line.so_customer_cost - ((line.so_customer_cost*line.discount)/ 100.00)) or 0.0

    @api.onchange('price_after_discount', 'landed_cost')
    def _onchange_cost_for_quotation(self):
        for line in self:
            line.cost_for_quotation = line.price_after_discount + line.landed_cost

    @api.onchange('so_customer_cost', 'utility')
    def _onchnage_budget_quote_unit_price(self):
        for rec in self:
            rec.budget_quot_unit_price = (rec.so_customer_cost + ((rec.so_customer_cost*rec.utility)/ 100.00)) or 0.0
            rec.price_unit = (rec.so_customer_cost + ((rec.so_customer_cost*rec.utility)/ 100.00)) or 0.0

