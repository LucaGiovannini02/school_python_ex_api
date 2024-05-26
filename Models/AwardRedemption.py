from marshmallow import Schema, fields
from marshmallow.validate import Range

class AwardRedemption(Schema):
    CartaFedeltaID = fields.Integer(required=True)
    PremioID = fields.Integer(required=True)
    SaldoPunti = fields.Integer(required=True, validate=[Range(min=1, error="Value must be greater than 0")])