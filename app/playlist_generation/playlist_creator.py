from spotipy import Spotify
from typing import List, Dict
import base64
import io
from PIL import Image
import cv2
import numpy as np
from .spotify_integration import get_spotify_client

def get_mood_seeds(emotion: str) -> Dict:
    return {
        "Happy": {
            "seed_tracks": ["2LawezPeJhN4AWuSB0GtAU", "6Zk3P1UE3dOB6nDs6F2BUi"],  # Happy by Pharrell, Uptown Funk
            "seed_genres": ["pop", "dance"],
            "target_features": {
                "valence": 0.8,    # Very positive
                "energy": 0.8,     # High energy
                "danceability": 0.7
            }
        },
        "Sad": {
            "seed_tracks": ["4pfrrhvplbJZAIsfosGWQP", "7qEHsqek33rTcFNT9PFqLf"],  # Someone Like You, All of Me
            "seed_genres": ["acoustic", "piano"],
            "target_features": {
                "valence": 0.3,    # Negative
                "energy": 0.3,     # Low energy
                "danceability": 0.4
            }
        },
        "Angry": {
            "seed_tracks": ["3YuaBvuZqcwN3CEAyyoaei", "7lQ8MOhq6IN2w8EYcFNSUk"],  # In The End, Numb
            "seed_genres": ["rock", "metal"],
            "target_features": {
                "valence": 0.3,    # Negative
                "energy": 0.9,     # Very high energy
                "danceability": 0.5
            }
        },
        "Neutral": {
            "seed_tracks": ["5jgFfDIR6FR0gvlA56Nakr", "7LVHVU3tWfcxj5aiPFEW4Q"],  # Fix You, Chasing Cars
            "seed_genres": ["indie", "alternative"],
            "target_features": {
                "valence": 0.5,    # Balanced
                "energy": 0.5,
                "danceability": 0.5
            }
        }
    }.get(emotion, {
        "seed_genres": ["pop"],
        "target_features": {
            "valence": 0.5,
            "energy": 0.5,
            "danceability": 0.5
        }
    })

def find_matching_songs(sp: Spotify, emotion: str, limit: int = 20) -> List[str]:
    try:
        mood = get_mood_seeds(emotion)
        
        # Get recommendations using seed tracks and target features
        recommendations = sp.recommendations(
            seed_tracks=mood.get("seed_tracks", [])[:2],
            seed_genres=mood["seed_genres"][:2],
            limit=limit,
            target_valence=mood["target_features"]["valence"],
            target_energy=mood["target_features"]["energy"],
            target_danceability=mood["target_features"]["danceability"],
            min_popularity=40,
            market="US"
        )
        
        if not recommendations or not recommendations['tracks']:
            return []
            
        # Get audio features for all recommended tracks
        track_ids = [track['id'] for track in recommendations['tracks']]
        audio_features = sp.audio_features(track_ids)
        
        # Filter tracks that match our mood criteria
        matching_tracks = []
        for track, features in zip(recommendations['tracks'], audio_features):
            if features and _is_mood_match(features, mood["target_features"]):
                matching_tracks.append(track['uri'])
                
        return matching_tracks[:limit]

    except Exception as e:
        print(f"Error finding matching songs: {str(e)}")
        return []

def _is_mood_match(features: Dict, target: Dict, tolerance: float = 0.2) -> bool:
    """Check if track features match target mood within tolerance"""
    return all(
        abs(features.get(key, 0) - target[key]) <= tolerance
        for key in ['valence', 'energy', 'danceability']
    )

def create_playlist(emotion: str, face_image) -> str:
    sp = get_spotify_client()
    if not sp:
        return None

    try:
        track_uris = find_matching_songs(sp, emotion)
        
        if not track_uris:
            print("No matching songs found. Using broader search...")
            mood = get_mood_seeds(emotion)
            results = sp.search(
                q=f"genre:{mood['seed_genres'][0]}",
                type="track",
                limit=20,
                market="US"
            )
            track_uris = [track["uri"] for track in results["tracks"]["items"]]

        user_id = sp.me()["id"]
        playlist_name = f"{emotion} Mood - AI Generated"
        playlist_description = f"An AI-curated playlist matching your {emotion} emotion"
        
        playlist = sp.user_playlist_create(
            user_id, 
            playlist_name,
            public=True,
            description=playlist_description
        )
        
        if track_uris:
            for i in range(0, len(track_uris), 5):
                batch = track_uris[i:i+5]
                sp.playlist_add_items(playlist["id"], batch)
            
        set_playlist_cover_image(sp, playlist["id"], face_image)
        return playlist["external_urls"]["spotify"]
        
    except Exception as e:
        print(f"Error creating playlist: {str(e)}")
        return None

def set_playlist_cover_image(sp: Spotify, playlist_id: str, face_image) -> None:
    try:
        # Convert CV2 image (BGR) to RGB
        face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image first
        pil_image = Image.fromarray(face_image_rgb)
        
        # Calculate dimensions for a square output maintaining aspect ratio
        target_size = 300  # Spotify's required size
        
        # Get current dimensions
        width, height = pil_image.size
        
        # Calculate scaling factor to fit the smaller dimension to target_size
        # while maintaining aspect ratio
        scale = target_size / min(width, height)
        
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image maintaining aspect ratio
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a white square background
        background = Image.new('RGB', (target_size, target_size), 'white')
        
        # Calculate position to paste the image (center it)
        paste_x = (target_size - new_width) // 2
        paste_y = (target_size - new_height) // 2
        
        # Paste the resized image onto the white background
        background.paste(pil_image, (paste_x, paste_y))
        
        # Save to buffer
        buffer = io.BytesIO()
        background.save(buffer, format='JPEG', quality=95)
        image_data = buffer.getvalue()
        
        # Upload to Spotify
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        sp.playlist_upload_cover_image(playlist_id, encoded_image)
        print("Successfully set playlist cover image")
        
    except Exception as e:
        print(f"Error setting playlist cover image: {str(e)}")