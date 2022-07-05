from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    authorized_signature = fields.Binary(
        string='Authorized Signature',
        related='company_id.authorized_signature',
    )
