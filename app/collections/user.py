import mongoengine as me

from app.collections.role import Roles


class Users(me.Document):
    email = me.EmailField(unique=True, required=True)
    password = me.StringField(required=True)
    role_type = me.ReferenceField(document_type=Roles, reverse_delete_rule=me.CASCADE, required=True)
    verified = me.BooleanField(default=False)

