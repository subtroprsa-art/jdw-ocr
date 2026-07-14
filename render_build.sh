#!/bin/bash

echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Pre-download EasyOCR model (speeds up first request)
echo "📦 Pre-downloading EasyOCR model..."
python3 -c "import easyocr; reader = easyocr.Reader(['en'], gpu=False)" || echo "⚠️ Model download will happen on first request"

echo "✅ Build complete"
