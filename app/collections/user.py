import json

import mongoengine as me

from app.collections.role import Roles


class Users(me.Document):
    email = me.EmailField(unique=True)
    password = me.StringField()
    role_type = me.ReferenceField(document_type=Roles, reverse_delete_rule=me.CASCADE)

    meta = {'allow_inheritance': True}

    def format(self):
        user_dict = {
            'email': self.email,
            'password': self.password,
            'role_type': self.role_type
        }

        return json.dumps(user_dict)
