import datetime

from flask import Blueprint, g, jsonify

from hear_me.auth.auth import auth
from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.views.schemas.messages_preview import (
    MessagePreview,
    MessagesPreview
)

messages = Blueprint('messages', __name__)
message_preview_schema = MessagePreview()
schema = MessagesPreview()


@messages.route('/v1/messages', methods=['GET'])
@auth.authenticate
def get_messages():
    user = g.user
    result = {
        'conversations_preview': [
            prepare_message_preview(user_id, messages)
            for user_id, messages in user.messages.items()
        ]
    }
    return jsonify(schema.serialize(result))


def prepare_message_preview(user_id, messages):
    with service_registry.services.mongo_connector:
        user_preview = User.get_by_id(user_id)
        if messages:
            return message_preview_schema.serialize({
                '_id': user_preview.id,
                'last_message': messages[0].text[:50],
                'display_name': user_preview.display_name or user_preview.id,
                'image_url': user_preview.image_url
            })
        else:
            return message_preview_schema.serialize(user_preview.to_dict())
