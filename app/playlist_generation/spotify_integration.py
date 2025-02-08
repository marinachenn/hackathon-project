import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = "c4110e5fece54345bb41eebe465667d7"
SPOTIFY_CLIENT_SECRET = "5e735b51a16c493bb3d32224750f4ce3"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-public"
    ))
    return sp