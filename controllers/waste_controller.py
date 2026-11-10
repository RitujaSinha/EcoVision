"""
Waste Controller (C in MVC)
Coordinates between the View layer (HTTP requests/UI) and the Model layer (WasteClassifier & WasteDataModel).
Handles payload extraction, image validation, classification dispatch, and JSON responses.
"""

import os
import re
import base64
import time
from io import BytesIO
from flask import Blueprint, request, jsonify, render_template, send_from_directory, current_app
from werkzeug.utils import secure_filename
from PIL import Image

from models.classifier_model import WasteClassifier
from models.waste_data_model import WasteLogManager, WASTE_CATEGORIES
from models.mobilenet_model import EcoVisionMobileNetV2
from datasets.dataset_loader import get_available_samples, ensure_sample_images

# Define Flask Blueprint for MVC routing
waste_blueprint = Blueprint('waste_controller', __name__)
classifier = WasteClassifier()


def is_allowed_file(filename):
    """Check allowed image extension."""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp', 'bmp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


@waste_blueprint.route('/')
def index():
    """Renders the main EcoVision web view."""
    stats = WasteLogManager.get_stats()
    return render_template('index.html', categories=WASTE_CATEGORIES, stats=stats)


@waste_blueprint.route('/api/classify', methods=['POST'])
def classify():
    """
    Main classification endpoint.
    Accepts:
    1. Multi-part form file upload ('file' or 'image')
    2. Base64 encoded snapshot ('image_base64' in JSON)
    3. Sample selection ('sample_path' in JSON)
    """
    try:
        image_obj = None
        filename = f"capture_{int(time.time())}.jpg"
        source = "upload"

        # Case 1: JSON payload (Webcam base64 or sample path)
        if request.is_json:
            data = request.get_json()
            if 'image_base64' in data and data['image_base64']:
                b64_str = data['image_base64']
                # Strip data URL header if present (e.g., 'data:image/jpeg;base64,...')
                if ',' in b64_str:
                    b64_str = b64_str.split(',', 1)[1]
                image_data = base64.b64decode(b64_str)
                image_obj = Image.open(BytesIO(image_data))
                source = "webcam"
                filename = f"webcam_{int(time.time())}.jpg"

            elif 'sample_path' in data and data['sample_path']:
                # Sample image selected from datasets/samples
                sample_rel = data['sample_path'].strip('/')
                full_sample_path = os.path.join(current_app.config['SAMPLE_DIR'], sample_rel)
                if not os.path.exists(full_sample_path):
                    return jsonify({"error": f"Sample image not found: {sample_rel}"}), 404
                image_obj = Image.open(full_sample_path)
                filename = os.path.basename(full_sample_path)
                source = "sample"

        # Case 2: Multi-part file upload
        if image_obj is None and ('image' in request.files or 'file' in request.files):
            file = request.files.get('image') or request.files.get('file')
            if file and file.filename != '':
                if not is_allowed_file(file.filename):
                    return jsonify({"error": "Unsupported file format. Please upload JPG, PNG, WEBP, or BMP."}), 400
                filename = secure_filename(file.filename)
                image_obj = Image.open(file.stream)
                source = "upload"

        if image_obj is None:
            return jsonify({"error": "No valid image provided. Please upload a file or take a snapshot."}), 400

        # Save an uploaded record copy in datasets/uploads
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if upload_folder:
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, filename)
            try:
                image_obj.save(save_path)
            except Exception:
                pass

        # Execute classification through Model
        result = classifier.predict(image_obj, filename_hint=filename)

        # Record into history log
        record = WasteLogManager.record(
            category_id=result["category"],
            confidence=result["confidence"] / 100.0,
            filename=filename,
            source=source
        )

        return jsonify({
            "status": "success",
            "data": result,
            "log": record,
            "stats": WasteLogManager.get_stats()
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@waste_blueprint.route('/api/history', methods=['GET'])
def get_history():
    """Returns recent classification events and statistics."""
    return jsonify({
        "status": "success",
        "history": WasteLogManager.get_history(limit=25),
        "stats": WasteLogManager.get_stats()
    })


@waste_blueprint.route('/api/samples', methods=['GET'])
def list_samples():
    """Lists available preloaded sample images from the datasets folder."""
    samples = get_available_samples(current_app.config['SAMPLE_DIR'])
    return jsonify({"status": "success", "samples": samples})


@waste_blueprint.route('/api/model-info', methods=['GET'])
def model_info():
    """Returns CNN architecture parameters and configuration."""
    return jsonify({
        "status": "success",
        "architecture": "MobileNetV2 Inverted Residual Bottleneck",
        "parameters": EcoVisionMobileNetV2.total_trainable_parameters(),
        "classes": EcoVisionMobileNetV2.CLASSES,
        "layers": EcoVisionMobileNetV2.get_architecture_summary(),
        "hyperparameters": EcoVisionMobileNetV2.get_training_hyperparameters()
    })


@waste_blueprint.route('/datasets/samples/<path:filename>')
def serve_sample(filename):
    """Serve sample dataset images."""
    return send_from_directory(current_app.config['SAMPLE_DIR'], filename)

