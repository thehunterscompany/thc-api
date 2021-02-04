import mongoengine as me


class Documents(me.Document):
    name = me.StringField()
    active = me.BooleanField(default=False)

    def format(self):
        return {
            'name': self.name,
            'active': self.active,
        }
