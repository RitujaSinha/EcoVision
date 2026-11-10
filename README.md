


# EcoVision
EcoVision is a deep learning-based waste classification and recycling assistant that identifies waste types from images and provides appropriate disposal and recycling recommendations. It aims to promote efficient waste segregation, reduce recycling contamination, and support sustainable waste management.

The project follows the Model--View--Controller (MVC) architecture,
keeping classification logic, request handling, and the user interface
organized into separate layers.

<p align="center">
  <img src="assets/front.png" width="100%" alt="EcoVision Banner">
</p>

<h1 align="center">♻️ EcoVision</h1>

<p align="center">
   Smart Waste Classification System
</p>

🌱 Waste Categories
 ## ♻️ Waste Categories

<p align="center">
  <img src="assets/categories.png" width="90%" alt="Waste Categories">
</p>

The application configuration also includes a human category as a
non-waste safety category.

✨ Key Features


- Image Classification: Submit waste images for classification.
- Webcam Capture: Capture an item using your device camera.
- Drag-and-Drop Upload: Upload supported image formats.
- Sample Images: Try the application with sample category images.
- Smart Bin Suggestions: Get a suggested waste-disposal category.
- Confidence Scores: View the class probability distribution.
- Environmental Metrics: View estimated carbon-savings and
  decomposition information.
- Scan History: Review previously scanned items.


## ✨ Key Features

<p align="center">
  <img src="assets/features.png" width="90%" alt="EcoVision Features">
</p>


🛠️ Technology Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-black)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red)
![Computer Vision](https://img.shields.io/badge/Computer-Vision-green)
![ai/ml](https://img.shields.io/badge/License-MIT-yellow)

🏗️ Project Architecture

EcoVision/
│
├── app.py                  # Flask application entry point
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── run.sh                  # Automated setup and launch
├── Procfile                # Deployment process
├── Dockerfile              # Docker configuration
├── render.yaml             # Render deployment settings
│
├── models/                 # Model and classification logic
├── controllers/            # Request handling
├── frontend/               # HTML, CSS and JavaScript
└── datasets/               # Samples and uploaded images

MVC Workflow

User
  |
  v
Frontend (View)
  |
  v
Controller
  |
  v
Model / Classifier
  |
  v
Classification Result
  |
  v
Frontend (View)

🚀 Getting Started

Prerequisites
- Python 3.10 or newer
- pip
- Git

1. Clone the repository

git clone <YOUR_REPOSITORY_URL>
cd EcoVision

2. Run the setup script (recommended)
On macOS or Linux:
chmod +x run.sh
./run.sh
The script creates a virtual environment if required, installs
dependencies from requirements.txt, and starts the application.

3. Manual installation
If you prefer to install dependencies yourself:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py





by Manish