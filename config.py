import os

# Application Metadata
APP_NAME = "Simple Ingest Tool"
VERSION = "1.0.0"

# File and Directory Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "log")
LOG_FILE = os.path.join(LOG_DIR, "simpleingest.log")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Validation Rules
CAMERA_NUMBER_PATTERN = r"\d{2}"  # Exactly 2 digits
SCENE_NUMBER_PATTERN = r"\d{4}"   # Exactly 4 digits

# Default Settings
DEFAULT_MEDIA_TYPE = "Video"
DEFAULT_CAPTURE_DATE_FORMAT = "dd/MM/yyyy"

# Supported File Extensions for Each Media Type
VALID_FILE_EXTENSIONS = {
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".m4v", ".wmv", ".flv", ".mpeg", ".raw", ".webm"],
    "Images": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma", ".aiff", ".pcm"],
}

# Logging Configuration
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

LOGGING = {
    "level": "DEBUG",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "log_file": "simpleingest.log",  # Set to None for console output only
}

# Ensure required directories exist
os.makedirs(LOG_DIR, exist_ok=True)
