import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Application configuration for EcoVision."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ecovision-smart-waste-2026')
    # Bind to 0.0.0.0 so other devices on Wi-Fi/LAN can access the server
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5005))
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

    # Directory Paths
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'datasets', 'uploads')
    DATASET_DIR = os.path.join(BASE_DIR, 'datasets')
    SAMPLE_DIR = os.path.join(BASE_DIR, 'datasets', 'samples')
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

    # Upload constraints
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload

    # Target categories (6 waste streams + 1 human non-waste safety category)
    CATEGORIES = ['plastic', 'paper', 'glass', 'metal', 'cardboard', 'organic', 'human']
