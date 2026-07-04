from odoo import api, fields, models


class ConaiProductLine(models.Model):
    _name = 'conai.product.line'
    _description = 'Riga Materiale CONAI Prodotto'
    _order = 'product_tmpl_id, sequence'

    product_tmpl_id = fields.Many2one(
        'product.template', string='Prodotto', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    material_id = fields.Many2one(
        'conai.material', string='Materiale', required=True)
    band_id = fields.Many2one(
        'conai.band', string='Fascia', required=True,
        domain="[('material_id', '=', material_id)]",
    )
    weight_kg = fields.Float(
        string='Peso (kg/unità)', required=True, digits=(10, 6),
        help="Peso in kg di questo componente materiale per unità di prodotto. "
             "Per prodotti compositi, aggiungere una riga per materiale.",
    )

    @api.onchange('material_id')
    def _onchange_material_id(self):
        self.band_id = False
