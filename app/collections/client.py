import mongoengine as me

from app.collections.user import Users


class Clients(me.Document):
    user = me.ReferenceField(document_type=Users, reverse_delete_rule=me.CASCADE, required=True)
    profiles = me.ListField(me.ReferenceField('Profiles'))
    credit_line = me.ReferenceField('CreditLines')
    number_owners = me.IntField()
    referred_by = me.StringField()

