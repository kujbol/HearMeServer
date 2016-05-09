from flask import g

from hear_me.auth.token_auth import TokenAuth
from hear_me.libs.services import service_registry
from hear_me.models.user import User
from hear_me.resources.base import ClientError


def verify_token(token):
    g.user = None
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

auth = TokenAuth(verify_token, scheme='token')
