from odoo import fields, models, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    name = fields.Char(
        string='Province'
    )
