import requests

from hear_me.resources.base import BaseClient


class SpotifyConnectorFactory:
    def __init__(self, config=None):
        self.spotify_api_url = config['SPOTIFY_API_URL']

    def build(self):
        return SpotifyConnector(
            spotify_api_url=self.spotify_api_url
        )


class SpotifyConnector(BaseClient):
    def __init__(self, spotify_api_url):
        super().__init__(spotify_api_url)

    def headers(self, token):
        return {"Authorization": "Bearer {}".format(token)}

    def me(self, token):
        url_suffix = '/me'
        return self.make_call(
            requests.get, url_suffix, headers=self.headers(token)
        )

    def top(self, token, top_type):
        url_suffix = '/top/' + top_type
        return self.make_call(
            requests.get, url_suffix, headers=self.headers(token)
        )
