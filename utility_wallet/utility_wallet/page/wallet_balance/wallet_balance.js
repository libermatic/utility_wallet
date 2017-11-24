frappe.pages['wallet-balance'].on_page_load = function(wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'Wallet Balance',
    single_column: true,
  });
  frappe.require('assets/js/utility_wallet.min.js', function() {
    page.wallet_balance = new utility_wallet.WalletBalance({
      parent: page.main,
    });
    page.wallet_balance.refresh();
  });
};
