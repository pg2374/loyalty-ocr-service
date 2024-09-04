# import os
# from google.cloud import vision
# from google.cloud.vision import types

# def detect_text_google_vision(image_path):
#     """Detects text in an image using Google Vision API."""
#     client = vision.ImageAnnotatorClient()

#     with open(image_path, 'rb') as image_file:
#         content = image_file.read()
    
#     image = types.Image(content=content)
#     response = client.text_detection(image=image)
    
#     texts = response.text_annotations
#     if not texts:
#         return "", []

#     extracted_text = texts[0].description
#     return extracted_text, texts

# def preprocess_and_detect_google_vision(image_file, debug=False):
#     """Preprocesses the image and then detects text using Google Vision OCR."""
#     # Here you can add any preprocessing if needed
#     extracted_text, annotations = detect_text_google_vision(image_file)
#     return extracted_text, annotations
