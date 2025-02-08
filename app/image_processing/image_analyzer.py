import cv2

def load_image(image_path):
    """Load an image from the given path."""
    return cv2.imread(image_path)

def detect_faces(image):
    """Detect faces in the image using OpenCV."""
    face_net = cv2.dnn.readNetFromTensorflow(FACE_MODEL, FACE_PROTO)
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)
    face_net.setInput(blob)
    detections = face_net.forward()
    return detections

def extract_face(image, detection):
    """Extract a face region from the image."""
    height, width = image.shape[:2]
    box = detection[3:7] * np.array([width, height, width, height])
    (startX, startY, endX, endY) = box.astype("int")
    face = image[startY:endY, startX:endX]
    return face