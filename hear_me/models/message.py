from mongoengine import (
    DateTimeField,
    EmbeddedDocument,
    StringField,
)


class Message(EmbeddedDocument):
    text = StringField()
    send_date = DateTimeField()
    sender = StringField()

    def to_dict(self):
        return self.to_mongo().to_dict()
