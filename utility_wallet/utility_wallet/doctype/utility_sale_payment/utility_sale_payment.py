# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UtilitySalePayment(Document):
	def on_update(self):
		print "ROW_UPDATE________________________________________"
	def on_submit(self):
		print "ROW_SUBMIT________________________________________"
	def on_cancel(self):
		print "ROW_CANCEL________________________________________"
	def update_after_submit(self):
		print "ROW_UPDATE_AFTER_SUBMIT________________________________________"
