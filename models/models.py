from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    procurement_signature = fields.Binary('Procurement Signature')
    supplay_signature = fields.Binary('Supply Chain Manager Signature')
    pr_manager_signature = fields.Binary('Project manager Signature')

    select_reason = fields.Text('Selection Reason')

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def action_print_bid_comparison_gh(self):
        active_ids = self.env.context.get('active_ids', [])


        # Restructure data for cross-tabulation
        vendor_product_prices = {}
        unique_products = set()
        unique_vendors = set()

        lines = self.browse(active_ids)

        for line in lines:
            _logger.info(line.product_id.name)
            product_name = line.product_id.display_name
            vendor_name = line.partner_id.name

            # Track unique products and vendors
            unique_products.add(product_name)
            unique_vendors.add(vendor_name)

            # Create nested dictionary for vendor-product pricing
            if vendor_name not in vendor_product_prices:
                vendor_product_prices[vendor_name] = {}

            vendor_product_prices[vendor_name][product_name] = {
                'product_name': product_name,
                'unit_price': line.price_unit,
                'total_price': line.price_subtotal,
                'product_qty': line.product_qty,
                'unit_of_measure': line.product_uom.name,
                'otd': f"{line.on_time_rate_perc * 100:.2f}%" if line.on_time_rate_perc else 'N/A',
                'reference': line.order_id.name,
                'status': line.state,
                'expected_arrival': line.date_planned,
                'currency': line.currency_id.symbol
            }

        # Prepare report data
        report_data = {
            'vendors': sorted(list(unique_vendors)),
            'products': sorted(list(unique_products)),
            'vendor_product_prices': vendor_product_prices
        }

        # Uncomment to debug
        # raise UserError(str(report_data))

        # return self.env.ref('advicts_bid_reports.report_bid_comparison').report_action(self, data=report_data)

    def action_print_bid_comparison_by_products(self):
        # Fetch the active IDs from the context
        active_ids = self.env.context.get('active_ids', [])

        # Prepare data for the report, grouped by product
        products = {}
        lines = self.browse(active_ids)  # Get only the selected purchase order lines

        for line in lines:
            product_name = line.product_id.name
            if product_name not in products:
                products[product_name] = {
                    'name': product_name,
                    'purchase_order_lines': []
                }
            products[product_name]['purchase_order_lines'].append({
                'product_name': line.product_id.display_name,
                'vendor_name': line.partner_id.name,
                'otd': f"{line.on_time_rate_perc * 100:.2f}%",
                'reference': line.order_id.name,
                'status': line.state,
                'description': line.name,
                'expected_arrival': line.date_planned,
                'product_qty': line.product_qty,
                'unit_of_measure': line.product_uom.name,
                'price_unit': line.price_unit,
                'total': line.price_subtotal,
                'currency': line.currency_id.name
            })

        # Uncomment this line to test the data format with a popup

        report_data = {
            'data': list(products.values())
        }
        # raise UserError(str(report_data))
        return self.env.ref('advicts_bid_reports.report_bid_comparison_by_products').report_action(self,
                                                                                                   data=report_data)


