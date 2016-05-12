from flask import Blueprint, g, jsonify

from hear_me.auth.auth import auth
from hear_me.libs.schema import deserialize_schema
from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.views.schemas.next_user import NextUserResultSchema, NextUserSchema

next_user = Blueprint('next_user', __name__)
result_schema = NextUserResultSchema()
schema = NextUserSchema()


@next_user.route('/v1/next_user', methods=['GET'])
@auth.authenticate
def get_next_user():
    user = g.user
    user_id = user.get_next_user_id()
    with service_registry.services.mongo_connector:
        next_user = User.get_by_id(user_id)
    return jsonify(schema.serialize(next_user.to_dict()))


# @next_user.route('/v1/next_user', methods=['POST'])
# @auth.authenticate
# @deserialize_schema(schema)
# def post_square(deserialized):
#     user = g.user