from flask import Blueprint, g, jsonify

from hear_me.auth.auth import auth
from hear_me.libs.schema import deserialize_schema
from hear_me.models.user import SearchPreferences, SearchSettings
from hear_me.views.schemas.settings import SettingsSchema

settings = Blueprint('settings', __name__)
schema = SettingsSchema()


@settings.route('/v1/settings', methods=['GET'])
@auth.authenticate
def get_settings():
    user = g.user
    return jsonify(schema.serialize(user.to_dict()))


@settings.route('/v1/settings', methods=['POST'])
@auth.authenticate
@deserialize_schema(schema)
def post_settings(deserialized):
    user = g.user
    search_settings = deserialized['search_settings']
    user.search_settings = SearchSettings(**search_settings)

    search_preferences = deserialized['search_preferences']
    user.search_preferences = SearchPreferences(**search_preferences)

    if user.can_be_activated():
        user.active()

    user.save()

    return jsonify(schema.serialize(user.to_dict()))
