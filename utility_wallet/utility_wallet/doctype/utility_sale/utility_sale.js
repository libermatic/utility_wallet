// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

async function set_unique_no(frm) {
  const { message = {} } = await frappe.db.get_value(
    'Customer Utility Item',
    {
      utility_item: frm.doc['utility_item'],
      parent: frm.doc['customer'],
      parenttype: 'Customer',
    },
    'unique_no'
  );
  frm.set_value('unique_no', message['unique_no']);
}

async function get_rounding_adjustment(amt) {
  const { message } = await frappe.db.get_value(
    'Utility Wallet Settings',
    null,
    'round_to'
  );
  const round_to = parseInt(message['round_to'], 10);
  if (round_to) {
    const new_amt = Math.ceil(amt / round_to) * round_to;
    return new_amt - amt;
  }
  return 0;
}

frappe.ui.form.on('Utility Sale', {
  refresh: async function(frm) {
    if (frm.doc['docstatus'] === 1) {
      frm.set_df_property('is_paid', 'read_only', 1);
    }
    if (
      frm.doc['docstatus'] === 1 &&
      0 < frm.doc['paid_amount'] &&
      frm.doc['paid_amount'] < frm.doc['total']
    ) {
      const remove_dialog = new frappe.ui.Dialog({
        title: 'Delete Payment',
        fields: [{ fieldname: 'ht', fieldtype: 'HTML' }],
      });
      const container = $('<table />').addClass(
        'table table-condensed table-striped'
      );
      container.append(
        $('<tr />')
          .append($('<th scope="col" />').text('Date'))
          .append($('<th scope="col" class="text-right" />').text('Amount'))
          .append($('<th scope="col" class="text-center" />').text('Action'))
      );
      remove_dialog.fields_dict.ht.$wrapper.append(container);
      frm.doc['payments'].forEach(function({
        payment_id,
        payment_date,
        payment_amount,
      }) {
        const handle_click = async function() {
          const { message = {} } = await frappe.call({
            method:
              'utility_wallet.utility_wallet.doctype.utility_sale.utility_sale.make_payment',
            args: {
              name: frm.doc['name'],
              payment_id,
              payment_date,
              payment_amount,
              reverse: 1,
            },
          });
          remove_dialog.hide();
          frm.reload_doc();
        };
        container.append(
          $('<tr />')
            .append($('<td />').text(payment_date))
            .append(
              $('<td class="text-right" />').text(
                format_currency(
                  payment_amount,
                  frappe.defaults.get_default('currency'),
                  2
                )
              )
            )
            .append(
              $('<td class="text-center" />').append(
                $('<i class="fa fa-times" style="cursor: pointer;" />').click(
                  handle_click
                )
              )
            )
        );
      });
      frm.add_custom_button(__('Delete Payment'), async function(fields) {
        remove_dialog.show();
      });
    }
    if (frm.doc['docstatus'] === 1 && !frm.doc['is_paid']) {
      const pay_dialog = new frappe.ui.Dialog({
        title: 'Make Payment',
        fields: [
          {
            label: 'Date',
            fieldname: 'payment_date',
            fieldtype: 'Datetime',
            default: frappe.datetime.now_datetime(),
          },
          {
            label: 'Amount',
            fieldname: 'payment_amount',
            fieldtype: 'Currency',
            default: frm.doc['total'] - frm.doc['paid_amount'],
          },
        ],
      });
      pay_dialog.set_primary_action(__('Pay'), async function(fields) {
        await frappe.call({
          method:
            'utility_wallet.utility_wallet.doctype.utility_sale.utility_sale.make_payment',
          args: Object.assign(
            { name: frm.doc['name'], payment_id: frappe.utils.get_random(10) },
            fields
          ),
        });
        this.hide();
        frm.reload_doc();
      });
      const pay_button = frm.add_custom_button(
        __('Receive Payment'),
        function() {
          pay_dialog.show();
        }
      );
      pay_button.addClass('btn-primary');
    }
  },
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
    frm.set_df_property('payments', 'read_only', 1);
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
    await frm.set_value('sale_expense_rate', message['sale_expense']);

    if (frm.doc['customer']) {
      set_unique_no(frm);
      const { message } = await frappe.db.get_value(
        'Customer Utility Item',
        {
          utility_item: frm.doc['utility_item'],
          parent: frm.doc['customer'],
          parenttype: 'Customer',
        },
        'no_sale_charges'
      );
      if (message['no_sale_charges']) {
        frm.set_value('sale_expense_rate', 0);
      }
    }
    frm.set_value('amount', null);
    frm.set_value('charges', null);
  },
  wallet_provider: async function(frm) {
    const { message = {} } = await frappe.call({
      method: 'utility_wallet.utility_wallet.utils.get_wallet_balance',
      args: {
        wallet_account: frm.doc.wallet_account,
        wallet_provider: frm.doc.wallet_provider,
      },
    });
    frm.set_value('balance', message['virtual']);
  },
  amount: async function(frm) {
    const { message } = await frappe.db.get_value(
      'Utility Item Supplier',
      {
        wallet_provider: frm.doc['wallet_provider'],
        parent: frm.doc['utility_item'],
        parenttype: 'Utility Item',
      },
      'sale_rate'
    );
    const { amount } = frm.doc;
    const charges = amount * frm.doc['service_rate'] / 100;
    frm.set_value('charges', charges);
    frm.set_value('total', amount + charges);
  },
  charges: async function(frm) {
    const { amount, charges } = frm.doc;
    const total = amount + charges;
    frm.set_value('total', total);
  },
  is_paid: async function(frm) {
    if (frm.doc['is_paid']) {
      frm.set_value('paid_amount', frm.doc['total']);
    } else {
      frm.set_value('paid_amount', 0);
    }
  },
  total: async function(frm) {
    const { total, amount, disable_rounding } = frm.doc;
    if (disable_rounding) {
      frm.set_value('charges', total - amount);
    } else {
      const rounding_adjustment = await get_rounding_adjustment(total);
      frm.set_value('charges', total + rounding_adjustment - amount);
    }
    if (frm.doc['is_paid']) {
      frm.set_value('paid_amount', total);
    }
  },
  disable_rounding: async function(frm) {
    frm.set_value('amount', null);
    frm.set_value('charges', null);
  },
  validate: async function(frm) {
    if (!frm.doc.__islocal && !frm.doc['voucher_no']) {
      frappe.throw('Cannot submit without Voucher No.');
    }
  },
});
