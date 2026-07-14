from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from PIL import Image
import io
import os
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Try to find tesseract
tesseract_paths = [
    '/usr/bin/tesseract',
    '/usr/local/bin/tesseract',
    '/opt/render/project/.local/bin/tesseract',
    'tesseract'
]

tesseract_found = None
for path in tesseract_paths:
    try:
        result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            tesseract_found = path
            break
    except:
        continue

if tesseract_found:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = tesseract_found
    print(f"✅ Tesseract found at: {tesseract_found}")
else:
    print("❌ Tesseract not found. OCR will not work.")
    pytesseract = None

@app.route('/')
def home():
    return 'OCR Service Running'

@app.route('/health', methods=['GET'])
def health():
    if tesseract_found:
        return jsonify({'status': 'ok', 'ocr': 'tesseract', 'path': tesseract_found})
    else:
        return jsonify({'status': 'error', 'ocr': 'tesseract', 'error': 'Tesseract not found'}), 500

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if pytesseract is None:
        return jsonify({'error': 'Tesseract not available'}), 500
    
    try:
        data = request.json
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        text = pytesseract.image_to_string(image)
        
        return jsonify({'text': text})
    
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
