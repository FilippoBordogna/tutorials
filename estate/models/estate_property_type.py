from odoo import models, fields

class estate_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer()

    _order = "sequence"

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)','The name of the type must be unique')
    ]