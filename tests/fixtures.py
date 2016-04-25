from datetime import datetime

import pytest
from mock import Mock
from mongoengine.connection import connect

from hear_me.libs.mongo import MongoConnectorFactory
from hear_me.libs.services import service_registry
from hear_me.main import init_app
from hear_me.models.user import User
from hear_me.resources.spotify import SpotifyConnector
from hear_me.settings import defaults as settings


@pytest.fixture()
def app():
    return init_app(settings).test_client()


@pytest.fixture()
def fixt_user():
    return User(
        id='kujbol',
        birth_date=datetime(1994, 11, 6, 0, 0, 0),
        image_url='http://some.fake.url/img.jpg',
        country='PL',
        email='kujbol@gmail.com',
        is_active=False,
        favorite_music=[],
        square=[],
        friends=[],
        messages={},
    )


@pytest.fixture()
def mock_spotify_con(spotify_me_data):
    spotify_connector = Mock(spec=SpotifyConnector)
    spotify_connector.me.return_value = spotify_me_data
    return spotify_connector


@pytest.fixture()
def fixt_mongo_connector():
    test_settings = {
        'DB_NAME': 'test_db',
        'HOST': 'mongodb://localhost',
        'PORT': 27017,
    }
    return MongoConnectorFactory(conf=test_settings).build()


@pytest.fixture()
def fixt_service_registry(spotify_me_data):
    services = service_registry.services
    services.spotify_connector = mock_spotify_con(spotify_me_data)
    services.mongo_connector = fixt_mongo_connector()
    return service_registry


@pytest.fixture()
def spotify_me_data():
    return {
        "birthdate": "1994-11-06",
        "country": "PL",
        "display_name": None,
        "email": "kujbol@gmail.com",
        "external_urls": {
            "spotify": "https://open.spotify.com/user/kujbol"
        },
        "followers": {
            "href": None,
            "total": 0
        },
        "href": "https://api.spotify.com/v1/users/kujbol",
        "id": "kujbol",
        "images": [],
        "product": "premium",
        "type": "user",
        "uri": "spotify:user:kujbol"
    }


@pytest.yield_fixture()
def mongo():
    db_alias = connect('test_db')
    yield db_alias
    db_alias.drop_database('test_db')
