import sys
import logging
from PyQt5.QtWidgets import QApplication
from app.main import MediaIngestGUI  # Import the main GUI class for the application
from app.config import (
    LOG_FILE, LOG_LEVEL  # Import logging configurations
)

# Configure logging
def configure_logging():
    """
    Sets up logging configuration for the application.
    Logs messages to both a file and the console.
    """
    logging.basicConfig(
        level=LOG_LEVEL,  # Set the logging level (e.g., DEBUG, INFO, ERROR)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Define log message format
        handlers=[
            logging.FileHandler(LOG_FILE),           # Handler to write logs to a file
            logging.StreamHandler(sys.stdout),       # Handler to output logs to the console
        ]
    )

# Exception hook to catch uncaught exceptions
def exception_hook(exc_type, exc_value, traceback):
    """
    Handles uncaught exceptions by logging them as critical errors.
    Ensures all unhandled exceptions are logged for debugging purposes.
    """
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, traceback))
    sys.__excepthook__(exc_type, exc_value, traceback)

if __name__ == "__main__":
    # Configure logging for the application
    configure_logging()

    # Set the custom exception hook to catch and log any uncaught exceptions
    sys.excepthook = exception_hook

    # Log the application startup
    logging.info("Starting Media Ingest application.")

    # Initialise the PyQt application
    app = QApplication(sys.argv)  # Create the main application object
    gui = MediaIngestGUI()  # Create an instance of the Media Ingest GUI
    gui.show()  # Display the GUI window

    try:
        # Run the application event loop
        exit_code = app.exec_()
        logging.info("Application exited cleanly.")  # Log clean exit
    except Exception as e:
        # Log any unhandled exceptions that occur during application execution
        logging.critical(f"Unhandled exception during app execution: {e}", exc_info=True)
        exit_code = 1  # Set exit code to indicate an error occurred

    # Exit the application with the appropriate exit code
    sys.exit(exit_code)
