import mongoengine as me


class Roles(me.Document):
    type = me.StringField(unique=True, required=True)
    description = me.StringField(null=True)

    def format(self) -> dict:
        return {
            'type': self.type,
            'description': self.description
        }
