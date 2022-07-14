from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    authorized_signature = fields.Binary(
        string='Authorized Signature',
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'ics_account_ext.authorized_signature',
            self.authorized_signature)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        authorized_signature = params.get_param(
            'ics_account_ext.authorized_signature')
        if authorized_signature:
            res.update(
                authorized_signature=authorized_signature)
            self.env.company.authorized_signature = authorized_signature
        return res
