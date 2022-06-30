from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    shop_type_id = fields.Many2one(
        string='Shop Type',
        comodel_name='res.partner.industry',
    )

    province_id = fields.Many2one(
        string='Province',
        comodel_name='crm.team'
    )

    distribution_id = fields.Many2one(
        string='Distribution',
        comodel_name='distribution',
    )

    sale_office_id = fields.Many2one(
        string='Sale Office',
        comodel_name='sale.office',
    )
