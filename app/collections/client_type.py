import mongoengine as me

from app.collections.document import Documents


class ClientType(me.Document):
    income = me.StringField()
    employment_type = me.StringField()
    documents = me.ListField(me.ReferenceField(Documents, reverse_delete_rule=me.NULLIFY, null=True))

    def format(self) -> dict:
        return {
            'income': self.income,
            'employment_type': self.employment_type,
            'documents': self.documents
        }
