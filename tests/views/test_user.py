import pytest
from flask.json import loads

from hear_me.models.user import User
from hear_me.views.schemas.user import UserSchema


@pytest.mark.usefixtures('mongo')
def test_register_empty_db(app, fixt_service_registry, fixt_user):
    headers = {'token': 'fake token'}

    response = app.get('v1/user', headers=headers)
    json = loads(response.data)

    spotify_connector = fixt_service_registry.services.spotify_connector
    spotify_connector.me.assert_called_once_with(headers['token'])
    assert response.status_code == 200
    assert json == UserSchema().serialize(fixt_user.to_dict())
    assert User.get_by_id(json['_id']) is not None


@pytest.mark.usefixtures('mongo')
def test_register_existing_user(app, fixt_service_registry, fixt_user):
    fixt_user.save()
    headers = {'token': 'fake token'}

    response = app.get('v1/user', headers=headers)
    json = loads(response.data)

    spotify_connector = fixt_service_registry.services.spotify_connector
    spotify_connector.me.assert_called_once_with(headers['token'])

    assert response.status_code == 200
    assert json == UserSchema().serialize(fixt_user.to_dict())
    assert User.get_by_id(json['_id']) is not None
