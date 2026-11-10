# EcoVision
EcoVision is a deep learning-based waste classification and recycling assistant that identifies waste types from images and provides appropriate disposal and recycling recommendations. It aims to promote efficient waste segregation, reduce recycling contamination, and support sustainable waste management.

The project follows the Model--View--Controller (MVC) architecture,
keeping classification logic, request handling, and the user interface
organized into separate layers.

🌱 Waste Categories
  Category       Suggested Bin
🧴 Plastic     Blue
📄 Paper       Yellow
🍾 Glass       Teal
🥫 Metal       Silver
📦 Cardboard   Brown
🍎 Organic     Green

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

🛠️ Technology Stack

- Backend: Python, Flask
- Machine Learning: PyTorch, Torchvision
- Image Processing: Pillow
- Frontend: HTML, CSS, JavaScript
- Production Server: Gunicorn
- Deployment: Render, Docker

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

4. Open the application

Visit:
http://127.0.0.1:5005

Press Ctrl + C in the terminal to stop the local server.
For Windows, create and activate the environment with
python -m venv venv and .\venv\Scripts\Activate.ps1.

☁️ Deployment
Render

The repository includes a render.yaml configuration for deploying
EcoVision on Render.

1. Push the project to GitHub.
2. Connect the repository to Render.
3. Create a Blueprint deployment.
4. Review the service settings and deploy.
The supplied configuration uses Python 3.10.12 and Gunicorn to run the
Flask application.

Docker

A Dockerfile is included for containerized deployment.
docker build -t ecovision .
docker run --rm -p 7860:7860 ecovision
Open http://127.0.0.1:7860 in your browser.
⚙️ Configuration
Application settings are managed in config.py.

Setting               Default
Host                  0.0.0.0
Port                  5005
Debug mode            True
Maximum upload size   16 MB

For production deployment, set a secure SECRET_KEY and disable debug
mode using environment variables.

by Manish