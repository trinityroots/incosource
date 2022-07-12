from odoo.addons.sale.report.sale_report import SaleReport
from odoo.addons.pos_sale.report.sale_report import SaleReport as SalePosReport


def post_load_hook():

    def _select_sale_new(self, fields=None):
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
            s.sale_office_id as sale_office_id,
            s.distribution_id as distribution_id,
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

    def _from_sale_new(self, from_clause=''):
        from_ = """
                sale_order_line l
                      right outer join sale_order s on (s.id=l.order_id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                    left join sale_office sff on (s.sale_office_id = sff.id)
                    left join distribution dis on (s.distribution_id = dis.id)
                %s
        """ % from_clause
        return from_

    def _group_by_sale_new(self, groupby=''):
        groupby_ = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.partner_id,
            s.user_id,
            s.state,
            s.company_id,
            s.campaign_id,
            s.medium_id,
            s.source_id,
            s.pricelist_id,
            s.analytic_account_id,
            s.team_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.industry_id,
            partner.commercial_partner_id,
            l.discount,
            s.sale_office_id,
            s.distribution_id,
            s.id %s
        """ % (groupby)
        return groupby_

    SaleReport._select_sale = _select_sale_new
    SaleReport._from_sale = _from_sale_new
    SaleReport._group_by_sale = _group_by_sale_new

    def _select_pos_new(self, fields=None):
        if not fields:
            fields = {}
        select_ = '''
            MIN(l.id) AS id,
            l.product_id AS product_id,
            t.uom_id AS product_uom,
            sum(l.qty) AS product_uom_qty,
            sum(l.qty) AS qty_delivered,
            0 as qty_to_deliver,
            CASE WHEN pos.state = 'invoiced' THEN sum(l.qty) ELSE 0 END AS qty_invoiced,
            CASE WHEN pos.state != 'invoiced' THEN sum(l.qty) ELSE 0 END AS qty_to_invoice,
            SUM(l.price_subtotal_incl) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS price_total,
            SUM(l.price_subtotal) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS price_subtotal,
            (CASE WHEN pos.state != 'invoiced' THEN SUM(l.price_subtotal_incl) ELSE 0 END) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS amount_to_invoice,
            (CASE WHEN pos.state = 'invoiced' THEN SUM(l.price_subtotal_incl) ELSE 0 END) / MIN(CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END) AS amount_invoiced,
            count(*) AS nbr,
            pos.name AS name,
            pos.date_order AS date,
            CASE WHEN pos.state = 'draft' THEN 'pos_draft' WHEN pos.state = 'done' THEN 'pos_done' else pos.state END AS state,
            pos.partner_id AS partner_id,
            pos.user_id AS user_id,
            pos.company_id AS company_id,
            NULL AS campaign_id,
            NULL AS medium_id,
            NULL AS source_id,
            extract(epoch from avg(date_trunc('day',pos.date_order)-date_trunc('day',pos.create_date)))/(24*60*60)::decimal(16,2) AS delay,
            t.categ_id AS categ_id,
            pos.pricelist_id AS pricelist_id,
            NULL AS analytic_account_id,
            pos.crm_team_id AS team_id,
            p.product_tmpl_id,
            partner.country_id AS country_id,
            partner.industry_id AS industry_id,
            partner.commercial_partner_id AS commercial_partner_id,
            NULL AS sale_office_id,
            NULL AS distribution_id,
            (sum(t.weight) * l.qty / u.factor) AS weight,
            (sum(t.volume) * l.qty / u.factor) AS volume,
            l.discount as discount,
            sum((l.price_unit * l.discount * l.qty / 100.0 / CASE COALESCE(pos.currency_rate, 0) WHEN 0 THEN 1.0 ELSE pos.currency_rate END)) as discount_amount,
            NULL as order_id
        '''

        for field in fields.keys():
            select_ += ', NULL AS %s' % (field)
        return select_

    SalePosReport._select_pos = _select_pos_new
