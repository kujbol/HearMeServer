from mongoengine import EmbeddedDocument, ListField, StringField, DateTimeField


class Conversation(EmbeddedDocument):
    messages = ListField()


class Message(EmbeddedDocument):
    text = StringField()
    send_date = DateTimeField()
    sender = StringField()

