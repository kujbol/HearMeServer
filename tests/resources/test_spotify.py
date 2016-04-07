import pytest
import requests
from mock import patch, sentinel, ANY

from hear_me.resources.spotify import SpotifyConnectorFactory, SpotifyConnector
from hear_me.settings.defaults import SpotifySettings

@pytest.fixture()
def fixt_spotify_connector():
    return SpotifyConnectorFactory(SpotifySettings).build()



@pytest.mark.parametrize(
    'param_method, param_sufix, param_request, param_kwargs, param_payload', [
        ('me', '/me', requests.get, {}, {}),
        ('top', '/top/artist', requests.get, {'top_type': 'artist'}, {}),
        ('top', '/top/tracks', requests.get, {'top_type': 'tracks'}, {}),
    ]
)
@patch.object(SpotifyConnector, 'make_call', autospec=True)
def test_spotify_connector(
        mock_make_call, fixt_spotify_connector,
        param_request, param_sufix, param_method, param_kwargs, param_payload
):
    method = getattr(fixt_spotify_connector, param_method)

    method(sentinel.token, **param_kwargs)
    if param_payload:
        mock_make_call.assert_called_once_with(
            fixt_spotify_connector, param_request, param_sufix,
            headers=fixt_spotify_connector.headers(sentinel.token),
            payload=param_payload
        )
    else:
        mock_make_call.assert_called_once_with(
            fixt_spotify_connector, param_request, param_sufix,
            headers=fixt_spotify_connector.headers(sentinel.token),
        )
