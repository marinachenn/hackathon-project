import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load the pre-trained emotion detection model
model = load_model("path_to_pretrained_model.h5")  # Replace with actual model path
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def detect_emotion(face_image):
    # Preprocess the face image for the model
    resized_image = cv2.resize(face_image, (48, 48))
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    image_array = img_to_array(grayscale_image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array /= 255.0

    # Predict emotion
    predictions = model.predict(image_array)
    emotion_index = np.argmax(predictions)
    emotion = emotion_labels[emotion_index]

    return emotion