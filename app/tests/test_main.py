import unittest
from io import BytesIO

import cv2
import numpy as np
from fastapi.testclient import TestClient

from app import app


class MainTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_upload_image(self):
        # Create a blank 2x2 pixel image with 3 color channels (BGR)
        image = np.zeros((2, 2, 3), dtype=np.uint8)

        # Set pixel colors (red and blue)
        image[0, 0] = [0, 0, 255]  # Red pixel at (0, 0)
        image[1, 1] = [255, 0, 0]  # Blue pixel at (1, 1)
        # Convert the image to the RGB format (if needed)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Create a BytesIO object to save the image
        image_bytesio = BytesIO()

        # Use OpenCV's imencode function to encode the image and write it to the BytesIO object
        retval, buffer = cv2.imencode(".png", image_rgb)
        if retval:
            image_bytesio.write(buffer.tobytes())
            image_bytesio.seek(0)  # Reset the BytesIO position to the beginning

        # pass the mock image to the `files` parameter
        response = self.client.post(
            "/upload",
            files={"file": ("mock.png", image_bytesio, "image/png")},
        )

        self.assertEqual(response.status_code, 200)
