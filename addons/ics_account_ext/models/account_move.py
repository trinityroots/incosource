from odoo import models
from bahttext import bahttext


class AccountMove(models.Model):
    _inherit = 'account.move'

    def amount_baht_text(self, amount):
        if self.currency_id.name == 'THB':
            return bahttext(amount)
        else:
            return self.currency_id.amount_to_text(amount)
