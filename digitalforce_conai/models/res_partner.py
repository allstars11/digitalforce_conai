from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    conai_exemption_ids = fields.One2many(
        'conai.exemption', 'partner_id',
        string='Esenzioni CONAI',
        help="Esenzioni CONAI per materiale negoziate con questo partner. "
             "Applicabile solo ai partner italiani.",
    )
    conai_exempt = fields.Boolean(
        string='Esente totalmente da CONAI',
        help="Se selezionato, nessuna riga CONAI verrà generata per questo partner.",
    )
    is_italian_partner = fields.Boolean(
        string='Partner italiano',
        compute='_compute_is_italian_partner', store=False,
    )

    @api.depends('country_id')
    def _compute_is_italian_partner(self):
        for rec in self:
            rec.is_italian_partner = rec.country_id.code == 'IT'
