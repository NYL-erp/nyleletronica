# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    category_suplier_ids = fields.Many2many(
        'res.partner',
        string='Suppliers'
    )
