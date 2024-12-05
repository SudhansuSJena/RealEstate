from odoo import http
from odoo.http import request

class RealEstate(http.Controller):
    @http.route('/realestate/my', website=True, auth='public')
    def real_estate_customers(self, **kw):
        customers = request.env["real_estate.customers"].sudo().search([])
        return request.render("real_estate.customers_page", {
            "customers": customers  # Corrected the key name
        })
