from odoo import fields, models


class RealEstateSaleContracts(models.Model):
    _name = "real_estate.sale_contracts"
    _description = "Sale contracts for Property"
    _inherit = ['mail.thread']
    _res_name = ['buyer_id']

    name = fields.Many2one(
        comodel_name="real_estate.customers",
        string="Customer",
        ondelete="cascade",
        domain=[],
        help='customers',
        tracking=True
    )
    property_id = fields.Many2one(
        comodel_name = "real_estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
        domain=[],
        help='Select property for Sale',
        tracking=True
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        ondelete="cascade",
        domain=[],
        help='Select the currency.',
        tracking=True
    )
    sale_date = fields.Date(string="Sale's Date", tracking=True)
    sale_status = fields.Selection([
        ('drafted', 'Drafted'),
        ('signed', 'Signed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Sale's status", tracking=True)
    buyer_id = fields.Many2one(
        comodel_name="real_estate.customers",
        string="Buyer",
        ondelete="cascade",
        domain=[],
        help='Customer buying Property',
        tracking=True
    )
    sale_price = fields.Float(string="Sale's Price", tracking=True)