# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.utils.data import add_days

def execute(filters=None):
	column = [
			_("Transaction Date") + ":Date:150",
			_("Document ID") + ":Link/Utility Sale:90",
			_("Customer") + ":Link/Customer:120",
			_("Utility Item") + ":Link/Utility Item:120",
			_("Wallet Provider") + ":Link/Supplier:120",
			_("Amount") + ":Currency/currency:90",
			_("Charges") + ":Currency/currency:90",
			_("Total") + ":Currency/currency:90",
			_("Voucher Code") + "::180",
		]
	cond = ["docstatus = 1"]
	if filters:
		if filters.get('from_date'):
			cond.append("transaction_date >= '%s'" % filters.get('from_date'))
		if filters.get('to_date'):
			cond.append("transaction_date < '%s'" % add_days(filters.get('to_date'), 1))
		if filters.get('utility_item'):
			cond.append("utility_item = '%s'" % filters.get('utility_item'))
		if filters.get('wallet_provider'):
			cond.append("wallet_provider = '%s'" % filters.get('wallet_provider'))
	data = frappe.db.sql("""
		SELECT transaction_date, name, customer, utility_item, wallet_provider, amount, charges, total, voucher_no
		FROM `tabUtility Sale`
		WHERE {}
	""".format(" and ".join(cond)))
	return column, data
