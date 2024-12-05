from odoo import models, fields


class RealEstatePropertyDetails(models.Model):
    _name = "real_estate.property_details"
    _description="Details of RealEstate Property"
    _inherit=["mail.thread"]

    property_id = fields.Many2one(
        comodel_name="real_estate.property",
        string="Property Details",
        ondelete="restrict",
        required=True,
        help='Property details of selected Property',
        tracking=True,
        index=True
    )

    name = fields.Char(string="Detail's Name")

    bedroom_area = fields.Float(string="Bedroom area", tracking=True)
    bathroom_area = fields.Float(string="Bathroom area", tracking=True)
    kitchen_area = fields.Float(string="Kitchen area", tracking=True)
    hall_area = fields.Float(string="Hall area", tracking=True)
    parking_area = fields.Float(string="Parking area", tracking=True)
    backyard_area = fields.Float(string="Backyard area", tracking=True)
    total_bedrooms = fields.Integer(string="Total bedrooms", tracking=True)
    total_bathrooms = fields.Integer(string="Total bathrooms", tracking=True)
    total_floors = fields.Integer(string="Total floors", tracking=True)
    total_halls = fields.Integer(string="Total halls", tracking=True)
    total_parkings = fields.Integer(string="Total parking", tracking=True)
    

    _sql_constraints = [
        ('unique_property', 'UNIQUE(property_id)', 'Each property can only have one details.')
    ]