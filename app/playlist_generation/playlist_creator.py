from .spotify_integration import get_spotify_client
import base64
from PIL import Image
import io
import cv2

def set_playlist_cover_image(sp, playlist_id, face_image):
    try:
        # Convert CV2 image (BGR) to PIL Image (RGB)
        face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(face_image_rgb)
        
        # Resize image to Spotify's requirements (300x300)
        max_size = (300, 300)
        pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert image to JPEG format in memory
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG')
        image_data = buffer.getvalue()
        
        # Encode image data as base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        
        # Upload image to playlist
        sp.playlist_upload_cover_image(playlist_id, encoded_image)
        print("Successfully set playlist cover image")
        
    except Exception as e:
        print(f"Error setting playlist cover image: {str(e)}")

def create_playlist(emotion, face_image):
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

    # Set the playlist cover image
    set_playlist_cover_image(sp, playlist["id"], face_image)

    return playlist["external_urls"]["spotify"]