from odoo import api, fields, models


class ConaiSetupWizard(models.TransientModel):
    _name = 'conai.setup.wizard'
    _description = 'Configurazione iniziale CONAI'

    account_id = fields.Many2one(
        'account.account', string='Conto ricavi CONAI',
        help="Conto utilizzato per le righe di contributo CONAI in fattura.",
    )
    default_tax_id = fields.Many2one(
        'account.tax', string='IVA predefinita sulle righe CONAI',
        domain=[('type_tax_use', '=', 'sale'), ('active', '=', True)],
        help="IVA applicata sulle righe CONAI. Il CONAI non è un'imposta — l'IVA si applica in aggiunta.",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        tax_22 = self.env['account.tax'].search([
            ('type_tax_use', '=', 'sale'),
            ('amount', '=', 22),
            ('active', '=', True),
        ], limit=1)
        if tax_22:
            res['default_tax_id'] = tax_22.id
        return res

    def action_confirm(self):
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('digitalforce_conai.account_id', self.account_id.id)
        ICP.set_param('digitalforce_conai.default_tax_id',
                      self.default_tax_id.id if self.default_tax_id else False)
        if self.default_tax_id:
            bands_without_tax = self.env['conai.band'].search([
                ('default_tax_id', '=', False)
            ])
            bands_without_tax.write({'default_tax_id': self.default_tax_id.id})
        return {'type': 'ir.actions.act_window_close'}
