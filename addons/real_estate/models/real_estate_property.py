from odoo import models, fields, exceptions
import base64
from io import BytesIO
from PIL import Image as PILImage


class RealEstateProperty(models.Model):
    _name = "real_estate.property"
    _description = "REAL ESTATE PROPERTY MASTER"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Property Name", tracking=True)
    
    typeOfProperty = fields.Many2one(
        comodel_name="real_estate.property_types",
        string="Type of Property",
        ondelete="cascade",
        required=True,
        tracking=True,
        help="Select the type of property"
    )

    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('sold', 'Sold'),
        ('leased', 'Leased')
    ], string="Property Status", default='available', tracking=True)

    area = fields.Float(string="Property Area", tracking=True)
    geo_location = fields.Char(string="Geo-Location", tracking=True)

    amenity = fields.Many2many(
        comodel_name="real_estate.amenities",
        relation="property_amenities_rel",
        column1="property_id",
        column2="amenities_id",
        string="Property Amenities",
        tracking=True,
        help="Select Amenities for Property"
    )

    feature = fields.Many2many(
        comodel_name="real_estate.features",
        relation="property_features_rel",
        column1="property_id",
        column2="features_id",
        string="Property Features",
        tracking=True,
        help="Select Features for Property"
    )

    connectivity = fields.Many2many(
        comodel_name="real_estate.connectivity",
        relation="property_connectivity_rel",
        column1="property_id",
        column2="connectivity_id",
        string="Property Connectivity",
        tracking=True,
        help="See the connectivities from the property."
    )

    property_details_id = fields.Many2one(
        comodel_name="real_estate.property_details",
        string="Property Details",
        tracking=True,
        help="Select your property details"
    )

    booking_ids = fields.One2many(
        comodel_name="real_estate.bookings",
        inverse_name="property_id",
        string="Booking",
        help="Booking IDs of Property"
    )

    rent_contract_ids = fields.One2many(
        comodel_name="real_estate.rent_contracts",
        inverse_name="property_id",
        string="Rental Contracts",
        help="Property's Rental Contracts"
    )

    sale_contract_ids = fields.One2many(
        comodel_name="real_estate.sale_contracts",
        inverse_name="property_id",
        string="Sale Contracts",
        help="Property's Sale Contracts"
    )

    image = fields.One2many(
        comodel_name="real_estate.image",
        inverse_name="property_id",
        string="Custom Images",
        help="Images related to the customer"
    )

    image1 = fields.Image(string="Image", max_height=100, max_width=100)

    # image1_base64 = fields.Char(compute="_compute_image1_base64", string="Image Base64", store=False)

    # def _compute_image1_base64(self):
    #     for record in self:
    #         if record.image1:
    #             # Convert the image to base64 string
    #             image_data = base64.b64encode(record.image1).decode('utf-8')
    #             record.image1_base64 = image_data
    #         else:
    #             record.image1_base64 = False

    
