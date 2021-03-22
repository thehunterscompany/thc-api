from marshmallow import Schema, fields


class SaveClientInput(Schema):
    user = fields.Raw()
    referred_by_non_related = fields.Str()
    referred_by_client = fields.Str()


