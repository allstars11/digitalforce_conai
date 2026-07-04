from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _has_conai_lines(self):
        return any(
            l.product_id and l.product_id.product_tmpl_id.is_conai_product
            for l in self.invoice_line_ids
        )

    def _is_conai_eligible(self):
        return (
            self.move_type == 'out_invoice'
            and self.partner_id.country_id
            and self.partner_id.country_id.code == 'IT'
            and not self.partner_id.commercial_partner_id.conai_exempt
        )

    def action_generate_conai_lines(self):
        """Manual button — always regenerates, draft only."""
        for move in self:
            if not move._is_conai_eligible():
                continue
            if move.state != 'draft':
                raise UserError(
                    _("CONAI lines can only be generated on draft invoices."))
            move._generate_conai_lines()

    def _generate_conai_lines(self):
        """Remove existing CONAI lines and regenerate from scratch."""
        self.ensure_one()

        conai_account_id = self.env['ir.config_parameter'].sudo().get_param(
            'digitalforce_conai.account_id')
        conai_account = (
            self.env['account.account'].browse(int(conai_account_id))
            if conai_account_id else False
        )
        conai_tax_id = self.env['ir.config_parameter'].sudo().get_param(
            'digitalforce_conai.default_tax_id')
        conai_tax = (
            self.env['account.tax'].browse(int(conai_tax_id))
            if conai_tax_id else False
        )

        invoice_date = self.invoice_date or fields.Date.today()

        # Remove existing CONAI lines
        existing = self.invoice_line_ids.filtered(
            lambda l: l.product_id and l.product_id.product_tmpl_id.is_conai_product
        )
        if existing:
            self.with_context(_conai_generating=True).write(
                {'invoice_line_ids': [(2, l.id) for l in existing]})

        new_line_vals = []
        for line in self.invoice_line_ids:
            if not line.product_id:
                continue
            tmpl = line.product_id.product_tmpl_id
            if tmpl.is_conai_product or not tmpl.conai_line_ids:
                continue

            for conai_line in tmpl.conai_line_ids:
                band = conai_line.band_id
                material = band.material_id
                weight_kg_per_unit = conai_line.weight_kg
                if not weight_kg_per_unit:
                    continue

                rate_per_tonne = band.get_rate_at(invoice_date)
                if not rate_per_tonne:
                    continue

                qty_kg = line.quantity * weight_kg_per_unit
                exemption_pct = self.env['conai.exemption'].get_exemption(
                    self.partner_id.commercial_partner_id, material)

                conai_product = self.env['product.product'].search([
                    ('product_tmpl_id.is_conai_product', '=', True),
                    ('default_code', '=', band.code),
                ], limit=1)
                if not conai_product:
                    continue

                account = conai_account or line.account_id
                if not account:
                    continue

                taxes = band.default_tax_id or conai_tax or line.tax_ids

                name = conai_product.name
                if exemption_pct:
                    kg_exempt = qty_kg * (exemption_pct / 100.0)
                    name += '\n' + _(
                        "Exemption %.0f%% — exempt quantity: %.4f kg"
                    ) % (exemption_pct, kg_exempt)
                name += ' - %s' % line.product_id.display_name

                new_line_vals.append((0, 0, {
                    'product_id': conai_product.id,
                    'name': name,
                    'quantity': qty_kg,
                    'price_unit': rate_per_tonne / 1000.0,
                    'discount': exemption_pct,
                    'tax_ids': [(6, 0, taxes.ids)],
                    'account_id': account.id,
                }))

        if new_line_vals:
            self.with_context(_conai_generating=True).write(
                {'invoice_line_ids': new_line_vals})

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move._is_conai_eligible() and not move._has_conai_lines():
                move._generate_conai_lines()
        return moves

    def write(self, vals):
        # Skip if we're the ones writing (prevents recursion)
        if self.env.context.get('_conai_generating'):
            return super().write(vals)
        res = super().write(vals)
        if 'invoice_line_ids' in vals:
            for move in self:
                if (move.state == 'draft'
                        and move._is_conai_eligible()
                        and not move._has_conai_lines()):
                    move._generate_conai_lines()
        return res
