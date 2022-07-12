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
