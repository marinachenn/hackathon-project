import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spotify_client():
    try:
        # Get credentials from environment variables
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError("Missing Spotify credentials in environment variables")

        # Define all required scopes
        scopes = [
            'playlist-modify-public',
            'playlist-modify-private',
            'ugc-image-upload'
        ]
        
        # Create Spotify client with all necessary scopes
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=' '.join(scopes)
        ))
        
        # Test the connection
        sp.current_user()  # This will raise an exception if authentication fails
        return sp

    except Exception as e:
        print(f"Spotify Authentication Error: {str(e)}")
        print("Please ensure your .env file contains valid Spotify credentials:")
        print("SPOTIPY_CLIENT_ID=your_client_id")
        print("SPOTIPY_CLIENT_SECRET=your_client_secret")
        print("SPOTIPY_REDIRECT_URI=http://localhost:8888/callback")
        return None