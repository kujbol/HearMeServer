from flask import Blueprint, g, jsonify, request

from hear_me.auth.auth import auth
from hear_me.libs.schema import deserialize_schema_wrapper
from hear_me.libs.services import service_registry
from hear_me.models.message import Message
from hear_me.models.user import User
from hear_me.views.schemas.message import (
    MessagesSchema,
    MessageSchema,
)

message = Blueprint('message', __name__)
post_schema = MessageSchema()
schema = MessagesSchema()


@message.route('/v1/message/<messaged_user_id>', methods=['GET'])
@auth.authenticate
def get_messages(messaged_user_id):
    messages_from = request.args.get('from', 0)
    messages_count = request.args.get('count', 15)
    user = g.user
    if user.messages.get(messaged_user_id):
        return jsonify(schema.serialize(
            {
                'messages': map(
                    lambda message: message.to_dict(),
                    user.messages[messaged_user_id][
                        messages_from:messages_from + messages_count
                    ]
                )
            }
        ))
    return jsonify(schema.serialize({'messages': []}))


@message.route('/v1/message/<messaged_user_id>', methods=['POST'])
@deserialize_schema_wrapper(post_schema)
@auth.authenticate
def post_message(deserialized, messaged_user_id):
    user = g.user
    if messaged_user_id not in user.matched:
        return jsonify({"auth_error": "cannot send message to stranger"}), 401

    with service_registry.services.mongo_connector:
        new_message = Message(**deserialized)
        messaged_user = User.get_by_id(messaged_user_id)
        messaged_user.messages[user.id].append(new_message)
        messaged_user.save()

        user.messages[messaged_user_id].append(new_message)
        user.save()

        return jsonify(post_schema.serialize(new_message.to_mongo().to_dict()))
