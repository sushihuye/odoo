# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cli_rep_sales(models.Model):
	_name = 'cli.rep.sales'
	
	@api.one
	def generate_data(self):
		tglawal = self.tgl_awal
		tglakhir = self.tgl_akhir
		repid = str(self.id)
		if self.category=="Chemical":
			if self.isppn == True :
				kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','>',0),('cabang','=',0)]
			else:
				kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','=',0),('cabang','=',0)]
		else:
			if self.isppn == True :
				kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','>',0),('cabang','=',0)]
			else:
				kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','=',0),('cabang','=',0)]
		self.env.cr.execute("DELETE FROM cli_rep_sales_lines WHERE rep_id = %s"%repid)
		orderraw=self.env['sale.order']
		order=orderraw.sorted(key=lambda r: r.user_id)
		ord_id=order.search(kriteria)
		xsumKomisi = 0
		xsumNetto = 0
		xsumPD = 0
		xsumPD1 = 0
		xsumHarga_jual = 0
		for val in ord_id:
			newline=True
			xHarga=0
			xItem=''
			xNetto=0
			xHarga_jual=0
			xDiskonrp=0
			xDisc=0
			xppn=0
			if self.category=="Chemical":
				criteria_prod=4
			else:
				criteria_prod=3
			for val2 in val.order_line:
				if val2.product_id.product_tmpl_id.categ_id.id == criteria_prod :
					if newline==False:
						xItem += "\r\n"
					xItem += str(int(val2.product_uom_qty))+' '+val2.product_uom.name+' '+val2.product_id.name+'('+"{:,}".format(int(val2.price_unit)).replace(',','.')+")"
					newline=False
					xHarga += (val2.product_uom_qty * val2.price_unit)
					xNetto += (val2.product_uom_qty * val2.base_price)
					xDiskonrp += val2.diskonrp
					xDisc += (val2.product_uom_qty * int(val2.price_unit*(val2.discount/100)))
					xppn += (val2.price_subtotal- (val2.product_uom_qty * (val2.price_unit-int(val2.price_unit*(val2.discount/100)))))
					xHarga_jual += val2.price_subtotal
			xPsn_kom = 0
			xKomisi = 0
			xHarga_jual = xHarga_jual - xDiskonrp
			xDisc = xDisc + xDiskonrp
			xPD = xHarga - xDisc - xNetto
			xPD1 = int(xPD * (float(val.pd_rate)/100))
			if self.category=="Chemical":
				xPsn_kom = val.rate_chem
				xKomisi = int(val.komisi_chem)
			else :
				xPsn_kom = val.rate_lubs
				xKomisi = int(val.komisi_lubs)
			xsumKomisi += xKomisi
			xsumNetto += xNetto
			xsumPD1 += xPD1
			xsumPD += xPD
			xsumHarga_jual += xHarga_jual
			result={
				'rep_id': self.id,
				'Tanggal': val.date_order,
				'no_inv': val.client_order_ref,
				'sales': val.user_id.name,
				'customer': val.partner_id.name,
				'Item': xItem,
				'Harga': xHarga,
				'Disc': val.diskon,
				'Harga_jual': val.amount_untaxed,
				'ppn':xppn,
				'PD': val.pd1,
				'PD1': val.pd2,
				'Netto': xNetto,
				'Psn_kom': xPsn_kom,
				'Komisi': xKomisi,
				'ppn':xppn
			}
			self.env['cli.rep.sales.lines'].create(result)
			self.sumKomisi = xsumKomisi
			self.sumNetto = xsumNetto
			self.sumPD = xsumPD
			self.sumPD1 = xsumPD1
			self.sumHarga_jual = xsumHarga_jual
		return
		
	tgl_awal = fields.Date("Tanggal Awal")
	tgl_akhir = fields.Date("Tanggal Akhir")
	name = fields.Char("Nama Report :")
	category = fields.Selection([('Chemical','Chemical'),('Lubricant','Lubricant')],'Kategori',default='Chemical')
	isppn = fields.Boolean('PPN')
	report_line = fields.One2many('cli.rep.sales.lines','rep_id')
	lang = fields.Char("Language", default="en_US")
	sumKomisi = fields.Float("Total Komisi")
	sumNetto = fields.Float("Total Netto")
	sumPD = fields.Float("Total PD")
	sumPD1 = fields.Float("Total PD1")
	sumHarga_jual = fields.Float("Total Harga Jual")



class cli_rep_sales_line(models.Model):
	_name= "cli.rep.sales.lines"
	_order="no_inv"
	
	rep_id = fields.Many2one('cli.rep.sales')
	Tanggal = fields.Date('Tanggal')
	no_inv = fields.Char('No.Inv',select=True)
	sales = fields.Char('Sales')
	customer = fields.Char('Customer')
	Item = fields.Text('Item')
	Harga = fields.Float('Harga')
	Disc = fields.Float('Disc')
	Harga_jual = fields.Float('Harga Jual')
	PD = fields.Float('PD')
	PD1 = fields.Float('PD1')
	Netto = fields.Float('Netto')
	Psn_kom = fields.Float('%KOM')
	Komisi = fields.Float('Komisi')
	ppn = fields.Float('PPN')