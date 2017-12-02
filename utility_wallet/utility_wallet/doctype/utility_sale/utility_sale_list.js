frappe.listview_settings['Utility Sale'] = {
  add_fields: ['total', 'paid_amount'],
  get_indicator: function(doc) {
    if (flt(doc['total']) === flt(doc['paid_amount'])) {
      return [__('Paid'), 'green', 'total,=,paid_amount'];
    }
    return [__('Pending'), 'orange', 'total,>,paid_amount'];
  },
  reports: [
    {
      name: 'Wallet Balance',
      report_type: 'Page',
      route: 'wallet-balance',
    },
  ],
};
