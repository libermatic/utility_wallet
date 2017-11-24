// Copyright (c) 2016, Libermatic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Utility Sale Register'] = {
  filters: [
    {
      fieldname: 'from_date',
      label: __('From Date'),
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
      width: '80',
    },
    {
      fieldname: 'to_date',
      label: __('To Date'),
      fieldtype: 'Date',
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: 'utility_item',
      label: __('Utility Item'),
      fieldtype: 'Link',
      options: 'Utility Item',
    },
    {
      fieldname: 'wallet_provider',
      label: __('Wallet Provider'),
      fieldtype: 'Link',
      options: 'Supplier',
      get_query: doc => ({
        filters: { has_wallet: true },
      }),
    },
  ],
};
