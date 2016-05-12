from mongoengine import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    IntField,
    ListField,
    MapField,
    PointField,
    PULL,
    ReferenceField,
    StringField,
)

from hear_me.libs.services import service_registry
from hear_me.models.base import BaseDocument
from hear_me.models.message import Message
from hear_me.models.music import Music
from hear_me.utils.i18n import available_languages


available_gender = ['male', 'female']


class SearchSettings(EmbeddedDocument):
    gender = StringField(choices=available_gender)
    languages = ListField(StringField(choices=available_languages))

    def is_ready(self):
        return self.gender and len(self.languages)


class SearchPreferences(EmbeddedDocument):
    genders = ListField(StringField(choices=available_gender))
    languages = ListField(StringField(choices=available_languages))
    age_range_low = IntField(min_value=1, max_value=99)
    age_range_top = IntField(min_value=1, max_value=99)
    is_in_same_country = BooleanField()

    def is_ready(self):
        return (
            self.genders and len(self.languages) and
            self.age_range_low and self.age_range_top
        )


class Square(EmbeddedDocument):
    energy = EmbeddedDocumentField(Music)
    sadness = EmbeddedDocumentField(Music)
    relax = EmbeddedDocumentField(Music)
    top = EmbeddedDocumentField(Music)


class User(BaseDocument):
    id = StringField(primary_key=True)
    visible_name = StringField()
    birth_date = DateTimeField()
    country = StringField()
    email = StringField()
    last_known_position = PointField()
    image_url = StringField()
    token = StringField()

    # Search
    search_settings = EmbeddedDocumentField(SearchSettings)
    search_preferences = EmbeddedDocumentField(SearchPreferences)

    # Flags
    is_active = BooleanField(required=True)

    # Music
    friends = ListField(ReferenceField('self', reverse_delete_rule=PULL))
    messages = MapField(EmbeddedDocumentField(Message))
    square = EmbeddedDocumentField(Square)

    meta = {
        'collection': 'User'
    }

    def can_be_activated(self):
        return (
            self.search_settings.is_ready() and
            self.search_preferences.is_ready()
        )

    def active(self):
        self.is_active = True

    def get_next_user_id(self):
        # TODO change this mock for something reasonable -> send data to elastic
        with service_registry.services.mongo_connector:
            for user in User.objects():
                if user.id != self.id:
                    return user.id
            return self.id

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
