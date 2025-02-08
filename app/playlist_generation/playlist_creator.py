from spotify_integration import get_spotify_client

def create_playlist(emotion):
    sp = get_spotify_client()

    # Map emotions to Spotify search queries
    emotion_to_query = {
        "Happy": "happy",
        "Sad": "sad",
        "Angry": "angry",
        "Surprise": "exciting",
        "Fear": "calm",
        "Neutral": "chill"
    }

    # Search for tracks based on emotion
    query = emotion_to_query.get(emotion, "chill")
    results = sp.search(q=query, type="track", limit=10)

    # Extract track URIs
    track_uris = [track["uri"] for track in results["tracks"]["items"]]

    # Create a new playlist
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, f"{emotion} Mood Playlist", public=True)
    sp.playlist_add_items(playlist["id"], track_uris)

    return playlist["external_urls"]["spotify"]