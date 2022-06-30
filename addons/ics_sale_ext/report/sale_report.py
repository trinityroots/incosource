from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

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

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            coalesce(min(l.id), -s.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.product_uom_qty / u.factor * u2.factor)
                ELSE 0 END as product_uom_qty,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.qty_delivered / u.factor * u2.factor)
                ELSE 0 END as qty_delivered,
            CASE WHEN l.product_id IS NOT NULL
                THEN SUM(
                (l.product_uom_qty - l.qty_delivered) / u.factor * u2.factor)
                ELSE 0 END as qty_to_deliver,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.qty_invoiced / u.factor * u2.factor)
                ELSE 0 END as qty_invoiced,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.qty_to_invoice / u.factor * u2.factor)
                ELSE 0 END as qty_to_invoice,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.price_total / CASE COALESCE(s.currency_rate, 0)
                WHEN 0 THEN 1.0 ELSE s.currency_rate END)
                ELSE 0 END as price_total,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0)
                WHEN 0 THEN 1.0 ELSE s.currency_rate END)
                ELSE 0 END as price_subtotal,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(
                l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0)
                WHEN 0 THEN 1.0 ELSE s.currency_rate END)
                ELSE 0 END as untaxed_amount_to_invoice,
            CASE WHEN l.product_id IS NOT NULL
                THEN sum(
                l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0)
                WHEN 0 THEN 1.0 ELSE s.currency_rate END)
                ELSE 0 END as untaxed_amount_invoiced,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            s.campaign_id as campaign_id,
            s.medium_id as medium_id,
            s.source_id as source_id,
            extract(
            epoch from avg(
            date_trunc('day',s.date_order)-date_trunc('day',s.create_date))
            )/(24*60*60)::decimal(16,2) as delay,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            s.shop_type_id as shop_type_id,
            s.province_id as province_id,
            s.distribution_id as distribution_id,
            s.sale_office_id as sale_office_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.industry_id as industry_id,
            partner.commercial_partner_id as commercial_partner_id,
            CASE WHEN l.product_id IS NOT NULL THEN sum(p.weight * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as weight,
            CASE WHEN l.product_id IS NOT NULL THEN sum(p.volume * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as volume,
            l.discount as discount,
            CASE WHEN l.product_id IS NOT NULL THEN sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))ELSE 0 END as discount_amount,
            s.id as order_id
        """

        for field in fields.values():
            select_ += field
        return select_

    def _from_sale(self, from_clause=''):
        from_ = """
            sale_order_line l
              right outer join sale_order s on (s.id=l.order_id)
                join res_partner partner on s.partner_id = partner.id
                left join product_product p on (l.product_id=p.id)
                left join product_template t on (p.product_tmpl_id=t.id)
                left join uom_uom u on (u.id=l.product_uom)
                left join uom_uom u2 on (u2.id=t.uom_id)
                left join product_pricelist pp on (s.pricelist_id = pp.id)
                left join res_partner_industry rpi on (s.shop_type_id = rpi.id)
                left join crm_team crm on (s.province_id = crm.id)
                left join distribution dis on (s.distribution_id = dis.id)
                left join sale_office sff on (s.sale_office_id = sff.id)
                %s
        """ % from_clause
        return from_
