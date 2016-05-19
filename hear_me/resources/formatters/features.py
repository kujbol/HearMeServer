from decimal import Decimal


class FormatFeaturesTracks:
    @staticmethod
    def format_tracks_features(spotify_data):
        return [
            FormatFeaturesTracks._format_track_feature(track)
            for track in spotify_data['audio_features']
        ]

    @staticmethod
    def _format_track_feature(track):
        return {
            'energy': Decimal(track['energy']),
            'valence': Decimal(track['valence']),
            'danceability': Decimal(track['danceability']),
            'tempo': Decimal(track['tempo']),
        }