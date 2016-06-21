import colander
from functools import wraps
from flask import request, jsonify


def deserialize_schema_wrapper(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                deserialized = schema.deserialize(
                    request.get_json(silent=True)
                )
            except colander.Invalid as e:
                return jsonify({"schema_error": e.asdict()}), 400
            return f(deserialized, *args, **kwargs)
        return wrapper
    return decorator