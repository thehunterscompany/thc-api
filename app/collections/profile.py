import mongoengine as me

from app.collections.client_type import ClientTypes


class Profiles(me.Document):
    name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    age = me.IntField()
    personal_id = me.StringField(required=True, unique=True)
    income = me.StringField(required=True)
    client_type = me.ReferenceField(document_type=ClientTypes, reverse_delete_rule=me.NULLIFY, required=True)
    client = me.ReferenceField('Clients', required=True)

    def format(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'personal_id': self.personal_id,
            'income': self.income,
            'client_type': self.client_type,
        }

