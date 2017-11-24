frappe.provide('utility_wallet');

utility_wallet.WalletBalance = Class.extend({
  init: function(opts) {
    $.extend(this, opts);
    this.make();
  },
  make: function() {},
  refresh: function() {
    if (this.before_refresh) {
      this.before_refresh();
    }
    frappe
      .call({
        method: 'utility_wallet.utility_wallet.utils.get_all_wallet_balances',
      })
      .then(({ message }) => {
        this.render(message);
      });
  },
  render: function(data = []) {
    const total = data.reduce((a, d) => a + d.balance, 0);
    const currency = frappe.defaults.get_default('currency');
    $(
      frappe.render_template('wallet_balance', { data, currency, total })
    ).appendTo(this.parent);
  },
});
