from odoo import fields, models


class ConaiBand(models.Model):
    _name = 'conai.band'
    _description = 'Fascia Materiale CONAI'
    _order = 'material_id, sequence, name'

    name = fields.Char(string='Fascia', required=True, translate=True)
    code = fields.Char(string='Codice tecnico', required=True)
    material_id = fields.Many2one('conai.material', string='Materiale',
                                   required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    rate_ids = fields.One2many('conai.rate', 'band_id', string='Tariffe')
    active = fields.Boolean(default=True)

    default_tax_id = fields.Many2one(
        'account.tax', string='IVA predefinita',
        domain=[('type_tax_use', '=', 'sale')],
        help="IVA applicata sulle righe CONAI per questa fascia. "
             "Il CONAI non è un'imposta — l'IVA si applica in aggiunta.",
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Il codice fascia deve essere univoco.'),
    ]

    def get_rate_at(self, date):
        """Restituisce la tariffa €/tonnellata applicabile alla data indicata."""
        self.ensure_one()
        rate = self.rate_ids.filtered(
            lambda r: r.date_from <= date
        ).sorted('date_from', reverse=True)[:1]
        return rate.rate_per_tonne if rate else 0.0
