# -*- coding: utf-8 -*-
{
    'name': 'Odoo Budget Quotation',
    'summary': 'Odoo Budget Quotation',
    'description': """
Odoo Budget Quotation
    """,
    'author': "",
    'website': '',
    'license': 'OPL-1',
    'category': 'Sale',
    'version': '2.0.0',
    'images' : [],
    'depends': [
        'sale',
        'purchase_requisition',
        'purchase_requisition_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/res_partner_views.xml',
        'views/quotation_budget_views.xml',
        'views/product_category_views.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': True,
}
