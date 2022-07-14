from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    distribution_id = fields.Many2one(
        string='Distribution',
        comodel_name='distribution',
    )

    sale_office_id = fields.Many2one(
        string='Sale Office',
        comodel_name='sale.office',
    )

    team_id = fields.Many2one(
        string='Province',
        comodel_name='crm.team',
    )

    industry_id = fields.Many2one(
        string='Shop Type',
        comodel_name='res.partner.industry',
    )
