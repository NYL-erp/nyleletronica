# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    def _get_custom_parent_categ_id(self, categ):
        return categ.parent_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('categ_id'):
                product_categ_id = self.env['product.category'].browse(vals.get('categ_id'))
                supplier_lst = []
                seller_to_add = 5 - len(vals.get('seller_ids')) if vals.get('seller_ids') else 5
                supplier_ids = product_categ_id.category_suplier_ids[:seller_to_add]
                len_seller_to_add = seller_to_add
                while product_categ_id.parent_id:
                    if len_seller_to_add > 0:
                        product_categ_id = product_categ_id.parent_id
                        supplier_ids += product_categ_id.category_suplier_ids[:len_seller_to_add]
                        len_seller_to_add -= len(supplier_ids)
                    else:
                        break;
                for supplier in supplier_ids[:seller_to_add]:
                    supplier_lst.append((0, 0, {
                        'name': supplier.id,
                        'price': 1.0,
                    }))
                if vals.get('seller_ids'):
                    vals['seller_ids'] += supplier_lst
                else:
                    vals['seller_ids'] = supplier_lst
        return super(ProductTemplate, self).create(vals_list)

