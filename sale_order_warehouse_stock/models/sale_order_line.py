from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    warehouse_stock_html = fields.Html(
        string='Stock Availability',
        compute='_compute_warehouse_stock',
        readonly=True,
    )
    
    has_sufficient_stock = fields.Boolean(
        compute='_compute_warehouse_stock',
        readonly=True,
    )
    
    total_available_qty = fields.Float(
        compute='_compute_warehouse_stock',
        readonly=True,
    )
    
    @api.depends('product_id', 'product_uom_qty')
    def _compute_warehouse_stock(self):
        for line in self:
            if not line.product_id:
                line.warehouse_stock_html = ''
                line.has_sufficient_stock = True
                line.total_available_qty = 0.0
                continue
            
            warehouses = self.env['stock.warehouse'].search([])
            stock_data = []
            total_available = 0.0
            
            for warehouse in warehouses:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', 'child_of', warehouse.lot_stock_id.id),
                    ('quantity', '>', 0)
                ])
                
                available_qty = sum(quants.mapped('quantity'))
                reserved_qty = sum(quants.mapped('reserved_quantity'))
                free_qty = available_qty - reserved_qty
                
                if available_qty > 0 or reserved_qty > 0:
                    stock_data.append({
                        'warehouse': warehouse.name,
                        'free': free_qty,
                        'available': available_qty,
                        'reserved': reserved_qty,
                    })
                    total_available += free_qty
            
            if stock_data:
                html = '<div class="warehouse-stock-list">'
                for data in stock_data:
                    html += f'''
                        <div style="margin-bottom:5px; padding:5px; border-bottom:1px solid #eee;">
                            <strong>{data['warehouse']}:</strong> {data['free']:.2f}
                            <small>(Total: {data['available']:.2f} | Reserved: {data['reserved']:.2f})</small>
                        </div>
                    '''
                html += '</div>'
                line.warehouse_stock_html = html
                line.has_sufficient_stock = total_available >= line.product_uom_qty
                line.total_available_qty = total_available
            else:
                line.warehouse_stock_html = '<span>No stock available</span>'
                line.has_sufficient_stock = False
                line.total_available_qty = 0.0
