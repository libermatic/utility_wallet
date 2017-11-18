// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

cur_frm.fields_dict['wallet_account'].get_query = function(doc) {
  return {
    filters: {
      account_type: 'Stock',
      is_group: false,
    },
  };
};

cur_frm.fields_dict['sale_income_account'].get_query = function(doc) {
  return {
    filters: {
      root_type: 'Income',
      is_group: false,
    },
  };
};
cur_frm.fields_dict['sale_charges_account'].get_query = function(doc) {
  return {
    filters: {
      root_type: 'Expense',
      is_group: false,
    },
  };
};
cur_frm.fields_dict['debit_to'].get_query = function(doc) {
  return {
    filters: {
      account_type: 'Cash',
      is_group: false,
    },
  };
};

cur_frm.fields_dict['purchase_commission_account'].get_query = function(doc) {
  return {
    filters: {
      root_type: 'Income',
      is_group: false,
    },
  };
};
cur_frm.fields_dict['credit_from'].get_query = function(doc) {
  return {
    filters: {
      account_type: 'Bank',
      is_group: false,
    },
  };
};
