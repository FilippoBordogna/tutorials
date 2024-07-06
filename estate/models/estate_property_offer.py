from odoo import models, fields

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    state = fields.Selection(
        string='Offer State',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Current Status of the offer",
        copy=False
    )
    partner_id=fields.Many2one("res.partner", string="Offerer")
    property_id=fields.Many2one("estate.property", string="Property of the offer")