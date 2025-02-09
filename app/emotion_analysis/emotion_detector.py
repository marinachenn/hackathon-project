import numpy as np
import cv2
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.preprocessing.image import img_to_array
import base64
from PIL import Image
import io

# Define the model architecture
def create_emotion_model():
    model = Sequential()
    
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))
    
    return model

# Create the model
model = create_emotion_model()

# Load pre-trained weights if available
try:
    model.load_weights("models/emotion_detection_model.h5")
except:
    print("Warning: Could not load model weights. Using untrained model.")
    print("Please ensure you have the model file in the models/ directory")

emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def detect_emotion(face_image):
    try:
        # Preprocess the face image for the model
        resized_image = cv2.resize(face_image, (48, 48))  # Resize to 48x48
        grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        image_array = img_to_array(grayscale_image)  # Convert to array
        image_array = image_array.reshape((1, 48, 48, 1))  # Reshape to (1, 48, 48, 1)
        image_array = image_array.astype('float32') / 255.0  # Normalize pixel values

        # Predict emotion
        predictions = model.predict(image_array)
        emotion_index = np.argmax(predictions)
        emotion = emotion_labels[emotion_index]
        
        return emotion
    except Exception as e:
        print(f"Error in detect_emotion: {str(e)}")
        return "Unknown"

def set_playlist_cover_image(sp, playlist_id, image_path):
    try:
        # Open and resize image to Spotify's requirements (must be under 256KB)
        image = Image.open(image_path)
        
        # Resize image if needed (Spotify recommends 300x300 to 3000x3000 pixels)
        max_size = (300, 300)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert image to JPEG format in memory
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_data = buffer.getvalue()
        
        # Encode image data as base64
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        
        # Upload image to playlist
        sp.playlist_upload_cover_image(playlist_id, encoded_image)
        print("Successfully set playlist cover image")
        
    except Exception as e:
        print(f"Error setting playlist cover image: {str(e)}")

