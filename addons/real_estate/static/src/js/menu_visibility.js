/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MenuVisibilityComponent extends Component {
    static template = 'real_estate.MenuVisibilityComponent';  // Ensure the template name is correct

    setup() {
        this.rpc = useService("rpc");
        this.state = {
            propertyPlusMenuVisible: false,
            customerMenuVisible: false,
        };

        onWillStart(async () => {
            try {
                // Fetch the visibility state for the menus
                const result = await this.rpc("/real_estate/menu_visibility", {});
                
                // Map the response to the component's state
                this.state.propertyPlusMenuVisible = result.property_plus_menu;
                this.state.customerMenuVisible = result.customer_menu;

                // Call the function to hide/show menus based on the state
                this.toggleMenuVisibility();
            } catch (error) {
                console.error(`Error occurred while fetching menu visibility: ${error}`);
            }
        });
    }

    // Function to toggle menu visibility based on the state
    toggleMenuVisibility() {
        // Select the menu items using their ids (replace with actual menu ids if needed)
        const propertyPlusMenu = document.querySelector('a.nav-link[href="/real_estate/add_property"]');
        const customerMenu = document.querySelector('a.nav-link[href="/customer"]');

        // Show or hide the menus based on the state values
        if (propertyPlusMenu) {
            propertyPlusMenu.style.display = this.state.propertyPlusMenuVisible ? '' : 'none';
        }

        if (customerMenu) {
            customerMenu.style.display = this.state.customerMenuVisible ? '' : 'none';
        }
    }
}

// Register the component in the 'systray' category
registry.category("systray").add("menuVisibility", {
    Component: MenuVisibilityComponent,
    sequence: 10,
});
