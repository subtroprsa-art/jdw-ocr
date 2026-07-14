#!/bin/bash

echo "📦 Installing system dependencies..."

# Try different methods to install tesseract
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu based (Render uses this)
    apt-get update --allow-releaseinfo-change || true
    apt-get install -y tesseract-ocr || echo "apt-get failed, trying alternative..."
fi

# Alternative: try using apt (sometimes works when apt-get doesn't)
if ! command -v tesseract &> /dev/null; then
    if command -v apt &> /dev/null; then
        apt update || true
        apt install -y tesseract-ocr || echo "apt failed"
    fi
fi

# Check if tesseract is installed
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract installed: $(tesseract --version | head -1)"
else
    echo "⚠️ Tesseract not found. Will try to use Python's pytesseract without system tesseract."
    # Try to install via pip
    pip3 install pytesseract
fi

echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "✅ Build complete"
