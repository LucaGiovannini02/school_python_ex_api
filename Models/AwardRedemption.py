from marshmallow import Schema, fields
from marshmallow.validate import Range

class AwardRedemption(Schema):
    CartaFedeltaID = fields.Integer(required=True)
    PremioID = fields.Integer(required=True)