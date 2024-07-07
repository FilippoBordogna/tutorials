from odoo import models, fields, api
from datetime import datetime, timedelta 

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
    partner_id = fields.Many2one("res.partner", string="Offerer")
    property_id = fields.Many2one("estate.property", string="Property of the offer")
    
    validity = fields.Integer(default=7)
    create_date = fields.Date(default = datetime.now())
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days