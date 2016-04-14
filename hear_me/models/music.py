from mongoengine import Document, StringField

from hear_me.models.base import BaseDocument


class Music(BaseDocument):
    title = StringField(required=True)
    url = StringField(required=True)

    meta = {
        'collection': 'Music'
    }