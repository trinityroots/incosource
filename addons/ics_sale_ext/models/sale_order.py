from odoo import fields, models, api, _
from odoo.tools import html_keep_url, is_html_empty


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    industry_id = fields.Many2one(
        string='Shop Type',
        comodel_name='res.partner.industry',
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
    def onchange_partner_id(self):
        # pylint: disable=biszx-onchange-func-name
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get('default_user_id',
                                                      self.env.uid)
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param(
                'account.use_invoice_terms'):
            if self.terms_type == 'html' and self.env.company.invoice_terms_html:
                baseurl = html_keep_url(self.get_base_url() + '/terms')
                values['note'] = _('Terms & Conditions: %s', baseurl)
            elif not is_html_empty(self.env.company.invoice_terms):
                values['note'] = self.with_context(
                    lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team'].with_context(
                default_team_id=self.partner_id.team_id.id
            )._get_default_team_id(
                domain=['|', ('company_id', '=', self.company_id.id),
                        ('company_id', '=', False)], user_id=user_id)

        # Add new value filed onchange
        distribution_id = self.partner_id.distribution_id or False
        team_id = self.partner_id.team_id or False
        sale_office_id = self.partner_id.sale_office_id or False
        industry_id = self.partner_id.industry_id or False
        values.update({
            'team_id': team_id,
            'industry_id': industry_id,
            'distribution_id': distribution_id,
            'sale_office_id': sale_office_id,
        })
        # ---------------------------------
        self.update(values)
