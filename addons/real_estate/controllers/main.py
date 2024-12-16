from odoo import http
from odoo.http import request
from odoo import fields
import base64

class RealEstate(http.Controller):

    @http.route('/', auth="public", website=True)
    def real_estate_website(self, **kwargs):
        return request.render("real_estate.website_front_page", {})

    # SuperAdmin access
    @http.route('/customer', website=True, auth='user')
    def real_estate_customers(self, **kw):
        if not request.env.user.has_group('real_estate.group_real_estate_superadmin'):
            return request.redirect('/web/login')

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
    

    @http.route("/buy_propertyy/<model('real_estate.property'):property>", auth='public', website=True)
    def real_estate_buy_property(self, property, **kwargs):

        # Get the current logged-in user
        current_user = request.env.user
        if current_user._is_public():
            return request.redirect('/web/login')
        

        if not property.exists():
            return request.render('website.404')
        
        # Mark the property as sold
        property.status = "booked"

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

    @http.route("/paymentsuccess/<model('real_estate.property'):property>", auth='public', website=True)
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

        amenity_types = request.env['real_estate.property'].sudo().search([])

        connectivity_types = request.env['real_estate.connectivity'].sudo().search([])

        return request.render('real_estate.property_form_template', {
            'property_types': property_types,
            'amenity_types': amenity_types,
            'connectivity_types': connectivity_types
        })
    

    @http.route('/real_estate/save_property', type='http', auth='public', website=True)
    def save_property(self, **kwargs):
        """
        Handles form submission from the frontend to save a property record in the backend.
        """

        try:
            # Extract form data: # Use `getlist` for multiple values
            name = kwargs.get('name')
            typeOfProperty = kwargs.get('typeOfProperty')
            status = kwargs.get('status')
            area = kwargs.get('area')
            geo_location = kwargs.get('geo_location')
            price = kwargs.get('price')

            if(kwargs.get('image1')):
                # 1. Retrieve uploaded image
                uploaded_file = kwargs.get('image1')
                # uploaded_file is now a FileStorage object.

                # 2. Read the file's binary content
                file_binary = uploaded_file.read()  
                # file_binary contains the raw bytes of the image

                # 3. Encode to base64
                base64_image = base64.b64encode(file_binary)  
                # base64_image is a base64 encoded string representation of the image

            # Handle amenity (multiple selection)
            if(kwargs.get('amenity')):
                amenity_ids = [int(aid) for aid in (kwargs.get('amenity') if isinstance(kwargs.get('amenity'), list) else kwargs.get('amenity').split(','))]

            # Handle connectivity (multiple selection)
            if(kwargs.get('connectivity')):
                connectivity_ids = [int(cid) for cid in (kwargs.get('connectivity') if isinstance(kwargs.get('connectivity'), list) else kwargs.get('connectivity').split(','))]

            # Prepare property dictionary for record creation.
            property_vals = {
                'name': name,
                'typeOfProperty': typeOfProperty,
                'status': status,
                'area': area,
                'geo_location': geo_location,
                'price': float(price) if price else 0.0,
                'image1': base64_image,
                'connectivity': connectivity_ids,
                'amenity': amenity_ids
            }

            # Create Property record.
            request.env['real_estate.property'].sudo().create(property_vals)

            # REDIRECT WITH SUCCESS message
            return request.redirect('/real_estate/add_property?success=1')
        
        except Exception as e:
            # Handle exceptions and rollback if needed
            request.env.cr.rollback()

            # Redirect to error message
            return request.redirect('/real_estate/add_property?error=1')


        

        

        
    
    

    
    
    # @http.route('/my/<name>', auth='public', website='True')
    # def real_estate_name(self, name):
    #     return '<h1>{}<h1>'.format(name)
    
    # @http.route('/your/<int:id>', auth='public', website='True')
    # def real_estate_name(self, id):
    #     return '<h1>{}<h1>'.format(id)
    