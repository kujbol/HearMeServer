from mongoengine import EmbeddedDocument, DecimalField, StringField
from math import tan, pi


class Music(EmbeddedDocument):
    id = StringField()
    image_url = StringField()

    energy = DecimalField(min_value=0, max_value=1)
    valence = DecimalField(min_value=0, max_value=1)
    danceability = DecimalField(min_value=0, max_value=1)
    tempo = DecimalField()

    # meta = {
    #     'collection': 'Music'
    # }

    def music_category(self):
        return (
            self._music_function(self.energy) +
            self._music_function(self.valence)
        )

    @staticmethod
    def _music_function(value):
        return tan(value * (pi/2.2))
