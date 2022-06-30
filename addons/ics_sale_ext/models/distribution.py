from odoo import fields, models


class Distribution(models.Model):
    _name = 'distribution'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        require=True,
    )

    sequence = fields.Integer(
        string='Sequence'
    )
