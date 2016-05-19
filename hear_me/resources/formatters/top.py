class FormatTopTracks:
    @staticmethod
    def format_top_tracks(spotify_data):
        return [
            FormatTopTracks._format_track(track)
            for track in spotify_data['items']
        ]

    @staticmethod
    def format_top_tracks_ids(spotify_data):
        return [
            track['id']
            for track in spotify_data['items']
        ]

    @staticmethod
    def _format_track(track):
        return {
            'image_url': (
                None if not track['album'] or not track['album']['images']
                else track['album']['images'][0].get('url')
            ),
            'name': track['name'],
            'id': track['id'],
            'preview_url': track['preview_url']
        }
