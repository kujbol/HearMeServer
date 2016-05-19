import requests

from hear_me.resources.base import BaseClient
from hear_me.resources.formatters.features import FormatFeaturesTracks
from hear_me.resources.formatters.top import FormatTopTracks


class SpotifyConnectorFactory:
    def __init__(self, config=None):
        self.spotify_api_url = config['SPOTIFY_API_URL']

    def build(self):
        return SpotifyConnector(
            spotify_api_url=self.spotify_api_url
        )


# TODO add formatter
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

    def top(self, token, top_type='tracks', offset=0, limit=100, ids=None):
        url_suffix = '/me/top/' + top_type
        params = {
            "offset": offset,
            "limit": limit,
        }
        response = self.make_call(
            requests.get, url_suffix, headers=self.headers(token), params=params
        )
        if ids:
            return FormatTopTracks.format_top_tracks_ids(response)
        return FormatTopTracks.format_top_tracks(response)

    def audio_features(self, token, track_ids):
        url_suffix = '/audio-features'
        params = {
            "ids": str(track_ids).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
        }
        response = self.make_call(
            requests.get, url_suffix, headers=self.headers(token), params=params
        )
        return FormatFeaturesTracks.format_tracks_features(response)
