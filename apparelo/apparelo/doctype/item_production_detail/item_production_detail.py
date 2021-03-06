# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext import get_default_company, get_default_currency
from frappe.model.document import Document
from apparelo.apparelo.doctype.ipd_item_mapping.ipd_item_mapping import ipd_item_mapping
from apparelo.apparelo.doctype.ipd_bom_mapping.ipd_bom_mapping import ipd_bom_mapping
from frappe.utils import comma_and,get_link_to_form
from collections import Counter

class ItemProductionDetail(Document):
	def on_submit(self):
		self.validate_process_records()
		ipd_list=self.create_process_details()
		ipd_item_mapping(ipd_list,self.name,self.item)
		ipd_bom_mapping(ipd_list,self.name,self.item)

	def validate_process_records(self):
		count = 0
		link =''
		for process in self.processes:
			doc_type= frappe.get_doc(process.process_name, process.process_record)
			if not doc_type.docstatus:
				link += f'{get_link_to_form(process.process_name,process.process_record)} , '
				count +=1
		if count != 0:
			frappe.throw(_(f"The process {link} is not submitted"))

	def submit_all_process_records(self):
		for process in self.processes:
			process_doc = frappe.get_doc(process.process_name, process.process_record)
			if not process_doc.docstatus:
				try:
					process_doc.submit()
				except:
					link = get_link_to_form(process.process_name, process.process_record)
					frappe.throw(_(f"Unable to submit process {link}"))
					frappe.log_error(frappe.get_traceback())
					return

	def create_process_details(self):
		ipd = []
		attribute_set={}
		cutting_attribute={}
		piece_count=None
		item_size=[]
		colour=[]
		final_process=self.final_process
		for final_size in self.size:
			item_size.append(final_size.size)
		for final_colour in self.colour:
			colour.append(final_colour.colour)

		for process in self.processes:
			process_variants = {}
			if process.process_name == 'Knitting':
				process_variants['process'] = 'Knitting'
				process_variants['index']=process.idx
				process_variants['input_index']=''
				process_variants['input_item']=[process.input_item]
				if process.input_item:
					process_variants['process_record'] = process.process_record
					knitting_doc = frappe.get_doc('Knitting', process.process_record)
					variants = knitting_doc.create_variants([process.input_item])
					process_variants['variants'] = list(set(variants))
					boms=knitting_doc.create_boms([process.input_item], variants, attribute_set,item_size,colour,piece_count)
					process_variants['BOM']=list(set(boms))
					ipd.append(process_variants)
				elif process.input_index:
					pass
				continue

			if process.process_name == 'Dyeing':
				process_variants['process'] = 'Dyeing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items = []
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								dyeing_doc = frappe.get_doc('Dyeing', process.process_record)
								variants.extend(dyeing_doc.create_variants(input_items))
								boms.extend(dyeing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue
			
			if process.process_name == 'Roll Printing':
				process_variants['process'] = 'Roll Printing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								roll_printing_doc = frappe.get_doc('Roll Printing', process.process_record)
								variants.extend(roll_printing_doc.create_variants(input_items))
								boms.extend(roll_printing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue
			if process.process_name == 'Steaming':
				process_variants['process'] = 'Steaming'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								steaming_doc = frappe.get_doc('Steaming', process.process_record)
								variants.extend(steaming_doc.create_variants(input_items))
								boms.extend(steaming_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Compacting':
				process_variants['process'] = 'Compacting'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								compacting_doc = frappe.get_doc('Compacting', process.process_record)
								variants.extend(compacting_doc.create_variants(input_items))
								boms.extend(compacting_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Bleaching':
				process_variants['process'] = 'Bleaching'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								bleaching_doc = frappe.get_doc('Bleaching', process.process_record)
								variants.extend(bleaching_doc.create_variants(input_items))
								boms.extend(bleaching_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Cutting':
				process_variants['process'] = 'Cutting'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					new_variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
					process_variants['process_record'] = process.process_record
					cutting_doc = frappe.get_doc('Cutting', process.process_record)
					variants,attribute_set = cutting_doc.create_variants(input_items_,item_size)
					bom,new_variants=cutting_doc.create_boms(input_items_, variants, attribute_set,item_size,colour,piece_count)
					new_variants.extend(new_variants)
					boms.extend(bom)
					counter_attr=Counter(cutting_attribute)
					attr_set=Counter(attribute_set)
					counter_attr.update(attr_set)
					cutting_attribute=dict(counter_attr)
					for value in cutting_attribute:
						cutting_attribute[value]=list(set(cutting_attribute[value]))
					process_variants['variants'] = list(set(new_variants))
					process_variants['BOM']=boms
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Piece Printing':
				process_variants['process'] = 'Piece Printing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								piece_printing_doc = frappe.get_doc('Piece Printing', process.process_record)
								variants.extend(piece_printing_doc.create_variants(input_items))
								boms.extend(piece_printing_doc.create_boms(input_items, variants,cutting_attribute,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Stitching':
				process_variants['process'] = 'Stitching'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							if str(pro['index'])==input_index:
								input_items.extend(pro['variants'])
					process_variants['process_record'] = process.process_record
					stitching_doc = frappe.get_doc('Stitching', process.process_record)
					variants.extend(stitching_doc.create_variants(input_items,colour,self.item,final_process))
					boms.extend(stitching_doc.create_boms(input_items, variants,cutting_attribute,item_size,colour,piece_count,final_process))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Label Fusing':
				process_variants['process'] = 'Label Fusing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								label_fusing_doc = frappe.get_doc('Label Fusing', process.process_record)
								variants.extend(label_fusing_doc.create_variants(input_items))
								boms.extend(label_fusing_doc.create_boms(input_items, variants,cutting_attribute,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue
			if process.process_name == 'Checking':
				process_variants['process'] = 'Checking'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								checking_doc = frappe.get_doc('Checking', process.process_record)
								variants.extend(checking_doc.create_variants(input_items,self.item,final_process))
								boms.extend(checking_doc.create_boms(input_items, variants,cutting_attribute,item_size,colour,piece_count,final_process))
					process_variants['variants'] =list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Ironing':
				process_variants['process'] = 'Ironing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								ironing_doc = frappe.get_doc('Ironing', process.process_record)
								variants.extend(ironing_doc.create_variants(input_items,self.item,final_process))
								boms.extend(ironing_doc.create_boms(input_items, variants,cutting_attribute,item_size,colour,piece_count,final_process))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Packing':
				process_variants['process'] = 'Packing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					new_variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								process_variants['process_record'] = process.process_record
								packing_doc = frappe.get_doc('Packing', process.process_record)
								variants,piece_count= packing_doc.create_variants(input_items,self.item)
								new_variants.extend(variants)
								boms.extend(
									packing_doc.create_boms(
										input_items, variants,
										item_size, colour, piece_count, self.item))
					process_variants['variants'] = list(set(new_variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

		if self.additional_flows!=[]:
			ipd=additional_process(self,ipd)
		if self.is_combined_packing:
			input_items_=[]
			process_variants = {}
			for ipd in self.combined_ipds:
				item_mapping = frappe.db.get_value("IPD Item Mapping", {'item_production_details': ipd.ipd})
				ipd_doc=frappe.get_doc("Item Production Detail",ipd.ipd)
				variants = frappe.get_doc('IPD Item Mapping', item_mapping).get_process_variants(ipd_doc.final_process)
				input_items_.extend(variants)
			if self.process_name == 'Packing':
				process_variants['process'] = 'Packing'
				process_variants['index']="C1"
				new_variants=[]
				boms=[]
				process_variants['input_index']=''
				process_variants['process_record'] = self.process_record
				packing_doc = frappe.get_doc('Packing', self.process_record)
				variants,piece_count= packing_doc.create_variants(input_items_,self.item)
				new_variants.extend(variants)
				boms.extend(packing_doc.create_boms(input_items_, variants,cutting_attribute,item_size,colour,piece_count,self.item))
				process_variants['variants'] = list(set(new_variants))
				process_variants['BOM']=list(set(boms))
				process_variants['input_item']=list(set(input_items_))
				ipd.append(process_variants)
			else:
				frappe.throw(_(f"Only Packing Process is Supported in Combined IPD Packing"))
		return ipd

def additional_process(self,ipd):
	items=[]
	for process in self.additional_flows:
			input_index=''
			process_variants={}
			input_item=[]
			process_variants['index']='A'+str(process.idx)
			process_variants['process']=process.process_1
			process_variants['input_index']=''
			process_=frappe.get_doc("Multi Process",process.process_1)
			for ipd_ in ipd:
				if ipd_['process']==process_.from_process:
					input_index=ipd_['input_index']
			input_indexs = input_index.split(',')
			for ipd_ in ipd:
				for in_index in input_indexs:
					if str(ipd_['index'])==in_index:
						input_=ipd_['variants']
						input_item.extend(input_)

				if ipd_['process']==process_.to_process:
					process_variants['variants']=ipd_['variants']
					process_variants['BOM']=ipd_['BOM']
			for item in input_item:
				item_={}
				item_['item']=item
				item_['qty']=0
				item_['uom']=''
				items.append(item_)
			boms=set()
			input_=set()
			for bom in process_variants['BOM']:
				item_list=[]
				bom_=frappe.get_doc("BOM",bom)
				additional_item={}
				for _item in bom_.items:
					if _item.bom_no=='':
						additional_item[_item.item_code]=0
				qty=1
				planned_qty=1
				additional_item,items_=bom_item(qty,bom,additional_item,input_item,items,planned_qty)
				for item in items_:
					if item['qty']!=0:
						input_.add(item['item'])
						item_list.append({"item_code": item['item'],"qty":item['qty'] ,"uom": item['uom']})
						item['qty']=0
						item['uom']=''
				for add_ in additional_item:
					item_list.append({"item_code": add_,"qty":additional_item[add_] ,"uom": 'Nos'})
				existing_bom = frappe.db.get_value('BOM', {'item': bom_.item,'process':process_variants['process']}, 'name')
				if not existing_bom:
					new_bom = frappe.get_doc({
						"doctype": "BOM",
						"currency": get_default_currency(),
						'process': process_variants['process'],
						"is_default":0,
						"is_active":1,
						"item": bom_.item,
						"company": get_default_company(),
						"items": item_list
					})
					new_bom.save()
					new_bom.submit()
					boms.add(new_bom.name)
				else:
					boms.add(existing_bom)
			process_variants['input_item']=list(input_)
			process_variants['BOM']=list(boms)
			ipd.append(process_variants)
	return ipd

def bom_item(qty,bom,additional_item,variants,items,planned_qty):
	bom_doc=frappe.get_doc("BOM",bom)
	bom_quantity=(bom_doc.quantity/bom_doc.quantity)*planned_qty
	for item in bom_doc.items:
		if item.uom=='Gram':
			bom_quantity=bom_quantity*item.stock_qty
		if item.uom=='Nos' and item.qty>1:
				qty=item.qty*planned_qty
		if item.bom_no=='':
			if not item.item_code in additional_item:
				additional_item[item.item_code]=0
				additional_item[item.item_code]+=item.qty*bom_quantity
			else:
				additional_item[item.item_code]+=item.qty*bom_quantity
		else:
			if item.item_code in variants:
				for bom_item_list in items:
					if item.item_code==bom_item_list['item']:
						bom_item_list['qty']+=item.qty*qty*bom_quantity
						bom_item_list['uom']=item.uom
						qty=1
			else:
				bom_item(qty,item.bom_no,additional_item,variants,items,bom_quantity)
				qty=1
	return additional_item,items

def process_based_qty(process,ipd=None,lot=None,qty_based_bom=None):
	process_bom=[]
	if lot:
		# getting qty from the lot
		qty_based_bom=[]
		lot_doc=frappe.get_doc("Lot Creation",lot)
		for item in lot_doc.po_items:
			qty_based_bom.append({item.bom_no:item.planned_qty})
		# setting IPD from lot as the qty is related to this lot only
		ipd = frappe.db.get_value('Lot Creation', {'name': lot}, 'item_production_detail')
	if ipd:
		ipd_bom_mapping = frappe.db.get_value("IPD BOM Mapping", {'item_production_details': ipd})
		for process_name in process:
			process_bom.extend(frappe.get_doc('IPD BOM Mapping', ipd_bom_mapping).get_process_boms(process_name))
	else:
		frappe.throw(_("Either IPD or Lot is required to compute process based qty"))

	items = []
	input_item = []
	for bom in set(process_bom):
		bom_doc=frappe.get_doc("BOM",bom)
		for item in bom_doc.items:
			input_item.append(item.item_code)
	for item in set(input_item):
		item_list={}
		item_list['item']=item
		item_list['qty']=0
		item_list['uom']=''
		items.append(item_list)

	additional_item = {}
	for bom_dict in qty_based_bom:
		for bom in bom_dict:
			bom_doc=frappe.get_doc("BOM",bom)
			for item in bom_doc.items:
				if item.bom_no=='':
					additional_item[item.item_code]=0
			if bom_dict[bom]:
				qty=1
				additional_item,items=bom_item(qty,bom,additional_item,set(input_item),items,bom_dict[bom])

	# making desired output structure from the created data
	final_item_list = []
	additional_item_list = []
	for item in items:
		if item['qty']!=0:
			final_item_list.append({"item_code": item['item'],"qty":item['qty'] ,"uom": item['uom']})
	for item in additional_item:
		additional_item_list.append({"item_code": item,"qty":additional_item[item] ,"uom": 'Nos'})

	return additional_item_list,final_item_list