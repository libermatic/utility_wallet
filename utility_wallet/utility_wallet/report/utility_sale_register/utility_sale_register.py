# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
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
			_("Outstanding") + ":Currency/currency:90",
			_("Unique No") + "::90",
			_("Voucher Code") + "::180",
			_("Phone") + "::90",
		]
	cond = ["ut.docstatus = 1"]
	if filters:
		if filters.get('from_date'):
			cond.append("ut.transaction_date >= '%s'" % filters.get('from_date'))
		if filters.get('to_date'):
			cond.append("ut.transaction_date < '%s'" % add_days(filters.get('to_date'), 1))
		if filters.get('utility_item'):
			cond.append("ut.utility_item = '%s'" % filters.get('utility_item'))
		if filters.get('wallet_provider'):
			cond.append("ut.wallet_provider = '%s'" % filters.get('wallet_provider'))
	data = frappe.db.sql("""
		SELECT ut.transaction_date, ut.name, ut.customer, ut.utility_item, ut.wallet_provider, ut.amount, ut.charges, ut.total, ut.total-ut.paid_amount, ut.unique_no, ut.voucher_no, at.phone
		FROM `tabUtility Sale` AS ut
		LEFT JOIN `tabDynamic Link` AS dt ON dt.link_name = ut.customer
		LEFT JOIN `tabAddress` AS at ON dt.parent = at.name
		WHERE {}
		ORDER BY ut.transaction_date
	""".format(" and ".join(cond)))
	return column, data
