{
    "name": "Custom Many2X Product Dropdown",
    "version": "19.0.1.0.0",
    "depends": ["web", "product"],
    "assets": {
        "web.assets_backend": [
            "cs_m2x_product_dropdown/static/src/js/many2x_patch.js",
            "cs_m2x_product_dropdown/static/src/xml/many2x_template.xml",
        ],
    },
    'installable': True,
    'application': False,
}
