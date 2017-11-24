# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext import get_default_company
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

class UtilityPurchase(AccountsController):
	def on_submit(self):
		self.set_missing_values()
		self.make_gl_entries()

	def on_cancel(self):
		self.set_missing_values()
		self.make_gl_entries(cancel=1)

	def set_missing_values(self, for_validate=False):
		datetime = self.transaction_date.split()
		self.posting_date = datetime[0]
		self.posting_time = datetime[1]
		self.company = get_default_company()

	def make_gl_entries(self, cancel=0, adv_adj=0):
		gl_entries = [
			self.get_gl_dict({
					'account': self.credit_from,
					'account_currency': get_account_currency(self.credit_from),
					'credit_in_account_currency': self.amount,
					'credit': self.amount,
					'against': self.supplier,
				}),
			self.get_gl_dict({
					'account': self.commission_account,
					'account_currency': get_account_currency(self.commission_account),
					'credit_in_account_currency': self.commission_amount,
					'credit': self.commission_amount,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center')
				}),
			self.get_gl_dict({
					'account': self.wallet_account,
					'account_currency': get_account_currency(self.wallet_account),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'against': self.supplier,
				}),
		]
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)
