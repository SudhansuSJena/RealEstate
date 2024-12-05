from odoo import models, fields


class RealEstateBookings(models.Model):
    _name="real_estate.bookings"
    _description="Property Bookings"
    _inherit=['mail.thread']


    customer_id = fields.Many2one(
        comodel_name="real_estate.customers",
        string="Customer",
        ondelete="cascade",
        domain=[],
        help='Select customers',
        tracking=True
    )

    property_id = fields.Many2one(
        comodel_name="real_estate.property",
        string="Select Property",
        ondelete="cascade",
        domain=[],
        help="Select properties",
        tracking=True
    )

    booking_date = fields.Date(string="Date", tracking=True)
    booking_status = fields.Selection([
        ('pending', 'Pending'), 
        ('confirmed', 'Confirmed'), 
        ('cancelled', 'Cancelled')
        ], string="Booking status", tracking=True)
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        ondelete="cascade",
        domain=[],
        required=True,
        help='Inbuilt Currency in res.currency model',
        tracking=True
    )
    payment_price = fields.Float(string="Payment", tracking=True)
    booking_hours = fields.Char(string="Booking Hours", tracking=True)