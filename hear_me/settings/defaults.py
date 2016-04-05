MongoDBConfig = {
    'DB_NAME': 'hear-me',
    'HOST': 'mongodb://localhost',
    'PORT': 27017,
}

FlaskConfig = {
    'DEBUG': True,
    'TESTING': True
}

SpotifySettings = {
    'CLIENT_ID': 'f7dc8845ae8a45c292dc9c94ffab8ddf',
    'CLIENT_SECRET': 'dc129472b74848ca8dec41403776087f',
    'SPOTIFY_AUTH_URL': "https://accounts.spotify.com/authorize",
    'SPOTIFY_TOKEN_URL': "https://accounts.spotify.com/api/token",
    'SPOTIFY_API_URL': "https://api.spotify.com/v1",
    'REDIRECT_URL': 'http://localhost:8888/callback',
    'SCOPE': "user-top-read user-read-private user-read-email "
             "user-follow-read user-read-birthdate",
    'STATE': True,
    'DIALOG': True,
}

SECRET = 'myverylongsecretwhichicreatedonplane'
