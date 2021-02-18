from marshmallow import Schema, fields

from app.collections.profile import Profiles


class SaveClientInput(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role_type = fields.Raw(required=True)
    profiles = fields.Raw(required=True)
    credit_line = fields.Raw(required=True)
    verified = fields.Bool()

