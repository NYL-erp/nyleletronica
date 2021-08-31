# -*- coding: utf-8 -*-

from odoo import fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

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
