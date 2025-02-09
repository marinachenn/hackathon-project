import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")  
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")  
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI") 

# OpenCV model paths
FACE_PROTO = "models/opencv_face_detector.pbtxt"
FACE_MODEL = "models/opencv_face_detector_uint8.pb"
EMOTION_MODEL = "models/emotion_detection_model.h5"  # Update to .h5 for Keras model