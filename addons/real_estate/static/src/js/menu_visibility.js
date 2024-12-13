odoo.define('real_estate.menu_visibility', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var $ = require('jquery');

    $(document).ready(function() {
        ajax.jsonRpc('/real_estate/menu_visibility', 'call', {}).then(function(result) {
            // Property Plus Menu
            var propertyPlusMenu = $('a[href="/real_estate/add_property"]');
            propertyPlusMenu.toggle(result.property_plus_menu);

            // Customer Menu
            var customerMenu = $('a[href="/customer"]');
            customerMenu.toggle(result.customer_menu);
        });
    });
});