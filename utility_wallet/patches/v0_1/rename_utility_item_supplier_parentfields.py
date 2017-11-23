# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def execute():
    frappe.reload_doc('Utility Wallet', 'doctype', 'Utility Item Supplier')
    frappe.db.sql("""
            UPDATE `tabUtility Item Supplier`
            SET parentfield='suppliers'
            WHERE parentfield='supplies'
        """)
