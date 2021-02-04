import mongoengine as me


class CreditLines(me.Document):
    budget = me.StringField()
    initial_payment = me.StringField()
    financing_value = me.StringField()
    credit_line_type = me.StringField()
    financing_time = me.StringField()

    def format(self) -> dict:
        return {
            'budget': self.budget,
            'initial_payment': self.initial_payment,
            'financing_value': self.financing_value,
            'credit_line_type': self.credit_line_type,
            'financing_time': self.financing_time,
        }
