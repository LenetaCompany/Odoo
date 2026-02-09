{
    'name': 'Payment check report',
    'version': '19.0.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Item Inventory Report V 1.0',
    'author': '',
    'website': 'https://comstarusa.com',
    'depends': ['base', 'web', 'sale', 'account','l10n_us_check_printing'],
    'data': [
        'reports/checks_report.xml',
    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
