from functools import wraps

from flask import request, make_response


class TokenAuth:
    def __init__(self, callback, scheme='token', error_msg='Unauthenticated'):
        self.schema = scheme
        self.callback = callback
        self.error_msg = error_msg

    def authenticate(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = request.headers[self.schema]
            except KeyError:
                return self.auth_error_callback()
            else:
                if not self.callback(token):
                    return self.auth_error_callback()
            return f(*args, **kwargs)
        return decorated

    def auth_error_callback(self):
        res = make_response(self.error_msg)
        res.status_code = 401
        return res
