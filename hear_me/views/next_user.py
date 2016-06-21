from flask import Blueprint, g, jsonify

from hear_me.auth.auth import auth
from hear_me.libs.schema import deserialize_schema_wrapper
from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.views.schemas.next_user import (
    NextUserResultSchema,
    NextUserSchema
)

next_user = Blueprint('next_user', __name__)
patch_schema = NextUserResultSchema()
schema = NextUserSchema()


@next_user.route('/v1/next_user', methods=['PATCH'])
@auth.authenticate
@deserialize_schema_wrapper(patch_schema)
def patch_next_user(deserialized):
    user = g.user
    if deserialized.get('like') is True:
        with service_registry.services.mongo_connector:
            liked_user = User.get_by_id(deserialized.get('_id'))
            if user.id in liked_user.liked:
                user.match_user(liked_user)
                user.save()
                liked_user.match_user(user)
                liked_user.save()
                return jsonify({"status": "matched"})
            else:
                user.liked.append(liked_user.id)
                user.save()
                return jsonify({"status": "liked"})

    return jsonify({"status": "not liked"})


@next_user.route('/v1/next_user', methods=['POST'])
@auth.authenticate
def post_next_user():
    user = g.user
    next_user_id = user.get_next_user_id()
    with service_registry.services.mongo_connector:
        next_user = User.get_by_id(next_user_id)
        user.update(push__showed=next_user_id)
        user.save()

    return jsonify(schema.serialize(next_user.to_dict()))
