# controllers/menu_visibility.py
from odoo import http
from odoo.http import request

class MenuVisibilityController(http.Controller):
    @http.route('/real_estate/menu_visibility', type='json', auth='user')
    def get_menu_visibility(self):
        # Get the current user
        current_user = request.env.user

        # Define visibility based on user's groups
        return {
            'property_plus_menu': 
                current_user.has_group('real_estate.group_real_estate_admin') or 
                current_user.has_group('real_estate.group_real_estate_superadmin'),
            
            'customer_menu': 
                current_user.has_group('real_estate.group_real_estate_admin') or 
                current_user.has_group('real_estate.group_real_estate_superadmin')
        }