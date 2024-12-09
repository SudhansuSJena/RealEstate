odoo.define('real_estate.BuyPropertyHandler', function(require){
    'use strict';

    const publicWidget = require('web.public.widget');// imports public.widget which handles all frontend actions like DOM manipulation, clicks etc.

    publicWidget.registry.BuyPropertyButton = publicWidget.Widget.extend({
        selector: ".buy-property-button", // Targets to the button class
        events: {
            'click': '_onClickBuyProperty', // Click event handler
        },

        /*-------------------------
        EVENT HANDLER FOR BUY BUTTON
        ----------------------------*/

        _onClickBuyProperty: function(event){
            event.preventDefault(); // Prevent default button behavior
            const propertyId = event.currentTarget.getAttribute('data-property-id');
            
            // Redirect the user to the buy property page
            if(propertyId){
                console.log("PropertyID: ")
                console.log(propertyId)
                window.location.href = `/buy_property/${propertyId}`;
            } else {
                console.log("Property ID is missing")
            }
        },
    });
});