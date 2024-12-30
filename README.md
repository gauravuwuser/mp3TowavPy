# mp3TowavPy

<!-- `mp3TowavPy` is a Python-based application for converting MP3 files to WAV format. It utilizes libraries such as `pydub`, `librosa`, `numpy`, and `flask` for efficient audio processing. -->

## Installation Process

Follow the steps below to set up the project environment:

### 1. Set up a Virtual Environment
First, create a virtual environment to isolate dependencies:

```bash
python -m venv venv


### For Linux/Mac:
source venv/bin/activate

### For Windows:
venv\Scripts\activate


# 2. Install Required Dependencies
# With the virtual environment activated, install the necessary Python packages:

pip install pydub librosa numpy flask gunicorn


# 3. Install FFmpeg
# pydub requires FFmpeg for audio format conversions. Follow the instructions to download and install FFmpeg:

# FFmpeg Installation Guide
# After installation, ensure that the ffmpeg binary is in your system’s PATH by updating the environment variables:

# Linux/Mac: Add FFmpeg’s location to the PATH by modifying the .bashrc or .zshrc file.
# Windows: Add FFmpeg’s bin directory to the PATH environment variable.


# 4. Run the Application
# Once everything is set up, start the Flask application by running:

python app.py