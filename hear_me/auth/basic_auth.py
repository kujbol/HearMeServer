from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from mongoengine import DoesNotExist

from hear_me.models.user import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, token):
    return True