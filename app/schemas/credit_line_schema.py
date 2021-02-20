from marshmallow import Schema, fields, validate


class SaveCreditLineInput(Schema):
    budget = fields.Str(required=True)
    initial_payment = fields.Str(required=True)
    financing_value = fields.Str(required=True)
    credit_line_type = fields.Str(required=True)
    financing_time = fields.Str(required=True)
    client = fields.Raw(required=True)
