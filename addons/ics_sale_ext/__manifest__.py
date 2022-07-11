{
    'name': 'Incosource Sale Ext',
    'summary': '''
        Sale Function Ext''',
    'author': 'Santi T.',
    'website': 'https://roots.tech',
    'version': '15.0.0.0.1',
    'depends': [
        'ics_core_update',
        'sale',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_menuitem.xml',
        'views/shop_type_view.xml',
        'views/distribution_view.xml',
        'views/sale_office_view.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/sale_report_view.xml',
    ],
    'license': 'LGPL-3',
}
