from odoo import http
from odoo.http import request
from odoo import fields

class RealEstate(http.Controller):

    @http.route('/', auth="public", website=True)
    def real_estate_website(self, **kwargs):
        return request.render("real_estate.website_front_page", {})

    @http.route('/customer', website=True, auth='public')
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
        
        print("Hello, this is my property.id")
        print(property.id)
        return request.render('real_estate.property_detail_page', {
            'property': property,
        })
    

    @http.route("/buy_propertyy/<model('real_estate.property'):property>", auth="public", website=True)
    def real_estate_buy_property(self, property, **kwargs):
        if not property.exists():
            return request.render('website.404')
        
        # Mark the property as sold
        property.status = "sold"

        # Get the current logged-in user
        current_user = request.env.user

        # Check if the current user is already linked to a customer
        customer = request.env['real_estate.customers'].search([
            ('name', '=', current_user.id)
        ], limit=1)

        if not customer:
           
            customer = request.env['real_estate.customers'].create({
                'name': current_user.id,
                'email': current_user.login,
                'phone_number': current_user.phone,
                'user_id': current_user.id,  
            })

        # Create a new booking linked to the customer and property
        booking = request.env['real_estate.bookings'].create({
            'customer_id': customer.id,
            'property_id': property.id,
            'booking_date': fields.Date.today(),
            'currency_id': current_user.company_id.currency_id.id,
            'payment_price': property.area * 1000,  # Example pricing logic
        })

        # Pass data to the template for rendering
        return request.render('real_estate.buy_property_page', {
            'property': property,
            'booking': booking,
            'customer': current_user,
        })

    
    

    
    
    # @http.route('/my/<name>', auth='public', website='True')
    # def real_estate_name(self, name):
    #     return '<h1>{}<h1>'.format(name)
    
    # @http.route('/your/<int:id>', auth='public', website='True')
    # def real_estate_name(self, id):
    #     return '<h1>{}<h1>'.format(id)
    