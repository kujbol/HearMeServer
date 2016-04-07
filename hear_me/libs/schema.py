import colander
from functools import wraps
from flask import request, jsonify


def deserialize_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                deserialized = schema.deserialize(request.json)
            except colander.Invalid as e:
                return jsonify({"error": e.message}), 400
            return f(deserialized, *args, **kwargs)
        return wrapper
    return decorator