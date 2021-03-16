import mongoengine as me


class CreditLines(me.Document):
    budget = me.StringField(required=True)
    initial_payment = me.StringField(required=True)
    financing_value = me.StringField(required=True)
    credit_line_type = me.StringField(required=True)
    financing_time = me.StringField(required=True)
    client = me.ReferenceField('Clients', required=True)


