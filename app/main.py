import sys
from PyQt5.QtWidgets import QApplication
from app.gui import MediaIngestGUI  # Import the GUI class for the application

# Entry point for the application
if __name__ == "__main__":
    # Create a QApplication instance to manage application-level resources and event handling.
    # This is required for any PyQt-based GUI application.
    app = QApplication(sys.argv)

    # Instantiate the main GUI class.
    # MediaIngestGUI is the primary interface for the application, defined in the app.gui module.
    gui = MediaIngestGUI()

    # Display the GUI to the user by showing the main window.
    gui.show()

    # Start the Qt event loop to handle user interactions, window events, and other GUI operations.
    # The event loop runs until the application is closed, at which point the app.exec_() call exits.
    sys.exit(app.exec_())
