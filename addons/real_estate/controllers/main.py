from odoo import http
from odoo.http import request

class RealEstate(http.Controller):
    @http.route('/realestate/my', website=True, auth='public')
    def real_estate_customers(self, **kw):
        customers = request.env["real_estate.customers"].sudo().search([])
        return request.render("real_estate.customers_page", {
            "customers": customers  # Corrected the key name
        })
    
    
    @http.route('/property', auth='public', website=True)
    def real_estate_property(self, **kwargs):
        properties = request.env["real_estate.property"].sudo().search([])
        return request.render("real_estate.product_page", {"properties": properties})
    

    @http.route('/property/<model("real_estate.property"):property>', auth='public', website=True)
    def real_estate_property_detail(self, property, **kwargs):
        if not property.exists():
            return request.render('website.404')  # Render 404 page if property doesn't exist
        return request.render('real_estate.property_detail_page', {
            'property': property,
        })

    
    
    # @http.route('/my/<name>', auth='public', website='True')
    # def real_estate_name(self, name):
    #     return '<h1>{}<h1>'.format(name)
    
    # @http.route('/your/<int:id>', auth='public', website='True')
    # def real_estate_name(self, id):
    #     return '<h1>{}<h1>'.format(id)
    