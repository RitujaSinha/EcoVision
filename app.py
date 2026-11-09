"""
EcoVision Web Application Entrypoint
Wires Model, View, and Controller components together and initializes the HTTP server.
"""

import os
from flask import Flask
from config import Config
from controllers.waste_controller import waste_blueprint
from datasets.dataset_loader import ensure_sample_images

def create_app():
    """Application factory for EcoVision."""
    app = Flask(
        __name__,
        template_folder=Config.TEMPLATES_DIR,
        static_folder=Config.STATIC_DIR,
        static_url_path='/static'
    )
    app.config.from_object(Config)

    # Ensure required runtime folders exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.SAMPLE_DIR, exist_ok=True)

    # Pre-generate sample test images in datasets/samples if empty
    ensure_sample_images(Config.SAMPLE_DIR)

    # Register MVC controller blueprint
    app.register_blueprint(waste_blueprint)

    return app

# Expose app for WSGI servers (Gunicorn, uWSGI, Render, Railway, HuggingFace)
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("♻️  EcoVision: Smart Waste Classification System")
    print("🚀  MVC Architecture Active")
    print(f"🌐  Access Server at: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

