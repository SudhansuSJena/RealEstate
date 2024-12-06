from odoo import models, fields


class RealEstateImage(models.Model):
    _name="real_estate.image"
    _description="Choose image for CUSTOMER OR PROPERTY"


    name = fields.Char(string="Image name")
    image = fields.Image(string="Image", required=True, help="Image File")
    image_type = fields.Selection([
        ('property', 'Property'),
        ('customer', 'Customer')
    ],
    string="Image Type",
    required=True,
    help="Specify if this image belongs to a Property or a Customer"
    )

    property_id = fields.Many2one(
        comodel_name="real_estate.property",
        string="Property",
        help="Select the property if the image belongs to a property",
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        help="Select the customer if the image belongs to a customer",
    )

    