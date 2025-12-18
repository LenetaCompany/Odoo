{
    'name': 'Item Inventory Report',
    'version' : '19.0.0.1',
    'category': 'Inventory/Inventory',
    'summary': 'Item Inventory Report V 1.0',
    'author': 'Fawad Mazhar',
    'website': 'https://comstarusa.com',
    'depends': ['base','product','stock', 'sale_management'],
    'data': [
        # 'data/data.xml',
        'security/ir.model.access.csv',
        'wizard/inventory_report_wizard.xml',
        'report/inventory_report.xml',
        # 'views/product_sales_report_view.xml',
        # 'report/product_sales_report_template.xml',
    ],

    'license': 'LGPL-3',}
