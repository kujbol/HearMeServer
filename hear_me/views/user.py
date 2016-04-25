from flask import Blueprint, request, jsonify

from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.views.schemas.user import UserSchema

user = Blueprint('user', __name__)
schema = UserSchema()


@user.route('/v1/user', methods=['GET'])
def get_user():
    """ return user data if user exists if not exists then create
    a new user, this view don't use standard authentication
    """
    token = request.headers.get('token')
    spotify_data = service_registry.services.spotify_connector.me(token)
    with service_registry.services.mongo_connector:
        user = User.get_by_id(spotify_data['id'])
        if user is None:
            user = User.from_spotify(spotify_data)
            user.save()
        return jsonify(schema.serialize(user.to_dict()))


