from marshmallow import Schema, fields

class SaveClientTypeInput(Schema):
    employment_type = fields.Str(required=True)
    documents = fields.Raw()

class UpdateClientTypeInput(SaveClientTypeInput):
    employment_type = fields.Str(required=False)
