from marshmallow import Schema, fields, validate

class SaveDocumentInput(Schema):
    name = fields.Str(required=True)
    active = fields.Boolean(required=False)

class UpdateDocumentInput(SaveDocumentInput):
    name = fields.Str(required=False)
