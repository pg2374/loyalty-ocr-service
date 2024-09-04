import os
import logging
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import cv2
import numpy as np
import imutils
import pytesseract
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)

def show_img(img, title="Image", debug=False):
    """Displays an image using matplotlib."""
    if debug:
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        plt.axis("off")
        plt.title(title)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()

def detect_orientation(image):
    """Detects the orientation of the text and returns the angle to rotate."""
    try:
        osd = pytesseract.image_to_osd(image)
        rotation = int(osd.split("\nRotate: ")[1].split("\n")[0])
        return rotation
    except Exception as e:
        logging.error(f"Error detecting orientation: {e}")
        return 0  # Default to no rotation if detection fails

def correct_orientation(image):
    """Corrects the orientation of the image based on the detected rotation."""
    rotation = detect_orientation(image)
    if rotation != 0:
        # Rotate the image to the correct orientation
        image = imutils.rotate_bound(image, rotation)
    return image

def preprocess_image(image_file, method="default", debug=False):
    """Pre-processes the image to improve text detection."""

    img = cv2.imread(image_file)
    img = correct_orientation(img)  # Correct the orientation first

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    processed_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)

    return processed_img

def extract_text_from_image(image):
    """Extracts text from the pre-processed image using Tesseract."""
    try:
        custom_config = r'--tessdata-dir "./tessdata" --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)  # Assume a single block of text
        return text
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return ""

def preprocess_and_extract_text(image_file, method="default", debug=False):
    """Preprocesses the image and extracts text."""
    processed_img = preprocess_image(image_file, method, debug)
    extracted_text = extract_text_from_image(processed_img)
    return extracted_text

def process_images(image_files, method="default", debug=False):
    """Processes multiple images concurrently and extracts text from each."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda img_file: preprocess_and_extract_text(img_file, method, debug), image_files))
    return results

# Example usage
# image_path = '/path/to/your/image.jpg'
# processed_img = preprocess_image(image_path, debug=True)
# extracted_text = extract_text_from_image(processed_img)
# print("Extracted Text:\n", extracted_text)

# Example for processing multiple images
# image_files = ['/path/to/your/image1.jpg', '/path/to/your/image2.jpg']
# results = process_images(image_files, method="default", debug=True)
# for idx, text in enumerate(results):
#     print(f"Extracted Text from image {idx+1}:\n{text}")
