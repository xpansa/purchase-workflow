odoo.define('purchase_requisition_multicurrency.purchase_requisition_multicurrency', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.DataModel');

    var CompareListView = core.view_registry.get('tree_purchase_order_line_compare');

    CompareListView = CompareListView.extend({
        render_buttons: function($node) {
            this._super.apply(this, arguments);
            var self = this;
            if (self.$buttons.find('.oe_header_currency').length == 0) {
                new Model('purchase.requisition')
                    .query(['currency_id'])
                    .filter([
                        ["id", "=", self.dataset.context.active_id]
                    ])
                    .first()
                    .then(function(tender) {
                        var currency_span = $('<span class="oe_header_currency">All prices in currency of purchase tender' + (tender['currency_id'][1] ? ' <b>[' + tender['currency_id'][1] + ']</b>' : '') + '</span>');
                        self.$buttons.append(currency_span);
                    });
            }
        },
    });

    core.view_registry.add('tree_purchase_order_line_compare', CompareListView);

});