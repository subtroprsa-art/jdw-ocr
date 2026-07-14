from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
import base64
from PIL import Image
import io
import os
import subprocess

app = Flask(__name__)
CORS(app)

# Tell pytesseract where tesseract is installed
# On Render, it's usually in /usr/bin/tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.route('/')
def home():
    return 'OCR Service Running'

@app.route('/health', methods=['GET'])
def health():
    # Check if tesseract is available
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        version = result.stdout.split('\n')[0] if result.stdout else 'unknown'
        return jsonify({'status': 'ok', 'ocr': 'tesseract', 'version': version})
    except Exception as e:
        return jsonify({'status': 'error', 'ocr': 'tesseract', 'error': str(e)}), 500

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        data = request.json
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run Tesseract OCR
        text = pytesseract.image_to_string(image)
        
        return jsonify({'text': text})
    
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
