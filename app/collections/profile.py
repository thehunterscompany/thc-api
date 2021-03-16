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


