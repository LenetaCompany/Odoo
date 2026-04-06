{
    'name': 'Aged receivable format',
    'version': '19.0.0.0',
    'description': """Accounting Report """,
    'category': 'contacts',
    'summary': 'Aged receivable format',
    'author': 'ComstarUSA',
    'website': 'https://comstarusa.com',
    'depends': ['account_accountant','account_reports'],
    'assets': {
        'account_reports.assets_pdf_export': [
            'cs_scss_report/static/src/scss/cs_account_pdf_export_template.scss',
        ],
        'web.report_assets_common': [
            'cs_scss_report/static/src/scss/cs_account_pdf_export_template.scss',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
