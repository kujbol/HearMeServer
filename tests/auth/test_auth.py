import pytest
from mock import patch

from hear_me.auth.auth import verify_token


@pytest.mark.usefixtures('mongo')
@patch('hear_me.auth.auth.g')
def test_verify_token_ok(mock_g, fixt_service_registry, fixt_user):
    token = 'fake token'
    fixt_user.save()

    result = verify_token(token)
    fixt_user.reload()

    spotify_connector = fixt_service_registry.services.spotify_connector
    spotify_connector.me.assert_called_once_with(token)
    assert fixt_user.token == token
    assert mock_g.user == fixt_user
    assert result is True


@pytest.mark.usefixtures('mongo')
@patch('hear_me.auth.auth.g')
def test_verify_token_missing_user(mock_g, fixt_service_registry):
    token = 'fake token'

    result = verify_token(token)

    assert result is False
