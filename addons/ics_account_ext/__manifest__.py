{
    'name': 'Incosource Account Ext',
    'summary': '''
        Account Function Ext''',
    'author': 'Santi T.',
    'website': 'https://roots.tech',
    'version': '15.0.0.0.1',
    "external_dependencies": {"python": ["bahttext"]},
    'depends': [
        'ics_core_update',
        'account',
    ],
    'data': [
        'views/res_partner_form_views.xml',
        'views/view_company_form.xml',
        'views/res_config_settings_view_form.xml',
    ],
    'license': 'LGPL-3',
}
