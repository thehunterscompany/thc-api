import mongoengine as me

from app.collections.client_type import ClientType


class Profiles(me.Document):
    name = me.StringField()
    last_name = me.StringField()
    age = me.IntField()
    personal_id = me.StringField(unique=True)
    owners = me.ReferenceField(document_type=ClientType, reverse_delete_rule=me.CASCADE)

    def format(self) -> dict:
        return {
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'personal_id': self.personal_id,
        }

