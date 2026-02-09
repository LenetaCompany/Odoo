{
    'name': 'Custom Reports',
    'version': '19.0.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Custom Reports V 1.0',
    'author': '',
    'website': 'https://comstarusa.com',
    'depends': ['base', 'web', 'sale', 'account', 'stock', 'product'],
    'data': [
        # 'data/data.xml',
        'reports/deliveries_reports/stock_report_views.xml',
        # 'reports/deliveries_reports/report_stockpicking_operations.xml',
        'reports/deliveries_reports/report_deliveryslip.xml',
        'reports/deliveries_reports/studio_customization.xml',
        'reports/accounting_reports/account_report.xml',
        'reports/accounting_reports/report_invoice.xml',
        'reports/accounting_reports/studio_customization.xml',
        'reports/payments_reports/account_report.xml',
        'reports/payments_reports/report_payment_receipt_templates.xml',
        'reports/payments_reports/studio_customization.xml',
        'reports/sales_reports/ir_actions_report.xml',
        'reports/sales_reports/ir_actions_report_templates.xml',
        'reports/sales_reports/studio_customization.xml',
        'views/sale_order_views.xml'

    ],

    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
