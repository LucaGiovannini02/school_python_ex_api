from marshmallow import Schema, fields
from marshmallow.validate import Range

class GetMovements(Schema):
    CartaFedeltaID = fields.Integer(required=True)
    DataMin = fields.DateTime(required=True)
    DataMax = fields.DateTime(required=True)
    Limit = fields.Integer(validate=[Range(min=1, error="Value must be greater than 0")])