from odoo import http
from odoo.http import request
from odoo import fields
import base64

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
        property.status = "booked"

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
            'booking_status': 'pending'
        })

        # Pass data to the template for rendering
        return request.render('real_estate.buy_property_page', {
            'property': property,
            'booking': booking,
            'customer': current_user,
        })

    @http.route("/paymentsuccess/<model('real_estate.property'):property>", auth="public", website=True)
    def real_estate_payment_success(self, property, **kwargs):
        if not property.exists():
            return request.render('website.404')
        
        property.status = "sold"

        current_user = request.env.user
        customer = request.env['real_estate.customers'].search([('name', '=', current_user.id)], limit=1)

        # It returns a list of dictionaries, even if there is only one record
        payment_price = request.env['real_estate.bookings'].search_read([
            ('customer_id', '=', customer.id),
            ('property_id', '=', property.id)
        ], ['payment_price'])

        if(payment_price):
            payment_price = payment_price[0]['payment_price']
        else:
            payment_price = 0.0

        
        sale = request.env['real_estate.sale_contracts'].create({
            'name': customer.id,
            'property_id': property.id,
            'currency_id': current_user.company_id.currency_id.id,
            'sale_date': fields.Date.today(),
            'sale_price': payment_price
        })

        booking = request.env['real_estate.bookings'].create({
            'customer_id': customer.id,
            'property_id': property.id,
            'booking_date': fields.Date.today(),
            'currency_id': current_user.company_id.currency_id.id,
            'payment_price': payment_price,  # Example pricing logic
            'booking_status': 'confirmed'
        })

        return request.render("real_estate.property_payment_successful", 
        {
            'sale':sale,
            'booking':booking,
            'customer':customer,
            'property':property
        })
    
    @http.route('/real_estate/add_property', type='http', auth='user', website=True)
    def add_property_form(self):
        # Get property types for the dropdown
        property_types = request.env['real_estate.property_types'].sudo().search([])

        return request.render('real_estate.property_form_template', {
            'property_types': property_types
        })
    

    @http.route('/real_estate/save_property', type='http', auth='public', website=True)
    def save_property(self, name, typeOfProperty, status, price, description=None, address=None, image=None):
        try:
            property_vals = {
                'name': name,
                'typeOfProperty': typeOfProperty,
                'status': status,
                'price': float(price),
                'description': description or False,
                'address': address or False,
            }

            # Handle image upload
            if(image):
                property_vals = base64.b64encode(image.read())

            # Create property record.
            property_obj = request.env['real_estate.property'].sudo()
            new_property = property_obj.create(property_vals)

            return request.redirect('/real_estate/add_property?success=1')
        
        except Exception as e:
            # Log the error and redirect with an error message
            request.env['ir.logging'].sudo().create({
                'name': 'Property Creation Error',
                'type': 'server',
                'dbname': request.env.cr.dbname,
                'level': 'error',
                'message': str(e),
                'path': '/real_estate/save_property',
                'func': 'save_property',
                'line': '0'
            })
            return request.redirect('/real_estate/add_property?error=1')


        
    
    

    
    
    # @http.route('/my/<name>', auth='public', website='True')
    # def real_estate_name(self, name):
    #     return '<h1>{}<h1>'.format(name)
    
    # @http.route('/your/<int:id>', auth='public', website='True')
    # def real_estate_name(self, id):
    #     return '<h1>{}<h1>'.format(id)
    