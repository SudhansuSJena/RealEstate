from odoo import models, fields


class RealEstateConnectivity(models.Model):
    _name = "real_estate.connectivity"
    _description = "Connectivity to Property"
    _inherit = ["mail.thread"]


    name = fields.Char(string="Connectivity Name", tracking=True)
    description = fields.Char(string="Description", tracking=True)