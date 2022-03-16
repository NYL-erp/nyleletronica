# -*- coding: utf-8 -*-
{
    'name': 'Odoo CRM Lead Budget',
    'summary': 'Odoo CRM Lead Budget',
    'description': """
        Odoo CRM Lead Budget
    """,
    'author': "Todoo SAS",
    'website': 'www.todoo.co',
    'license': 'OPL-1',
    'category': 'Sale',
    'version': '2.0.0',
    'images' : [],
    'depends': [
        'odoo_budget_quotation',
        'crm',
        'purchase_requisition',
        'sale_crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/action_generate_purchase_orders.xml',
        'views/crm_lead_budget.xml',
        'views/quotation_budget.xml',
        'views/purchase_requisition.xml',
        
    ],
    'installable': True,
    'application': True,
}
