{
    'name': 'ICS: Font',
    'summary': '''
        Font
    ''',
    'author': 'Roots',
    'category': 'Font',
    'website': 'https://roots.tech',
    'version': '15.0.0.0.1',
    'license': 'LGPL-3',
    'contributors': [
        'Santi T.',
    ],
    'depends': [
        'ics_core_update',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            'ics_font/static/src/css/tahoma.css',

        ],
        'web.report_assets_common': [
            'ics_font/static/src/css/tahoma.css',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}
