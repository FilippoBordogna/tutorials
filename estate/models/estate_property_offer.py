from odoo import models, fields, api, exceptions
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

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)','Price cannot be negative')
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def accept_offer(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise exceptions.UserError('The property is already sold')
            else:
                record.property_id.state = 'sold'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.state = 'accepted'    

    def refuse_offer(self):
        for record in self:
            record.state = 'refused'

    def _onchange_state(self):
        if self.state == 'accepted':
            if self.property_id.state == 'sold':
                raise exceptions.UserError('The property is already sold')
            else:
                self.property_id.state = 'sold'
                self.property_id.selling_price = self.price
                self.property_id.buyer = self.partner_id