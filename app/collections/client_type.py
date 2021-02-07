import mongoengine as me

from app.collections.document import Documents


class ClientTypes(me.Document):
    employment_type = me.StringField(unique=True)
    documents = me.ListField(me.ReferenceField(Documents, reverse_delete_rule=me.NULLIFY, null=True))

    def format(self):
        return {
            'employment_type': self.employment_type,
            'documents': self.documents
        }

