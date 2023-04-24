from fastapi.testclient import TestClient
from io import BytesIO
import unittest
from app.main import app

class MainTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
    
    def test_upload_image(self):
        # create a mock image
        mock_image = BytesIO()
        mock_image.write(b"mock image data")
        mock_image.seek(0)
        
        # pass the mock image to the `files` parameter
        response = self.client.post("/upload", files={"file": ("mock.png", mock_image, "image/png")})
        
        self.assertEqual(response.status_code, 200)
