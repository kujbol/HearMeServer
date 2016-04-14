from flask import Blueprint, jsonify, request

from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.resources.base import ClientError
from hear_me.views.schemas.user import UserRegisterSchema

register = Blueprint('register', __name__)
schema = UserRegisterSchema()


@register.route('/v1/register', methods=['PUT'])
def post_register():
    token = request.headers.get('token')
    data = service_registry.services.spotify_connector.me(token)
    with service_registry.services.mongo_connector:
        user = User.get_by_id(data['id'])
        if user is not None:
            raise ClientError(
                'server/v1/register/', 409, 'User already exists'
            )
        user = User.from_spotify(data)
        user.save()
        return jsonify(user.to_dict())
