# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def after_install():
	frappe.get_doc({
            'doctype': "Item Group",
            'item_group_name': "Utilities",
            'parent_item_group': "All Item Groups"
        }).insert()
	frappe.get_doc({
            'doctype': "Item",
            'item_code': "Electricity",
            'item_group': "Utilities",
            'stock_uom': "Unit",
            'is_stock_item': True
        }).insert()
