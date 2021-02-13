from marshmallow import Schema, fields, validate


class SaveRoleInput(Schema):
    type = fields.Str(required=True)
    description = fields.Str()
