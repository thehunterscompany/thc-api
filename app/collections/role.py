import mongoengine as me


class Roles(me.Document):
    type = me.StringField(unique=True, required=True)
    description = me.StringField(null=True)

