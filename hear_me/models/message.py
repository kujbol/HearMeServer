from mongoengine import (
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
)


class Message(EmbeddedDocument):
    text = StringField()
    send_date = DateTimeField()
    sender = StringField()


class Conversation(EmbeddedDocument):
    messages = ListField(EmbeddedDocumentField(Message))
