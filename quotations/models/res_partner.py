# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    importacion = fields.Integer('Importacion') #Porcentaje
    descuento = fields.Integer('Descuento') #Porcentaje
    TRM = fields.Integer('TRM') #Entero
    utilidad = fields.Integer('Utilidad') #Porcentaje
    factor = fields.Integer('Factor') #Entero