from colander import(
    MappingSchema,
    OneOf,
    Range,
    SchemaNode,
    SequenceSchema,
)

from hear_me.models.user import available_gender
from hear_me.utils.i18n import available_languages
from hear_me.utils.schema import Boolean, Integer, NullableString


class Languages(SequenceSchema):
    language = SchemaNode(
        NullableString(), validator=OneOf(available_languages)
    )


class Genders(SequenceSchema):
    gender = SchemaNode(NullableString(), validator=OneOf(available_gender))


class SearchSettingsSchema(MappingSchema):
    languages = Languages(default=[])
    gender = SchemaNode(NullableString(), validator=OneOf(available_gender))


class SearchPreferencesSchema(MappingSchema):
    languages = Languages(default=[])
    genders = Genders(default=[])
    age_range_low = SchemaNode(Integer(), validator=Range(1, 99), default=17)
    age_range_top = SchemaNode(Integer(), validator=Range(1, 99), default=99)
    is_in_same_country = SchemaNode(Boolean(), default=False)


class SettingsSchema(MappingSchema):
    search_settings = SearchSettingsSchema()
    search_preferences = SearchPreferencesSchema()
