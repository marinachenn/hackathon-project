import numpy as np
import cv2
from deepface import DeepFace
import os

def detect_emotion(face_image):
    try:
        # Analyze the face using DeepFace
        result = DeepFace.analyze(
            face_image, 
            actions=['emotion'],
            enforce_detection=False,
            silent=True
        )
        
        # Get the dominant emotion
        emotion = result[0]['dominant_emotion']
        
        # Map emotions to our playlist categories
        emotion_mapping = {
            'angry': 'Angry',
            'disgust': 'Disgust',
            'fear': 'Fear',
            'happy': 'Happy',
            'sad': 'Sad',
            'surprise': 'Surprise',
            'neutral': 'Neutral'
        }
        
        mapped_emotion = emotion_mapping.get(emotion, 'Neutral')
        print(f"Detected Emotion: {mapped_emotion}")
        return mapped_emotion

    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return "Neutral"

