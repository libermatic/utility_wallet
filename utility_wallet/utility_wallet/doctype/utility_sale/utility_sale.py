# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext import get_default_company
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

class UtilitySale(AccountsController):
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
		sale_expense_amount = self.amount * self.sale_expense_rate / 100
		gl_entries = [
			self.get_gl_dict({
					'account': self.wallet_account,
					'account_currency': get_account_currency(self.wallet_account),
					'credit_in_account_currency': self.amount + sale_expense_amount,
					'credit': self.amount + sale_expense_amount,
					'against': self.customer,
				}),
			self.get_gl_dict({
					'account': self.income_account,
					'account_currency': get_account_currency(self.income_account),
					'credit_in_account_currency': self.charges,
					'credit': self.charges,
					'against': self.customer,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center'),
				}),
			self.get_gl_dict({
					'account': self.debit_to,
					'account_currency': get_account_currency(self.debit_to),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'against': self.customer,
				}),
			self.get_gl_dict({
					'account': self.expense_account,
					'account_currency': get_account_currency(self.expense_account),
					'debit_in_account_currency': sale_expense_amount,
					'debit': sale_expense_amount,
					'against': self.customer,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center'),
				}),
		]
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)
