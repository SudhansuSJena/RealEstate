from odoo import models, fields, api


class RealEstateCustomers(models.Model):
    _name="real_estate.customers"
    _description="Customers to buy property"
    _inherit=['mail.thread'] # Inherit res.users to link with Odoo users

    name = fields.Many2one(
        comodel_name="res.users",
        required=True,
        string="Customer's Name", 
        tracking=True,
        )
    image = fields.Image(string="Customer's Image")
    phone_number = fields.Char(string="Customer's Phone-Number", tracking=True)
    email = fields.Char(string="Customer's email", tracking=True)
    password = fields.Char(string="Password")
    booking_ids = fields.One2many(
        comodel_name="real_estate.bookings",
        inverse_name="customer_id",
        string="Your Bookings",
        domain=[],
        tracking=True
    )

    # User relationship
    user_id = fields.Many2one(
    comodel_name='res.users',
    string='Related User',
    ondelete='cascade',
    help='Link to the Odoo user for authentication purposes.',
    )

    # Access Control
    user_type = fields.Selection(
    [('admin', 'Admin'), ('customer', 'Customer')],
    string="User Type",
    default='customer',
    help="Defines the type of user.",
    )

    rental_contract_ids = fields.One2many(
        comodel_name="real_estate.rent_contracts",
        inverse_name="tenant_id",
        string="Your Rental Contracts",
        domain=[],
        tracking=True,
    )

    sale_contract_ids = fields.One2many(
        comodel_name="real_estate.sale_contracts",
        inverse_name="buyer_id",
        string="Sale Contracts",
        domain=[],
        help="Customer's Sale Contracts",
        tracking=True,
    )

