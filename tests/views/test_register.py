import pytest
from flask.json import loads

from hear_me.models.user import User


@pytest.mark.usefixtures('mongo')
def test_register_empty_db(app, fixt_service_registry):
    headers = {'token': 'fake token'}

    response = app.put('v1/register', headers=headers)
    json = loads(response.data)

    spotify_connector = fixt_service_registry.services.spotify_connector
    spotify_connector.me.assert_called_once_with(headers['token'])
    assert json['_id'] == spotify_connector.me()['id']
    assert User.get_by_id(json['_id']) is not None


@pytest.mark.usefixtures('mongo')
def test_register_existing_user(app, fixt_service_registry, fixt_user):
    fixt_user.save()
    headers = {'token': 'fake token'}

    response = app.put('v1/register', headers=headers)

    spotify_connector = fixt_service_registry.services.spotify_connector
    spotify_connector.me.assert_called_once_with(headers['token'])

    assert response.status_code == 409
