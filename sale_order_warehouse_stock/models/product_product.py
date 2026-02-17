from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    warehouse_stock_summary = fields.Text(
        compute='_compute_warehouse_stock_summary',
        store=False,
    )
    
    def _compute_warehouse_stock_summary(self):
        for product in self:
            warehouses = self.env['stock.warehouse'].search([])
            summary = []
            
            for warehouse in warehouses:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', product.id),
                    ('location_id', 'child_of', warehouse.lot_stock_id.id),
                ])
                
                if quants:
                    total_qty = sum(quants.mapped('quantity'))
                    reserved_qty = sum(quants.mapped('reserved_quantity'))
                    free_qty = total_qty - reserved_qty
                    
                    summary.append(
                        f"{warehouse.name}: {free_qty:.2f} {product.uom_id.name} "
                        f"(Total: {total_qty:.2f})"
                    )
            
            product.warehouse_stock_summary = '\n'.join(summary) if summary else 'No stock available'
