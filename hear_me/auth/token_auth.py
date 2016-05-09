from functools import wraps

from flask import request, make_response, jsonify


class TokenAuth:
    def __init__(self, callback, scheme='token'):
        self.schema = scheme
        self.callback = callback

    def authenticate(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = request.headers[self.schema]
            except KeyError:
                return self.auth_error_callback("missing token")
            else:
                if not self.callback(token):
                    return self.auth_error_callback("unauthorized")
            return f(*args, **kwargs)
        return decorated

    def auth_error_callback(self, error_msg):
        return jsonify({"auth_error": error_msg}), 401
