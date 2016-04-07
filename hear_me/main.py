import sys

from flask import Flask
from elasticsearch import Elasticsearch


from hear_me.libs.mongo import MongoConnectorFactory
from hear_me.libs.services import service_registry
from hear_me.resources.spotify import SpotifyConnectorFactory
from hear_me.settings import defaults as config

# BluePrints
from hear_me.views.login import login
from hear_me.views.register import register


def init_app(settings):
    app = Flask(__name__)
    app.config.from_object(settings.FlaskConfig)
    app.debug = True
    app.register_blueprint(register)
    app.register_blueprint(login)

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


if __name__ == '__main__':
    settings = load_settings()
    app = init_app(settings)
    init_services(settings)
    app.run()
