from flask import Blueprint, request, jsonify

from hear_me.libs.services import service_registry
from hear_me.models.user import User, Square
from hear_me.views.schemas.user import UserSchema

user = Blueprint('user', __name__)
schema = UserSchema()


@user.route('/v1/user', methods=['GET'])
def get_user():
    """ return user data if user exists if not exists then create
    a new user, this view don't use standard authentication
    """
    token = request.headers.get('token')
    spotify_connector = service_registry.services.spotify_connector
    spotify_data = spotify_connector.me(token)
    with service_registry.services.mongo_connector:
        user = User.get_by_id(spotify_data['id'])
        if user is None:
            user = create_new_user(spotify_data, spotify_connector, token)
            user.save()
        return jsonify(schema.serialize(user.to_dict()))


def create_new_user(user_spotify_data, spotify_connector, token):
    user = User.from_spotify(user_spotify_data)

    top_ids = spotify_connector.top(token, ids=True)
    top_tracks = spotify_connector.top(token)
    features_tracks = spotify_connector.audio_features(token, top_ids)

    user.square = Square.create_from_features_top_tracks(
        features_tracks, top_tracks
    )

    return user
