{
    'name': 'Report css in odoo 19',
     'version': '19.0.0.0',
    'depends': ['account_reports'],

    # 'assets': {
    #     'web.report_assets_common': [
    #         'cs_scss_report/static/src/css/account_pdf_override.css',
    #
    #     ],
    #
    # },


'assets': {

    'web.report_assets_common': [

        'cs_scss_report/static/src/css/account_pdf_override.css',

    ],

    'web.report_assets_pdf': [

        'cs_scss_report/static/src/css/account_pdf_override.css',

    ],

    'web.assets_backend': [

        'cs_scss_report/static/src/css/account_pdf_override.css',

    ],

},

'installable': True,
    'application': False,
}
