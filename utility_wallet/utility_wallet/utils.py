# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

@frappe.whitelist()
def get_wallet_balance(wallet_provider=None, wallet_account=None):
    bal = frappe.db.sql("""
            SELECT sum(debit) - sum(credit)
            FROM `tabGL Entry`
            WHERE account = '{0}' AND against = '{1}'
        """.format(wallet_account, wallet_provider))[0][0]
    return flt(bal)
