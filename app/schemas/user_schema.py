from marshmallow import Schema, fields


class SaveUserInput(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role_type = fields.Str(required=True)
    verified = fields.Bool()
