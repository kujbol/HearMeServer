from flask import Blueprint, g, jsonify

from hear_me.auth.basic_auth import auth
from hear_me.libs.services import service_registry

login = Blueprint('login', __name__, url_prefix='/v1/login')


@login.route('/', methods=['GET'])
@auth.login_required
def login_token():
    data = service_registry.services.spotify_connector.me(g.user.token)
    return jsonify(data)
