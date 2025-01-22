import sys
import logging
from PyQt5.QtWidgets import QApplication
from app.main import MediaIngestGUI
from config import (
    LOG_FILE, LOG_LEVEL
)

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=LOG_LEVEL,  # Default level can be adjusted to DEBUG or ERROR
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),           # Logs to a file
            logging.StreamHandler(sys.stdout),       # Logs to console
        ]
    )

# Exception hook to catch uncaught exceptions
def exception_hook(exc_type, exc_value, traceback):
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, traceback))
    sys.__excepthook__(exc_type, exc_value, traceback)

if __name__ == "__main__":
    # Configure logging
    configure_logging()

    # Set the exception hook
    sys.excepthook = exception_hook

    logging.info("Starting Media Ingest application.")

    # Start the application
    app = QApplication(sys.argv)
    gui = MediaIngestGUI()
    gui.show()

    try:
        exit_code = app.exec_()
        logging.info("Application exited cleanly.")
    except Exception as e:
        logging.critical(f"Unhandled exception during app execution: {e}", exc_info=True)
        exit_code = 1

    sys.exit(exit_code)
