from odoo import models, fields


class RealEstateFeatures(models.Model):
    _name = "real_estate.features"
    _description = "Real Estate Features"
    _inherit = ["mail.thread"]


    name = fields.Char(string="Feature Name", tracking=True)
    description = fields.Char(string="Description", tracking=True)