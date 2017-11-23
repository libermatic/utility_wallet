// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

async function set_unique_no(frm) {
  const { message } = await frappe.db.get_value(
    'Customer Utility Item',
    {
      parent: frm.doc['customer'],
      parenttype: 'Customer',
    },
    'unique_no'
  );
  frm.set_value('unique_no', message['unique_no']);
}

frappe.ui.form.on('Utility Sale', {
  onload: async function(frm) {
    if (frm.doc.__islocal) {
      const { message } = await frappe.db.get_value(
        'Utility Wallet Settings',
        null,
        [
          'wallet_account',
          'sale_income_account',
          'sale_charges_account',
          'debit_to',
        ]
      );
      if (message) {
        const {
          wallet_account,
          sale_income_account,
          sale_charges_account,
          debit_to,
        } = message;
        frm.set_value('wallet_account', wallet_account);
        frm.set_value('income_account', sale_income_account);
        frm.set_value('debit_to', debit_to);
        frm.set_value('expense_account', sale_charges_account);
      }
    }
  },
  customer: async function(frm) {
    if (frm.doc['utility_item']) {
      set_unique_no(frm);
    } else {
      const { message } = await frappe.db.get_value(
        'Customer Utility Item',
        {
          parent: frm.doc['customer'],
          parenttype: 'Customer',
        },
        'utility_item'
      );
      if (message['utility_item']) {
        frm.set_value('utility_item', message['utility_item']);
      }
    }
  },
  utility_item: async function(frm) {
    const { message } = await frappe.db.get_value(
      'Utility Item Supplier',
      {
        parent: frm.doc['utility_item'],
        parenttype: 'Utility Item',
      },
      ['wallet_provider', 'sale_rate', 'sale_expense']
    );
    frm.set_value('wallet_provider', message['wallet_provider']);
    frm.set_value('service_rate', message['sale_rate']);
    frm.set_value('sale_expense_rate', message['sale_expense']);

    if (frm.doc['customer']) {
      set_unique_no(frm);
    }
    frm.set_value('amount', null);
    frm.set_value('charges', null);
  },
  wallet_provider: async function(frm) {
    const { message } = await frappe.call({
      method: 'utility_wallet.utility_wallet.utils.get_wallet_balance',
      args: {
        wallet_account: frm.doc.wallet_account,
        wallet_provider: frm.doc.wallet_provider,
      },
    });
    if (message) {
      frm.set_value('balance', message);
    } else {
      frm.set_value('balance', 0);
    }
  },
  amount: async function(frm) {
    const { message } = await frappe.db.get_value(
      'Utility Item Supplier',
      {
        parent: frm.doc['utility_item'],
        parenttype: 'Utility Item',
      },
      'sale_rate'
    );
    await frm.set_value('service_rate', message['sale_rate']);
    await frm.set_value(
      'charges',
      frm.doc['amount'] * frm.doc['service_rate'] / 100
    );
    frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
  },
  charges: async function(frm) {
    if (frm.doc['amount']) {
      await frm.set_value(
        'service_rate',
        frm.doc['charges'] / frm.doc['amount'] * 100
      );
      frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
    }
  },
  total: async function(frm) {
    const { message } = await frappe.db.get_value(
      'Utility Wallet Settings',
      null,
      'round_to'
    );
    const round_to = parseInt(message['round_to'], 10);
    if (round_to) {
      const old_total = frm.doc['total'];
      const new_total = Math.ceil(old_total / round_to) * round_to;
      if (old_total !== new_total) {
        frm.set_value('charges', new_total - frm.doc['amount']);
      }
    }
  },
  validate: async function(frm) {
    if (!frm.doc.__islocal && !frm.doc['voucher_no']) {
      frappe.throw('Cannot submit without Voucher No.');
    }
  },
});
