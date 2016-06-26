# -*- coding: utf-8 -*-
from openerp import http

# class CliRepSales(http.Controller):
#     @http.route('/cli_rep_sales/cli_rep_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_rep_sales/cli_rep_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_rep_sales.listing', {
#             'root': '/cli_rep_sales/cli_rep_sales',
#             'objects': http.request.env['cli_rep_sales.cli_rep_sales'].search([]),
#         })

#     @http.route('/cli_rep_sales/cli_rep_sales/objects/<model("cli_rep_sales.cli_rep_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_rep_sales.object', {
#             'object': obj
#         })