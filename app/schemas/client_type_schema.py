from marshmallow import Schema, fields


class SaveClientTypeInput(Schema):
    employment_type = fields.Str(required=True)
    documents = fields.Raw()
