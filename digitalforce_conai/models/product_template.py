from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    conai_line_ids = fields.One2many(
        'conai.product.line', 'product_tmpl_id',
        string='Materiali CONAI',
        help="Definire una riga per ogni componente di materiale da imballaggio. "
             "Per imballaggi compositi, aggiungere più righe.",
    )
    is_conai_product = fields.Boolean(
        string='È un prodotto di contributo CONAI',
        help="Contrassegnare questo prodotto come prodotto di contributo CONAI. "
             "Questi prodotti vengono iniettati automaticamente.",
    )
