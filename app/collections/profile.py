import mongoengine as me

from app.collections.client_type import ClientTypes


class Profiles(me.Document):
    name = me.StringField()
    last_name = me.StringField()
    age = me.IntField()
    personal_id = me.StringField(unique=True)
    income = me.StringField()
    client_type = me.ReferenceField(document_type=ClientTypes, reverse_delete_rule=me.CASCADE)

    def format(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'personal_id': self.personal_id,
            'income': self.income,
            'client_type': self.client_type,
        }

