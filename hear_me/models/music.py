from mongoengine import Document, StringField


class Music(Document):
    title = StringField(required=True)
    url = StringField(required=True)
