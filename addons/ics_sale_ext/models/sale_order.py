from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    customer_rank = fields.Integer(
        string='Customer Rank',
        related='partner_id.customer_rank'
    )

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.shop_type_id = self.partner_id.shop_type_id
        self.province_id = self.partner_id.province_id
        self.distribution_id = self.partner_id.distribution_id
        self.sale_office_id = self.partner_id.sale_office_id
