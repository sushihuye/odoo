# -*- coding: utf-8 -*-

from openerp import models, fields, api

class rep_stock(models.Model):
	_name = 'cli_rep_stock.rep_stock'

	@api.one
	def isi_data(self):
		repid = str(self.id)
		xtglakhir = self.tglakhir
		xtglawal = self.tglawal
		self.env.cr.execute('Delete from cli_rep_stock_rep_stock_line WHERE report_id = %s' % repid)
		produk = self.env['product.product']
		prod_id = produk.search([('product_tmpl_id.categ_id.id','=',int(float(self.category)))])
		sawal = self.env['stock.inventory.line']
		mutasi = self.env['stock.move']
		for hasil in prod_id:
			result={
				'report_id':self.id,
				'product_id':hasil.id,
				'product_name':hasil.name_template,
				'product_uom':hasil.product_tmpl_id.uom_id.name,
				'stock_awal':0,
				'stock_akhir':0,
				'mutasi_in':0,
				'mutasi_out':0,
			}
			self.env['cli_rep_stock.rep_stock_line'].create(result)
		for line in self.report_line:
			xproduct_id = line.product_id.id
			xlocation_id = line.report_id.location_id.id
			xqty=0
			self.env.cr.execute("SELECT sum(qty) as qty from stock_quant WHERE product_id = %d AND location_id=12 AND in_date<='%s'" % (xproduct_id, xtglakhir))
			result = self.env.cr.dictfetchall()
			for hsl in result:
				xqty = hsl['qty']
			if xqty is None:
				xqty = 0
			self.env.cr.execute("Update cli_rep_stock_rep_stock_line SET stock_akhir = %d WHERE product_id = %d" % (xqty, xproduct_id))
			sawal_val=sawal.search([('product_id','=',xproduct_id),('location_id','=',xlocation_id),('inventory_id.initial_inv','=',1)])
			line.stock_awal=sawal_val.product_qty
			xsawal_id = sawal_val.inventory_id.id
			#mutasi_val=mutasi.search([
			#	'&','&','&','&','|',
			#	('product_id','=',xproduct_id),
			#	('date','>=','01/05/2016'),
			#	('date','<=',xtglakhir),
			#	('inventory_id.id','!=',xsawal_id),
			#	('state','=','done'),
			#	('state','=','complete')])
			xmutasi_in = xmutasi_inl = xmutasi_out = xmutasi_outl = 0
			self.env.cr.execute("select product_qty,location_id,location_dest_id,inventory_id,date,state from stock_move WHERE product_id=%d and date >= '01/05/2016' AND date <= '%s' AND (inventory_id <> %d or inventory_id is Null) AND state in ('done','complete')" % (xproduct_id, xtglakhir, xsawal_id))
			result = self.env.cr.dictfetchall()
			for hasil in result:
				if hasil['date'] < xtglawal :
					if hasil['location_id'] == xlocation_id :
						xmutasi_outl += hasil['product_qty']
					if hasil['location_dest_id'] == xlocation_id:
						xmutasi_inl += hasil['product_qty']
				else:
					if hasil['location_id'] == xlocation_id :
						xmutasi_out += hasil['product_qty']
					if hasil['location_dest_id'] == xlocation_id:
						xmutasi_in += hasil['product_qty']
			line.stock_awal += (xmutasi_inl - xmutasi_outl)
			line.mutasi_in = xmutasi_in
			line.mutasi_out = xmutasi_out
			line.stock_akhir = line.stock_awal + line.mutasi_in - line.mutasi_out
		if self.isnol == 0:
			self.env.cr.execute("Delete FROM cli_rep_stock_rep_stock_line WHERE stock_akhir = 0 AND report_id =%s" % repid)
		return

	name = fields.Char('Judul Laporan')
	tglawal = fields.Date('Tanggal awal laporan')
	tglakhir = fields.Date('Tanggal akhir laporan')
	report_line = fields.One2many('cli_rep_stock.rep_stock_line','report_id','Report Line')
	category = fields.Selection([('4','Chemical'),('3','Lubricant')],'Kategori',default='4')
	isnol = fields.Boolean('Cetak saldo 0',default=False)
	lang = fields.Char('language',default='en-US')
	location_id = fields.Many2one('stock.location','Lokasi')
	
class rep_stock_line(models.Model):
	_name = "cli_rep_stock.rep_stock_line"
	_order = 'product_name'
	
	report_id = fields.Many2one('cli_rep_stock.rep_stock','Report Id')
	product_id = fields.Many2one('product.product','Product Id')
	product_name = fields.Char('Produk')
	product_uom = fields.Char('Satuan')
	stock_awal = fields.Float('Stock Awal')
	mutasi_out = fields.Float('Mutasi keluar')
	mutasi_in =  fields.Float('Mutasi masuk')
	stock_akhir = fields.Float('Stock Akhir')
	
class stock_inventory(models.Model):
	_name = "stock.inventory"
	_inherit = "stock.inventory"
	
	initial_inv= fields.Boolean('Initial_inv', default=False)
	