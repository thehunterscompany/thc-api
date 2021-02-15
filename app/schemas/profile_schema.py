from marshmallow import Schema, fields

from app.schemas.client_type_schema import SaveClientTypeInput


class SaveProfileInput(Schema):
    name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    personal_id = fields.Str(unique=True)
    income = fields.Str()
    client_type = fields.Nested(SaveClientTypeInput(), required=True)

