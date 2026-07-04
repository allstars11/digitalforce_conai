from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ConaiExemption(models.Model):
    _name = 'conai.exemption'
    _description = 'Esenzione CONAI Partner'
    _rec_name = 'material_id'

    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, ondelete='cascade')
    material_id = fields.Many2one(
        'conai.material', string='Materiale', required=True)
    exemption_rate = fields.Float(
        string='Esenzione %', required=True, digits=(5, 2),
        help="Percentuale di contributo CONAI esente per questo partner "
             "su questo materiale. Es. 89 significa sconto dell'89%% sulla riga CONAI.",
    )

    _sql_constraints = [
        ('partner_material_unique', 'UNIQUE(partner_id, material_id)',
         'Una sola esenzione per materiale per partner.'),
    ]

    @api.constrains('exemption_rate')
    def _check_exemption_rate(self):
        for rec in self:
            if not (0 <= rec.exemption_rate <= 100):
                raise ValidationError(
                    _("Il tasso di esenzione deve essere compreso tra 0 e 100%%."))

    def get_exemption(self, partner, material):
        exemption = self.search([
            ('partner_id', '=', partner.id),
            ('material_id', '=', material.id),
        ], limit=1)
        return exemption.exemption_rate if exemption else 0.0
