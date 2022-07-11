from odoo import fields, models


class SaleOffice(models.Model):
    _name = 'sale.office'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        require=True,
    )

    sequence = fields.Integer(
        string='Sequence'
    )
