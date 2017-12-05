# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, random_string
from erpnext import get_default_company
from erpnext.accounts.party import get_party_account
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

def _get_date_time(date_time):
	from datetime import datetime
	if isinstance(date_time, datetime):
		date = date_time.strftime('%Y-%m-%d')
		time = date_time.strftime('%H:%M:%S.%f')
	else:
		date, time = date_time.split()
	return date, time

class UtilitySale(AccountsController):
	def before_submit(self):
		if self.is_paid:
			self.append('payments', {
					'payment_id': random_string(10),
					'payment_date': self.transaction_date,
					'payment_amount': self.paid_amount
				})

	def on_submit(self):
		self.set_missing_values()
		self.make_parent_gl_entries()

	def on_cancel(self):
		self.set_missing_values()
		for entry in self.payments:
				make_payment(
				self.name,
				payment_id=entry.payment_id,
				payment_date=entry.payment_date,
				payment_amount=entry.payment_amount,
				parent_cancel=1
			)
		self.make_parent_gl_entries(cancel=1)

	def before_update_after_submit(self):
		total_paid = 0.0
		for row in self.payments:
			total_paid += flt(row.get_value('payment_amount'))
			if total_paid > self.total:
				return frappe.throw(_("Total paid amount cannot be greater than invoiced amount"))
		self.paid_amount = total_paid
		if total_paid == self.total:
			self.is_paid = 1

	def set_missing_values(self, for_validate=False):
		self.posting_date, self.posting_time = _get_date_time(self.transaction_date)
		self.company = get_default_company()

	def make_parent_gl_entries(self, cancel=0, adv_adj=0):
		sale_expense_amount = self.amount * self.sale_expense_rate / 100
		party_account = get_party_account('Customer', self.customer, self.company)
		gl_entries = [
			self.get_gl_dict({
					'account': self.wallet_account,
					'account_currency': get_account_currency(self.wallet_account),
					'credit_in_account_currency': self.amount + sale_expense_amount,
					'credit': self.amount + sale_expense_amount,
					'against': self.wallet_provider,
				}),
			self.get_gl_dict({
					'account': self.income_account,
					'account_currency': get_account_currency(self.income_account),
					'credit_in_account_currency': self.charges,
					'credit': self.charges,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center'),
					'against': self.customer,
				}),
			self.get_gl_dict({
					'account': party_account,
					'account_currency': get_account_currency(party_account),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'party_type': 'Customer',
					'party': self.customer,
				}),
			self.get_gl_dict({
					'account': self.expense_account,
					'account_currency': get_account_currency(self.expense_account),
					'debit_in_account_currency': sale_expense_amount,
					'debit': sale_expense_amount,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center'),
					'against': self.wallet_provider,
				}),
		]
		if self.is_paid:
			gl_entries.append(self.get_gl_dict({
					'account': party_account,
					'account_currency': get_account_currency(party_account),
					'credit_in_account_currency': self.total,
					'credit': self.total,
					'party_type': 'Customer',
					'party': self.customer,
					'against': self.debit_to,
				}))
			gl_entries.append(self.get_gl_dict({
					'account': self.debit_to,
					'account_currency': get_account_currency(self.debit_to),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'against': self.customer,
				}))
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)

@frappe.whitelist()
def make_payment(name, payment_id, payment_date, payment_amount, reverse=0, parent_cancel=0):
	r = frappe.get_doc('Utility Sale', name)
	cancel = reverse or parent_cancel
	if cancel:
		for entry in r.payments:
			if entry.get_value('payment_id') == payment_id:
				r.remove(entry)
				break
	else:
		r.append('payments', {
				'payment_id': payment_id,
				'payment_date': payment_date,
				'payment_amount': payment_amount
			})
	if not parent_cancel:
		r.save()
	r.posting_date = _get_date_time(payment_date)[0]
	r.company = get_default_company()
	party_account = get_party_account('Customer', r.customer, r.company)
	gl_entries = [
		r.get_gl_dict({
				'account': party_account,
				'account_currency': get_account_currency(party_account),
				'credit_in_account_currency': payment_amount,
				'credit': payment_amount,
				'voucher_type': 'Utility Sale Payment',
				'voucher_no': payment_id,
				'party_type': 'Customer',
				'party': r.customer,
				'against': r.debit_to,
				'against_voucher_type': 'Utility Sale',
				'against_voucher': name,
			}),
		r.get_gl_dict({
				'account': r.debit_to,
				'account_currency': get_account_currency(r.debit_to),
				'debit_in_account_currency': payment_amount,
				'debit': payment_amount,
				'voucher_type': 'Utility Sale Payment',
				'voucher_no': payment_id,
				'against': r.customer,
			}),
	]
	make_gl_entries(gl_entries, cancel=cancel, adv_adj=0)
