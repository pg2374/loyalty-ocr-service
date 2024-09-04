from flask import Flask, request, jsonify
from app.ocr import preprocess_image, extract_text_from_image
from app.utils.text_processing_utils import extract_all_info

app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    # Get the image from the request
    image = request.files['image']

    # Save the image to a temporary location
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)

    # Pre-process the image and extract text using OCR
    processed_img = preprocess_image(image_path)
    extracted_text = extract_text_from_image(processed_img)

    # Extract relevant information from the text
    extracted_info = extract_all_info(extracted_text)

    # Return the extracted information as a JSON response
    return jsonify({
        "text": extracted_text,
        "extracted_info": extracted_info
    })


if __name__ == '__main__':
    app.run(debug=True)
