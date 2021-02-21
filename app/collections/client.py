import mongoengine as me

from app.collections.user import Users


class Clients(Users):
    profiles = me.ListField(me.ReferenceField('Profiles'))
    credit_line = me.ReferenceField('CreditLines')
    number_owners = me.IntField()
    referred_by = me.StringField()

    def format(self) -> dict:
        return {
            'email': self.email,
            'password': self.password,
            'role_type': self.role_type,
            'number_owners': self.number_owners,
            'referred_by': self.referred_by,
            'verified': self.verified
        }
