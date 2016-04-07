from hear_me.models.base import BaseDocument
from hear_me.models.music import Music
from mongoengine import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    MapField,
    PointField,
    PULL,
    ReferenceField,
    StringField,
)

from hear_me.models.message import Message


class User(BaseDocument):
    id = StringField(primary_key=True)
    email = StringField()
    token = StringField()
    country = StringField()
    birth_date = DateTimeField()
    last_known_position = PointField()

    favorite_music = ListField(ReferenceField(Music, reverse_delete_rule=PULL))
    square = ListField(ReferenceField(Music, reverse_delete_rule=PULL))
    friends = ListField(ReferenceField('self', reverse_delete_rule=PULL))
    messages = MapField(EmbeddedDocumentField(Message))

    meta = {

    }

    @classmethod
    def from_spotify(cls, spotify_data):
        return cls(
            id=spotify_data['id'],
            email=spotify_data['email'],
            country=spotify_data['country'],
        )

