#!/usr/bin/env bash
# EcoVision Automated Setup and Launch Script

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "♻️  EcoVision: Smart Waste Classification System"
echo "=========================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3."
    exit 1
fi

# Create virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "📦 Creating lightweight Python virtual environment (venv)..."
    python3 -m venv --system-site-packages venv
fi

# Activate virtual environment
source venv/bin/activate

# Install minimal dependencies
echo "📥 Checking dependencies (Flask, Pillow)..."
pip install -q -r requirements.txt

# Start the Flask MVC Application
echo "🚀 Launching EcoVision Application on http://127.0.0.1:5005"
echo "Press Ctrl+C to stop the server."
echo "=========================================================="
python3 app.py

