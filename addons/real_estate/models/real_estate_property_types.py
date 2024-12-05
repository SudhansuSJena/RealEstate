from odoo import fields, models, exceptions


class RealEstatePropertyTypes(models.Model):
    _name = "real_estate.property_types"
    _description = "PROPERTY TYPES"
    _inherit = ["mail.thread"]


    name = fields.Char(string="Property-type Name", required=True, tracking=True)
