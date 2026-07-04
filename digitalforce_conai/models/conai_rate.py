from odoo import api, fields, models


class ConaiRate(models.Model):
    _name = 'conai.rate'
    _description = 'Tariffa CONAI'
    _order = 'band_id, date_from desc'

    band_id = fields.Many2one('conai.band', string='Fascia',
                               required=True, ondelete='cascade')
    material_id = fields.Many2one(related='band_id.material_id',
                                   store=True, string='Materiale')
    date_from = fields.Date(string='Valido dal', required=True)
    rate_per_tonne = fields.Float(
        string='Tariffa (€/t)', required=True, digits=(10, 4),
        help="Contributo CONAI in EUR per tonnellata di materiale da imballaggio."
    )
    rate_per_kg = fields.Float(
        string='Tariffa (€/kg)', compute='_compute_rate_per_kg',
        digits=(10, 6), store=True,
    )

    @api.depends('rate_per_tonne')
    def _compute_rate_per_kg(self):
        for rec in self:
            rec.rate_per_kg = rec.rate_per_tonne / 1000.0
