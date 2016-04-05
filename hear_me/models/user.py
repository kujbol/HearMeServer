from hear_me.libs.services import service_registry
from hear_me.models.music import Music
from mongoengine import (
    DateTimeField,
    Document,
    DoesNotExist,
    EmbeddedDocumentField,
    ListField,
    MapField,
    PointField,
    PULL,
    ReferenceField,
    StringField,
)

from hear_me.models.message import Message


class User(Document):
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

    def to_dict(self):
        return self.to_mongo().to_dict()

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.get(id=id)
        except DoesNotExist:
            return None

    @classmethod
    def from_spotify(cls, spotify_data):
        return cls(
            id=spotify_data['id'],
            email=spotify_data['email'],
            country=spotify_data['country'],
        )

