from mongoengine import Document, StringField, BooleanField

class Documents(Document):
    name = StringField(min_length=2, required=True)
    active = BooleanField(default=False)

    # def format(self):
    #     return {
    #         'name': self.name,
    #         'active': self.active,
    #     }
