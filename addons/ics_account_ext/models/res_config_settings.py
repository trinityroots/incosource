from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    authorized_signature = fields.Binary(
        string='Authorized Signature',
        related='company_id.authorized_signature',
    )
#     company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
