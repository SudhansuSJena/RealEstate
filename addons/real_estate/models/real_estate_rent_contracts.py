from odoo import models, fields


class RealEstateRentContracts(models.Model):
    _name = "real_estate.rent_contracts"
    _description = "Property Rental Contracts"
    _inherit = ['mail.thread']

    name = fields.Char(string="Customer's contract Name")
    property_id = fields.Many2one(
        comodel_name="real_estate.property",
        string="Property",
        ondelete='cascade',
        domain=[],
        required=True,
        help='Property that is availabe for renting',
        tracking=True
    )
    rent_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated')
    ], string="Rent's status", tracking=True)
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        domain=[],
        required=True,
        ondelete="cascade",
        help="Inbuilt Currency present in res.currency model of ODOO.",
        tracking=True
    )
    rent_amount = fields.Float(string="Rental Amount", tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    tenant_id = fields.Many2one(
        comodel_name="real_estate.customers",
        string="Tenant of the Property",
        domain=[],
        required=True,
        ondelete="cascade",
        help='Select Tenant of the property',
        tracking=True
    )
