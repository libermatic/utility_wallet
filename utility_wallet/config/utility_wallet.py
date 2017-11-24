# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Transactions"),
			"items": [
				{
					"type": "doctype",
					"name": "Utility Purchase",
					"description": _("Record wallet refills."),
				},
				{
					"type": "doctype",
					"name": "Utility Sale",
					"description": _("Record wallet consumptions."),
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "page",
					"name": "wallet-balance",
					"label": _("Wallet Balance")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Utility Sale Register",
					"doctype": "Utility Sale Register",
				},
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Utility Item",
					"description": _("All utility items."),
				},
				{
					"type": "doctype",
					"name": "Utility Wallet Settings",
					"description": _("Wallet configs."),
				},
			]
		},
	]
