from odoo.http import request


def do_query(query, key):
    request.env.cr.execute(query, [key])


def do_update(query, key1, key2):
    request.env.cr.execute(query, [key1, key2])


def do_concat(pulled_name):
    percent_pulled_name = str(pulled_name + "%")
    return percent_pulled_name


def do_concat_loop(pulled_stock_picking):
    percent_picking = [pulled + "%" for pulled in pulled_stock_picking]
    return percent_picking
