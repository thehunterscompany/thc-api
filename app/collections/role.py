import mongoengine as me


class Roles(me.Document):
    type = me.StringField(unique=True)
    description = me.StringField()

    def format(self) -> dict:
        return {
            'type': self.type,
            'description': self.description
        }
