import mongoengine as me

from app.collections.user import Users


class Clients(me.Document):
    user = me.ReferenceField(document_type=Users, reverse_delete_rule=me.CASCADE, required=True)
    profiles = me.ListField(me.ReferenceField('Profiles'), null=True)
    credit_line = me.ReferenceField('CreditLines', null=True)
    referred_by_non_related = me.StringField()
    referred_by_client = me.ReferenceField('Clients', null=True)


