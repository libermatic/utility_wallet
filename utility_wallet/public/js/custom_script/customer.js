frappe.ui.form.on('Customer', 'refresh', function(frm) {
  if (frm.doc.utility_service.length > 0) {
    frm.add_custom_button(__('Make Utility Sale'), function() {
      frm.make_new('Utility Sale');
    });
  }
});
