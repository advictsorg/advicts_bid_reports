from odoo import models
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def action_print_bid_comparison_gh(self):
        active_ids = self.env.context.get('active_ids', [])

        # Restructure data for cross-tabulation
        vendor_product_prices = {}
        unique_products = set()
        unique_vendors = set()

        lines = self.browse(active_ids)
        purchase_order = False
        for l in lines:
            if l.order_id.state == 'purchase':
                purchase_order = l.order_id
                break
        for line in lines:
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
            'vendor_product_prices': vendor_product_prices,
            'reason': purchase_order.select_reason or ' ',
            'procurement_signature': purchase_order.procurement_signature or False,
            'supply_signature': purchase_order.supplay_signature or False,
            'project_manager_signature': purchase_order.pr_manager_signature or False,
        }

        # Uncomment to debug
        # raise UserError(str(report_data))

        return self.env.ref('advicts_bid_reports.report_bid_comparison').report_action(self, data=report_data)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_print_bid_comparison_by_vendors(self):

        vendors = {}
        lines = self.order_line

        for line in lines:
            vendor_name = line.partner_id.name
            if vendor_name not in vendors:
                vendors[vendor_name] = {
                    'name': vendor_name,
                    'purchase_order_lines': []
                }
            vendors[vendor_name]['purchase_order_lines'].append({
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

        report_data = {
            'data': list(vendors.values())
        }
        print(report_data)
        # raise UserError(str(report_data))
        return self.env.ref('advicts_bid_reports.report_bid_comparison_by_vendors').report_action(self,
                                                                                                  data=report_data)

    def action_print_bid_comparison_by_products(self):

        products = {}
        lines = self.order_line

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

        report_data = {
            'data': list(products.values())
        }
        # raise UserError(str(report_data))
        return self.env.ref('advicts_bid_reports.report_bid_comparison_by_products').report_action(self,
                                                                                                   data=report_data)
