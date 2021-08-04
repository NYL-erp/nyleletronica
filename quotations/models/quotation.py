from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class Cotizador(models.Model):
    _name = 'quotation'
    
    importacion = fields.Integer('Importacion') #Porcentaje
    descuento = fields.Integer('Descuento') #Porcentaje
    TRM = fields.Integer('TRM') #Entero
    utilidad = fields.Integer('Utilidad') #Porcentaje
    factor = fields.Integer('Factor') #Entero

    # Factores de cotizacion -> pestaña en terceros 

    # Item Producto, Descripcion, Cantidad, Valor venta unitario, valor total de venta, proveedor, costo unitario, costo total, Neto, total neto
    
