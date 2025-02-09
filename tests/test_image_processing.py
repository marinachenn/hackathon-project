import unittest
from app.image_processing.image_analyzer import analyze_image

class TestImageProcessing(unittest.TestCase):
    def test_analyze_image(self):
        image_path = "data/images/IMG_0339.JPEG" 
        face_image = analyze_image(image_path)
        self.assertIsNotNone(face_image)

if __name__ == "__main__":
    unittest.main()