from odoo import fields, models


class ConaiMaterial(models.Model):
    _name = 'conai.material'
    _description = 'Materiale CONAI'
    _order = 'sequence, name'

    name = fields.Char(string='Materiale', required=True, translate=True)
    code = fields.Char(string='Codice tecnico', required=True)
    sequence = fields.Integer(default=10)
    band_ids = fields.One2many('conai.band', 'material_id', string='Fasce')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Il codice materiale deve essere univoco.'),
    ]
