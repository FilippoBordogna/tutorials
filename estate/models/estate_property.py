from odoo import models, fields, api, exceptions
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
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _order = "id desc"

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)','Expected Price cannot be negative'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)','Selling Price cannot be negative')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < (0.9 * record.expected_price):
                raise exceptions.UserError("The selling price cannot be less than 90% of the expected price")


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError('A sold property cannot be canceled')
            else:
                record.state = "canceled"

    def sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError('A canceled property cannot be sold')
            else:
                record.state = "sold"