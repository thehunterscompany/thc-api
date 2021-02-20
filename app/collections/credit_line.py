import mongoengine as me

from app.collections.client import Clients


class CreditLines(me.Document):
    budget = me.StringField(required=True)
    initial_payment = me.StringField(required=True)
    financing_value = me.StringField(required=True)
    credit_line_type = me.StringField(required=True)
    financing_time = me.StringField(required=True)
    client = me.ReferenceField(document_type=Clients, reverse_delete_rule=me.CASCADE, required=True)

    def format(self):
        return {
            'budget': self.budget,
            'initial_payment': self.initial_payment,
            'financing_value': self.financing_value,
            'credit_line_type': self.credit_line_type,
            'financing_time': self.financing_time,
        }



