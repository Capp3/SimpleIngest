import os
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = os.path.join(BASE_DIR, "../.env")
load_dotenv(ENV_FILE)

# Application Metadata
APP_NAME = os.getenv("APP_NAME", "Simple Ingest Tool")
VERSION = os.getenv("VERSION", "1.1.1")

# File and Directory Configuration
LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "log"))
LOG_FILE = os.path.join(LOG_DIR, "simpleingest.log")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Validation Rules
CAMERA_NUMBER_PATTERN = r"\b\d{2}\b"  # Exactly 2 digits
SCENE_NUMBER_PATTERN = r"\b\d{4}\b"   # Exactly 4 digits

# Default Settings
DEFAULT_MEDIA_TYPE = os.getenv("DEFAULT_MEDIA_TYPE", "Video")
DEFAULT_CAPTURE_DATE_FORMAT = os.getenv("DEFAULT_CAPTURE_DATE_FORMAT", "dd/MM/yyyy")

# Supported File Extensions for Each Media Type
VALID_FILE_EXTENSIONS = {
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".m4v", ".wmv", ".flv", ".mpeg", ".raw", ".webm"],
    "Images": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma", ".aiff", ".pcm"],
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Ensure required directories exist
os.makedirs(LOG_DIR, exist_ok=True)

