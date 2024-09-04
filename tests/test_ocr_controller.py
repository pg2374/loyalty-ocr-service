import unittest
from io import BytesIO
from main import app


class TestOCRController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_ocr_endpoint(self):
        # Prepare a dummy image for testing
        with open('images/receipt1.jpg', 'rb') as image_file:
            image_data = image_file.read()

        response = self.app.post('/ocr', data={
            'image': (BytesIO(image_data), 'test_image.jpg')
        })

        # Test if the response is JSON and has the correct structure
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json)
        self.assertIn('extracted_info', response.json)

    def tearDown(self):
        # Clean up any state here if necessary
        pass


if __name__ == '__main__':
    unittest.main()
