from marshmallow import Schema, fields

class AddPoints(Schema):
    CartaFedeltaID = fields.Integer(required=True)
    SaldoPunti = fields.Integer(required=True)