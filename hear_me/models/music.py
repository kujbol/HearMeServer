from enum import Enum

from decimal import Decimal
from mongoengine import EmbeddedDocument, DecimalField, StringField
from math import tan, pi


class MusicEnum(Enum):
    energy = 10
    sadness = 1
    relax = 4


class MusicType:
    def __init__(self, music):
        self.value = music.music_category()
        self.music = music
        self.enum = MusicEnum.energy
        for enum in MusicEnum:
            if abs(self.value - self.enum.value) > abs(self.value - enum.value):
                self.enum = enum


class Music(EmbeddedDocument):
    id = StringField()
    name = StringField()
    preview_url = StringField()
    image_url = StringField()

    energy = DecimalField(min_value=0, max_value=1)
    valence = DecimalField(min_value=0, max_value=1)
    danceability = DecimalField(min_value=0, max_value=1)
    tempo = DecimalField()

    @classmethod
    def from_track_features_top(cls, track_features, track_top):
        user_dict = {}
        user_dict.update(track_features)
        user_dict.update(track_top)

        return cls(**user_dict)

    @staticmethod
    def _music_function(value):
        return tan(value * Decimal(pi/2.1))

    # meta = {
    #     'collection': 'Music'
    # }

    def music_category(self):
        return (
            self._music_function(self.energy) +
            self._music_function(self.valence)
        )
