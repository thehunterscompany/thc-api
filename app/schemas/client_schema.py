from marshmallow import Schema, fields


class SaveClientInput(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role_type = fields.Raw(required=True)
    verified = fields.Bool()
    referred_by = fields.Str()
    credit_line = fields.Raw()
