# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    category_suplier_ids = fields.Many2many(
        'res.partner',
        string='Suppliers'
    )
    
    import_cost_term = fields.Float(
        'Import Cost %',
    )
    discount_cost_term = fields.Float(
        'Discount Cost %',
    )
    utility_cost_term = fields.Float(
        'Utility Cost %',
    )
    factor_cost_term = fields.Float(
        'Factor Cost %',
    )
