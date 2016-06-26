# -*- coding: utf-8 -*-
from openerp import http

# class CliRepStock(http.Controller):
#     @http.route('/cli_rep_stock/cli_rep_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_rep_stock/cli_rep_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_rep_stock.listing', {
#             'root': '/cli_rep_stock/cli_rep_stock',
#             'objects': http.request.env['cli_rep_stock.cli_rep_stock'].search([]),
#         })

#     @http.route('/cli_rep_stock/cli_rep_stock/objects/<model("cli_rep_stock.cli_rep_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_rep_stock.object', {
#             'object': obj
#         })