from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_reference = fields.Char(
        string='Customer Reference',
    )
