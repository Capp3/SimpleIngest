from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QProgressBar, QWidget, QFileDialog, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
import logging
import os
import json
from logic import process_batch
from config import (
    SETTINGS_FILE, LOG_FILE, VALID_FILE_EXTENSIONS,
    CAMERA_NUMBER_PATTERN, SCENE_NUMBER_PATTERN,
    DEFAULT_MEDIA_TYPE, DEFAULT_CAPTURE_DATE_FORMAT,
    APP_NAME, VERSION
)
import re

class MediaIngestGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_logging()
        self.init_ui()

        # Variables to store input data
        self.project_name = ""
        self.import_path = ""
        self.export_path = ""
        self.media_type = DEFAULT_MEDIA_TYPE
        self.capture_date = None
        self.camera_number = ""
        self.scene_number = ""

        # Load previous settings
        self.load_settings()

    def init_logging(self):
        """Initialise logging."""
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="gui - %(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info(f"Starting {APP_NAME} v{VERSION}")

    def init_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 600, 400)

        # Main layout for the interface
        main_layout = QVBoxLayout()

        # Project Name Entry
        project_layout = QHBoxLayout()
        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        self.project_name_input.setMaxLength(16)
        self.project_name_input.setPlaceholderText("Project Name")
        project_layout.addWidget(self.project_name_label)
        project_layout.addWidget(self.project_name_input)
        main_layout.addLayout(project_layout)

        # Import Path
        import_layout = QHBoxLayout()
        self.import_label = QLabel("Import Path:")
        self.import_path_input = QLineEdit()
        self.import_browse_button = QPushButton("Browse")
        self.import_browse_button.clicked.connect(self.browse_import_path)
        import_layout.addWidget(self.import_label)
        import_layout.addWidget(self.import_path_input)
        import_layout.addWidget(self.import_browse_button)
        main_layout.addLayout(import_layout)

        # Export Path
        export_layout = QHBoxLayout()
        self.export_label = QLabel("Export Path:")
        self.export_path_input = QLineEdit()
        self.export_browse_button = QPushButton("Browse")
        self.export_browse_button.clicked.connect(self.browse_export_path)
        export_layout.addWidget(self.export_label)
        export_layout.addWidget(self.export_path_input)
        export_layout.addWidget(self.export_browse_button)
        main_layout.addLayout(export_layout)

        # Media Type and Capture Date
        row_layout = QHBoxLayout()
        self.media_type_label = QLabel("Media Type:")
        self.media_type_dropdown = QComboBox()
        self.media_type_dropdown.addItems(list(VALID_FILE_EXTENSIONS.keys()))
        self.capture_date_label = QLabel("Capture Date:")
        self.capture_date_selector = QDateEdit()
        self.capture_date_selector.setDisplayFormat(DEFAULT_CAPTURE_DATE_FORMAT)
        self.capture_date_selector.setDate(QDate.currentDate())
        row_layout.addWidget(self.media_type_label)
        row_layout.addWidget(self.media_type_dropdown)
        row_layout.addWidget(self.capture_date_label)
        row_layout.addWidget(self.capture_date_selector)
        main_layout.addLayout(row_layout)

        # Camera Number and Scene Number
        line_layout = QHBoxLayout()
        self.camera_number_label = QLabel("Camera Number:")
        self.camera_number_input = QLineEdit()
        self.scene_number_label = QLabel("Scene Number:")
        self.scene_number_input = QLineEdit()
        line_layout.addWidget(self.camera_number_label)
        line_layout.addWidget(self.camera_number_input)
        line_layout.addWidget(self.scene_number_label)
        line_layout.addWidget(self.scene_number_input)
        main_layout.addLayout(line_layout)

        # Activate Button
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.start_batch_process)
        main_layout.addWidget(self.activate_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Finalise layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def browse_import_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Import Directory")
        if path:
            self.import_path_input.setText(path)

    def browse_export_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if path:
            self.export_path_input.setText(path)

    def start_batch_process(self):
        if not self.validate_fields():
            return

        # Fetch values from the GUI
        self.project_name = self.project_name_input.text().replace(" ", "_")
        self.import_path = self.import_path_input.text()
        self.export_path = self.export_path_input.text()
        self.media_type = self.media_type_dropdown.currentText()
        self.capture_date = self.capture_date_selector.date().toString(DEFAULT_CAPTURE_DATE_FORMAT)
        self.camera_number = self.camera_number_input.text()
        self.scene_number = self.scene_number_input.text()

        try:
            process_batch(
                self.import_path, self.export_path,
                self.project_name, self.media_type,
                self.capture_date, self.camera_number,
                self.scene_number
            )
            QMessageBox.information(self, "Success", "Batch process completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Batch process failed: {e}")

    def validate_fields(self):
        if not self.project_name_input.text():
            self.show_error_message("Project Name is required.")
            return False
        if not self.import_path_input.text():
            self.show_error_message("Import Path is required.")
            return False
        if not self.export_path_input.text():
            self.show_error_message("Export Path is required.")
            return False
        if not re.fullmatch(CAMERA_NUMBER_PATTERN, self.camera_number_input.text()):
            self.show_error_message("Camera Number must be exactly 2 digits.")
            return False
        if not re.fullmatch(SCENE_NUMBER_PATTERN, self.scene_number_input.text()):
            self.show_error_message("Scene Number must be exactly 4 digits.")
            return False
        return True

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Validation Error")
        error_dialog.setText(message)
        error_dialog.exec_()
        logging.warning(f"Validation failed: {message}")

    def save_settings(self):
        settings = {
            "project_name": self.project_name,
            "import_path": self.import_path,
            "export_path": self.export_path,
            "media_type": self.media_type,
            "capture_date": self.capture_date,
            "camera_number": self.camera_number,
            "scene_number": self.scene_number,
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                self.project_name_input.setText(settings.get("project_name", "").replace("_", " "))
                self.import_path_input.setText(settings.get("import_path", ""))
                self.export_path_input.setText(settings.get("export_path", ""))
                self.media_type_dropdown.setCurrentText(settings.get("media_type", DEFAULT_MEDIA_TYPE))
                self.capture_date_selector.setDate(
                    QDate.fromString(settings.get("capture_date", ""), DEFAULT_CAPTURE_DATE_FORMAT)
                )
                self.camera_number_input.setText(settings.get("camera_number", ""))
                self.scene_number_input.setText(settings.get("scene_number", ""))

# Run the application
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    gui = MediaIngestGUI()
    gui.show()
    sys.exit(app.exec_())
