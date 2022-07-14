from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    authorized_signature = fields.Binary(
        string='Authorized Signature',
    )
