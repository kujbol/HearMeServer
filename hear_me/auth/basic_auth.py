from flask import g
from flask_httpauth import HTTPTokenAuth

from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.resources.base import ClientError

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    try:
        data = service_registry.services.spotify_connector.me(token)
        with service_registry.services.mongo_connector:
            user = User.get_by_id(data['id'])
            if user:
                user.token = token
                user.save()
                g.user = user
                return True
            return False
    except ClientError:
        return False
