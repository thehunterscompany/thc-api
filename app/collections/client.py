import mongoengine as me

from app.collections.client_type import ClientType
from app.collections.credit_line import CreditLines
from app.collections.user import Users
from app.collections.profile import Profiles


class Clients(Users):
    profile = me.ListField(me.ReferenceField(document_type=Profiles, reverse_delete_rule=me.CASCADE))
    credit_line = me.ReferenceField(document_type=CreditLines, reverse_delete_rule=me.CASCADE)
    number_owners = me.IntField()
    referred_by = me.StringField()

    def format(self) -> dict:
        return {
            'email': self.email,
            'password': self.password,
            'role_type': self.role_type,
            'profile': self.profile,
            'credit_line': self.credit_line,
            'number_owners': self.number_owners,
            'referred_by': self.referred_by
        }