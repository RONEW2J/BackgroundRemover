# Background Remover

A powerful application for removing image backgrounds, available as both desktop and web application.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation

# 📥 How download

Download [BackgroundRemover.exe] - \dist,
model [u2net.onnx] - \models and
pkg [BackgroundRemover.pkg] - \build\BackgroundRemover

(https://drive.google.com/drive/folders/1LZJjiwUEWXJwkTj1Wup12AlvImWFUxyR?usp=sharing)

### 1. Set up Python Environment

First, ensure Python 3.11+ is installed:

```bash
python --version
```

### 2. Get the Project

Either clone the repository or download the ZIP:

```bash
git clone https://github.com/RONEW2J/BackgroundRemover
cd background-remover
```

### 3. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# For Windows CMD:
.venv\Scripts\activate.bat
# For Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Desktop Version

1. Activate virtual environment (if not already activated)
2. Run the desktop application:

```bash
python app.py
```

### Web Version

1. Activate virtual environment (if not already activated)
2. Start the Flask server:

```bash
python server.py
```

3. Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage Instructions

### Desktop Application

1. Launch the application using `python app.py`
2. Click "Choose File" or drag and drop an image
3. Wait for the model to load (first launch only)
4. Click "Remove Background" to process the image
5. Use "Save" to download the processed image
6. Click "Reset" to process another image

### Web Interface

1. Start server using `python server.py`
2. Open `http://localhost:5000` in your browser
3. Either:
   - Click "Choose File" button
   - Drag and drop an image onto the upload area
4. Wait for automatic processing
5. Click "Download" to save the result
6. Use "Upload New Image" to process another image

## Troubleshooting

### Common Issues

1. **Model Loading Error**

   ```bash
   # Try reinstalling rembg
   pip uninstall rembg
   pip install rembg --no-cache-dir
   ```

2. **Port Already in Use**

   ```bash
   # Try different port
   # Edit server.py and change port number:
   app.run(debug=True, port=5001)
   ```

3. **Memory Issues**
   - Close other applications
   - Process smaller images
   - Restart the application

### Requirements

```txt
rembg==2.0.50
Pillow==10.0.0
flask==2.3.3
torch==2.0.1
onnxruntime==1.15.1
numpy==1.24.3
```

## Project Structure

```
background-remover/
├── app.py              # Desktop application
├── server.py           # Web server
├── requirements.txt    # Dependencies
├── README.md          # Documentation
└── public/            # Web assets
    ├── index.html     # Web interface
    ├── css/           # Stylesheets
    └── js/            # JavaScript files
```

## Support

For issues and questions:

1. Check the troubleshooting section
2. Submit an issue on GitHub
3. Contact: ronew2j@email.com

## License

This project is licensed under the MIT License.
