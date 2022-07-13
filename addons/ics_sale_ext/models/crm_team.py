from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    name = fields.Char(
        string='Province'
    )
