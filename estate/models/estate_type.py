from odoo import models, fields

class estate_type(models.Model):
    _name = "estate.type"
    _description = "Estate Type"

    name = fields.Char(required=True)