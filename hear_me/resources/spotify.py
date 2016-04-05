import json
import requests
from flask import Response


class SpotifyConnectorFactory:
    def __init__(self, config=None):
        # self.auth_query_parameters = {
        #     "response_type": "code",
        #     "redirect_uri": config['REDIRECT_URL'],
        #     "scope": config['SCOPE'],
        #     "client_id": config['CLIENT_ID'],
        #     "state": str(config['STATE']).lower(),
        #     "show_dialog": str(config['DIALOG']).lower(),
        # }
        # self.client_id = config['CLIENT_ID']
        # self.client_secret = config['CLIENT_SECRET']
        self.spotify_api_url = config['SPOTIFY_API_URL']

    def build(self):
        return SpotifyConnector(
            spotify_api_url=self.spotify_api_url
        )


class SpotifyConnector:
    def __init__(self, spotify_api_url):
        self.spotify_api_url = spotify_api_url

    def me(self, token):
        url = self.spotify_api_url + '/me'
        headers = {"Authorization": "Bearer {}".format(token)}
        profile_response = requests.get(url, headers=headers)
        return json.loads(profile_response.text)

    def handle_response(self, response):
        if response.status_code != 200:
            return {
                'status': response.status_code,
                'reason': response.reason,
            }
        else:
            return response.json()
