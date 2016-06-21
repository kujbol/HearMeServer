import sys

from flask import Flask
from elasticsearch import Elasticsearch


from hear_me.libs.mongo import MongoConnectorFactory
from hear_me.libs.services import service_registry
from hear_me.resources.spotify import SpotifyConnectorFactory
from hear_me.settings import defaults as config

# BluePrints
from hear_me.views.message import message
from hear_me.views.messages_preview import messages
from hear_me.views.user import user
from hear_me.views.settings import settings
from hear_me.views.next_user import next_user


def init_app(settings):
    app = Flask(__name__)
    app.config.from_object(settings.FlaskConfig)
    app.debug = True
    return app


def register_blueprints(app):
    app.register_blueprint(user)
    app.register_blueprint(settings)
    app.register_blueprint(next_user)
    app.register_blueprint(messages)
    app.register_blueprint(message)


def init_services(settings):
    @service_registry.service
    def mongo_connector():
        return MongoConnectorFactory(conf=settings.MongoDBConfig).build()

    @service_registry.service
    def spotify_connector():
        return SpotifyConnectorFactory(config=settings.SpotifySettings).build()

    @service_registry.service
    def elastic_client():
        return Elasticsearch()


def load_settings():
    # TODO add reasonable loading settings
    return config


def get_app():
    settings = load_settings()
    app = init_app(settings)
    register_blueprints(app)
    init_services(settings)
    return app


application = get_app()
