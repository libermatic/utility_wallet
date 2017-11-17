// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Utility Purchase', {
  onload: async function(frm) {
    if (frm.doc.__islocal) {
      // frm.set_value('company', frappe.defaults.get_default('Company'));
      const { message } = await frappe.db.get_value(
        'Utility Wallet Settings',
        null,
        ['wallet_account', 'purchase_commission_account', 'credit_from']
      );
      if (message) {
        const {
          wallet_account,
          purchase_commission_account,
          credit_from,
        } = message;
        frm.set_value('credit_from', credit_from);
        frm.set_value('commission_account', purchase_commission_account);
        frm.set_value('wallet_account', wallet_account);
      }
    }
  },
  supplier: async function(frm) {
    const { message } = await frappe.db.get_value(
      'Supplier',
      frm.doc['supplier'],
      'purchase_commission'
    );
    frm.set_value('commission_rate', message['purchase_commission']);
  },
  amount: async function(frm) {
    commission_amount = frm.doc['amount'] * frm.doc['commission_rate'] / 100;
    frm.set_value('commission_amount', commission_amount);
    frm.set_value('total', frm.doc['amount'] + commission_amount);
  },
  commission_amount: async function(frm) {
    frm.set_value(
      'commission_rate',
      frm.doc['commission_amount'] / frm.doc['amount'] * 100
    );
  },
});
