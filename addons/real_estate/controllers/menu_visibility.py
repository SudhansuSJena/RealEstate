# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class RealEstateMenuVisibility(http.Controller):
    @http.route('/real_estate/menu_visibility', type='json', auth='user')
    def get_menu_visibility(self):
        """
        Dynamically determine menu visibility based on user groups.
        """
        current_user = request.env.user # Cur

        # Check user groups
        is_admin = current_user.has_group('real_estate.group_real_estate_admin') #  custom admin group
        is_super_admin = current_user.has_group('real_estate.group_real_estate_superadmin') # cuistom superadmin group
        
        # Determine menu visibility
        return {
            'property_plus_menu': is_admin or is_super_admin,  # Only for Admin and SuperAdmin
            'customer_menu': is_admin or is_super_admin,       # Only for Admin and SuperAdmin
        }
