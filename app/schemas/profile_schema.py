from marshmallow import Schema, fields

from app.schemas.client_type_schema import SaveClientTypeInput


class SaveProfileInput(Schema):
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    age = fields.Int()
    personal_id = fields.Str(unique=True, required=True)
    income = fields.Str(required=True)
    client_type = fields.Raw(required=True)

