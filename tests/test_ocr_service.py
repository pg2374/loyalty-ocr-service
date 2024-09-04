import unittest
from app.ocr import preprocess_image, extract_text_from_image, preprocess_and_extract_text


class TestOCRService(unittest.TestCase):

    def setUp(self):
        # Set up any necessary files or state here
        self.test_image_path = 'images/receipt1.jpg'
        self.test_processed_image = preprocess_image(self.test_image_path)

    def test_preprocess_image(self):
        # Test if the image preprocessing works correctly
        processed_image = preprocess_image(self.test_image_path)
        self.assertIsNotNone(processed_image)
        self.assertEqual(processed_image.shape,
                         (processed_image.shape[0], processed_image.shape[1]))

    def test_extract_text_from_image(self):
        # Test if text extraction works on a known image
        text = extract_text_from_image(self.test_processed_image)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_preprocess_and_extract_text(self):
        # Test the end-to-end process
        extracted_text = preprocess_and_extract_text(self.test_image_path)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)

    def tearDown(self):
        # Clean up any files or state here if necessary
        pass


if __name__ == '__main__':
    unittest.main()
