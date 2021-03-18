from marshmallow import Schema, fields

from app.schemas.user_schema import SaveUserInput


class SaveClientInput(Schema):
    user = fields.Nested(SaveUserInput)
    referred_by_non_related = fields.Str()
    referred_by_client = fields.Str()


