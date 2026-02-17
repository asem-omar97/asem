{
    'name': 'Sale Order Warehouse Stock',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Display available stock quantities across multiple warehouses in sale order lines',
    'author': 'Your Name',
    'depends': ['sale', 'stock', 'product'],
    'data': [
        'views/sale_order_views.xml',
        'views/product_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sale_order_warehouse_stock/static/src/css/warehouse_stock.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
