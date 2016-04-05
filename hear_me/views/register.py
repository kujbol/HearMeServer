from flask import Blueprint, jsonify

from hear_me.libs.schema import deserialize_schema
from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.resources.base import ClientError
from hear_me.views.schemas.user import UserRegisterSchema

register = Blueprint('register', __name__)
schema = UserRegisterSchema()


# TODO add schema decorator to valid json and throw error
@register.route('/v1/register', methods=['PUT'])
@deserialize_schema(schema)
def post_register(serialized):
    with service_registry.services.mongo_connector:
        token = serialized['token']
        spotify_data = service_registry.services.spotify_connector.me(token)
        user = User.get_by_id(spotify_data['id'])
        if user is not None:
            raise ClientError('server/v1/register/', 409, 'User already exists')

        user = User.from_spotify(spotify_data)
        user.save()

    return jsonify(user.to_dict())
