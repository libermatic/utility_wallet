# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def _create_account(doc, company_name):
    abbr = frappe.get_value('Company', company_name, 'abbr')
    return frappe.get_doc({
            'doctype': "Account",
            'account_name': doc['account_name'],
            'parent_account': "{} - {}".format(doc['parent_account'], abbr),
            'is_group': 0,
            'company': company_name,
            "account_type": doc['account_type'],
        }).insert(ignore_if_duplicate=True)


def after_wizard_complete(args=None):
    if frappe.defaults.get_global_default('country') != "India":
        return

    company_name = frappe.defaults.get_global_default('company')

    _create_account({
            'account_name': "Utility Wallet",
            'parent_account': "Stock Assets",
            "account_type": "Stock",
        }, company_name)

    _create_account({
            'account_name': "Commission on Utility Purchases",
            'parent_account': "Indirect Income",
            "account_type": None,
        }, company_name)


def _set_fixtures():
    # for custom field
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Customer',
            'label': 'Utility Information',
            'fieldname': 'utility_information',
            'fieldtype': 'Section Break',
            'insert_after': 'disabled',
            'collapsible': 1,
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Customer',
            'label': 'Utility Service',
            'fieldname': 'utility_service',
            'insert_after': 'utility_information',
            'fieldtype': 'Table',
            'options': 'Customer Utility Item',
        }).insert(ignore_if_duplicate=True)

    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Supplier',
            'label': 'Utility Wallet',
            'fieldname': 'utility_wallet',
            'fieldtype': 'Section Break',
            'insert_after': 'prevent_pos',
            'collapsible': 1,
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Supplier',
            'label': 'Has Wallet',
            'fieldname': 'has_wallet',
            'fieldtype': 'Check',
            'insert_after': 'utility_wallet',
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Supplier',
            'label': 'Purchase Commission',
            'fieldname': 'purchase_commission',
            'fieldtype': 'Percent',
            'insert_after': 'has_wallet',
            'depends_on': 'eval:doc.has_wallet==1',
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Supplier',
            'label': 'Credit Amount',
            'fieldname': 'credit_amount',
            'fieldtype': 'Currency',
            'insert_after': 'section_credit_limit',
        }).insert(ignore_if_duplicate=True)


def after_install(args=None):
    _set_fixtures()
