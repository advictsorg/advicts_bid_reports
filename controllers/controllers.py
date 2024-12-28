# -*- coding: utf-8 -*-
# from odoo import http


# class SaleLineProductGrid(http.Controller):
#     @http.route('/sale_line_product_grid/sale_line_product_grid', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_line_product_grid/sale_line_product_grid/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_line_product_grid.listing', {
#             'root': '/sale_line_product_grid/sale_line_product_grid',
#             'objects': http.request.env['sale_line_product_grid.sale_line_product_grid'].search([]),
#         })

#     @http.route('/sale_line_product_grid/sale_line_product_grid/objects/<model("sale_line_product_grid.sale_line_product_grid"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_line_product_grid.object', {
#             'object': obj
#         })
