import sys

from flask import Flask
from elasticsearch import Elasticsearch


from hear_me.libs.mongo import MongoConnectorFactory
from hear_me.libs.services import service_registry
from hear_me.resources.spotify import SpotifyConnectorFactory
from hear_me.settings import defaults as config

# BluePrints
from hear_me.views.user import user


def init_app(settings):
    app = Flask(__name__)
    app.config.from_object(settings.FlaskConfig)
    app.debug = True
    app.register_blueprint(user)

    return app


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
    if len(sys.argv) == 1:
        return config
    else:
        return None


def get_app():
    settings = load_settings()
    app = init_app(settings)
    init_services(settings)
    return app


application = get_app()
