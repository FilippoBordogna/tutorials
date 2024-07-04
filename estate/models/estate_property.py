from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    three_months_after  = datetime.now() + relativedelta(months=3)
    date_availability = fields.Date(copy=False, default=three_months_after) # Formato mm/gg/aa
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)  
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Where the garden is orientated"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Property State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Current Status of the property",
        required = True,
        default = 'new'
    )