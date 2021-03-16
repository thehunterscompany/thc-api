from mongoengine import StringField, ListField, ReferenceField, NULLIFY, Document
from ..utils import RefQuerySet, parser_one_object, override_result
from .documents import Documents


class ClientTypes(Document):
    employment_type = StringField(unique=True, required=True)
    documents = ListField(ReferenceField(Documents, reverse_delete_rule=NULLIFY, null=True))

    meta = {'queryset_class': RefQuerySet}

    def to_json(self):
        return override_result(self)
