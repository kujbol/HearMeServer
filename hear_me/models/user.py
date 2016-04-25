from hear_me.models.base import BaseDocument
from hear_me.models.music import Music
from mongoengine import (
    BooleanField,
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
    birth_date = DateTimeField()
    country = StringField()
    email = StringField()
    last_known_position = PointField()
    image_url = StringField()
    # nick_name = StringField() ADD FORMATTER !!
    token = StringField()

    # Flags
    is_active = BooleanField(required=True)

    # Music
    favorite_music = ListField(ReferenceField(Music, reverse_delete_rule=PULL))
    friends = ListField(ReferenceField('self', reverse_delete_rule=PULL))
    messages = MapField(EmbeddedDocumentField(Message))
    square = ListField(ReferenceField(Music, reverse_delete_rule=PULL))

    meta = {
        'collection': 'User'
    }

    @classmethod
    def from_spotify(cls, spotify_data):
        images = spotify_data['images']
        image_url = images[0]['url'] if images else None
        return cls(
            id=spotify_data['id'],
            email=spotify_data['email'],
            country=spotify_data['country'],
            birth_date=spotify_data['birthdate'],
            image_url=image_url,
            is_active=False,
        )

