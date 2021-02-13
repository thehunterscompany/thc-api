from marshmallow import Schema, fields, validate

from app.schemas.document_schema import SaveDocumentInput


class SaveClientTypeInput(Schema):
    employment_type = fields.Str(required=True)
    documents = fields.List(fields.Nested(SaveDocumentInput()), null=True)
