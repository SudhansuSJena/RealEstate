from odoo import fields, models


class RealEstateAmenities(models.Model):
    _name="real_estate.amenities"
    _description="Amenities for property"
    _inherit=["mail.thread"]

    
    name = fields.Char(string="Amenity Name", tracking=True)
    description=fields.Char(string="Description", tracking=True)
    # amenity_id = fields.Many2many(
    #     comodel_name = "real_estate.property",
    #     relation = "property_amenity_rel",
    #     column1 = "property_id",
    #     column2 = "amenity_id",
    #     string = "Amenity",
    #     domain = [],
    #     help = 'Choose Amenity'
    # )