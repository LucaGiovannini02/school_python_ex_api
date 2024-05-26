from marshmallow import Schema, fields

class Card(Schema):
    Titolare = fields.String(required=True)
    SaldoPunti = fields.Integer()