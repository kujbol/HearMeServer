import pytest

from hear_me.main import init_app
from hear_me.models.user import User

from mongoengine.connection import connect


@pytest.fixture()
def app():
    return init_app().test_client()


@pytest.fixture()
def fixt_user():
    return User(
        id=1,
        name=u'jeremy',
        surname=u'jarecki',
        email=u'my@email.com',
        username=u'jeremy',
        favorite_music=[],
        square=[],
        friends=[],
        messages={},
    )


@pytest.yield_fixture()
def mongo():
    db_alias = connect('test_db')
    yield db_alias
    db_alias.drop_database('test_db')
