frappe.provide('utility_wallet');

utility_wallet.WalletBalance = Class.extend({
  init: function(opts) {
    $.extend(this, opts);
    this.make();
  },
  make: function() {},
  refresh: function() {
    frappe
      .call({
        method: 'utility_wallet.utility_wallet.utils.get_all_wallet_balances',
      })
      .then(({ message }) => {
        this.render(message);
      });
  },
  render: function(data = []) {
    const total_actual_balance = data.reduce((a, d) => a + d.actual_balance, 0);
    const total_virtual_balance = data.reduce(
      (a, d) => a + d.virtual_balance,
      0
    );
    const currency = frappe.defaults.get_default('currency');
    $(
      frappe.render_template('wallet_balance', {
        data,
        currency,
        total_actual_balance,
        total_virtual_balance,
      })
    ).appendTo(this.parent);
  },
});
