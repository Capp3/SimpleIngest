from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QPlainTextEdit,
    QProgressBar, QWidget, QFileDialog, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
import logging
import os
import json
import re
from app.config import (
    SETTINGS_FILE, LOG_FILE, VALID_FILE_EXTENSIONS,
    DEFAULT_MEDIA_TYPE, DEFAULT_CAPTURE_DATE_FORMAT,
    APP_NAME, VERSION, CAMERA_NUMBER_PATTERN, SCENE_NUMBER_PATTERN
)
from app.threads import BatchProcessThread
from app.consolehandler import LogHandler


class MediaIngestGUI(QMainWindow):
    def __init__(self):
        # Initialises the Media Ingest GUI and loads settings
        super().__init__()
        self.init_logging()
        self.init_ui()

        # Initialise variables to store user input
        self.project_name = ""
        self.import_path = ""
        self.export_path = ""
        self.media_type = DEFAULT_MEDIA_TYPE
        self.capture_date = None
        self.camera_number = ""
        self.scene_number = ""

        # Load settings from previous session, if available
        self.load_settings()

    def init_logging(self):
        # Sets up logging for file and GUI console output.
        # Create a text box for displaying logs within the GUI
        self.log_console = QPlainTextEdit()
        self.log_console.setReadOnly(True)

        # Create file and GUI log handlers
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        gui_handler = LogHandler(self.log_console)  # Custom handler for GUI logging
        gui_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # Configure the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)  # Log level can be adjusted
        root_logger.addHandler(file_handler)
        root_logger.addHandler(gui_handler)

        # Log application startup
        logging.info(f"Starting {APP_NAME} v{VERSION}")

    def init_ui(self):
        # Initialises the GUI layout and components.
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 600, 500)

        # Main layout for all components
        main_layout = QVBoxLayout()

        # Project Name input
        project_layout = QHBoxLayout()
        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name here")
        project_layout.addWidget(self.project_name_label)
        project_layout.addWidget(self.project_name_input)
        main_layout.addLayout(project_layout)

        # Import Path selection
        import_layout = QHBoxLayout()
        self.import_label = QLabel("Import Path:")
        self.import_path_input = QLineEdit()
        self.import_browse_button = QPushButton("Browse")
        self.import_browse_button.clicked.connect(self.browse_import_path)
        import_layout.addWidget(self.import_label)
        import_layout.addWidget(self.import_path_input)
        import_layout.addWidget(self.import_browse_button)
        main_layout.addLayout(import_layout)

        # Export Path selection
        export_layout = QHBoxLayout()
        self.export_label = QLabel("Export Path:")
        self.export_path_input = QLineEdit()
        self.export_browse_button = QPushButton("Browse")
        self.export_browse_button.clicked.connect(self.browse_export_path)
        export_layout.addWidget(self.export_label)
        export_layout.addWidget(self.export_path_input)
        export_layout.addWidget(self.export_browse_button)
        main_layout.addLayout(export_layout)

        # Media Type and Capture Date selection
        type_date_layout = QHBoxLayout()
        self.media_type_label = QLabel("Media Type:")
        self.media_type_dropdown = QComboBox()
        self.media_type_dropdown.addItems(list(VALID_FILE_EXTENSIONS.keys()))
        self.capture_date_label = QLabel("Capture Date:")
        self.capture_date_selector = QDateEdit()
        self.capture_date_selector.setDisplayFormat(DEFAULT_CAPTURE_DATE_FORMAT)
        self.capture_date_selector.setDate(QDate.currentDate())
        type_date_layout.addWidget(self.media_type_label)
        type_date_layout.addWidget(self.media_type_dropdown)
        type_date_layout.addWidget(self.capture_date_label)
        type_date_layout.addWidget(self.capture_date_selector)
        main_layout.addLayout(type_date_layout)

        # Camera Number and Scene Number inputs
        camera_scene_layout = QHBoxLayout()
        self.camera_number_label = QLabel("Camera Number:")
        self.camera_number_input = QLineEdit()
        self.camera_number_input.setPlaceholderText("01")
        self.camera_number_input.editingFinished.connect(self.format_camera_number)

        self.scene_number_label = QLabel("Scene Number:")
        self.scene_number_input = QLineEdit()
        self.scene_number_input.setPlaceholderText("1234")
        self.scene_number_input.editingFinished.connect(self.format_scene_number)

        camera_scene_layout.addWidget(self.camera_number_label)
        camera_scene_layout.addWidget(self.camera_number_input)
        camera_scene_layout.addWidget(self.scene_number_label)
        camera_scene_layout.addWidget(self.scene_number_input)
        main_layout.addLayout(camera_scene_layout)

        # Activate button and progress bar
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.start_batch_process)
        main_layout.addWidget(self.activate_button)
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Console Window
        main_layout.addWidget(self.log_console)

        # Finalise layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def browse_import_path(self):
        # Opens a dialog to select the import directory.
        path = QFileDialog.getExistingDirectory(self, "Select Import Directory")
        if path:
            self.import_path_input.setText(path)

    def browse_export_path(self):
        # Opens a dialog to select the export directory.
        path = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if path:
            self.export_path_input.setText(path)

    def format_camera_number(self):
        # Ensures the camera number matches the required pattern.
        text = self.camera_number_input.text()
        required_length = len(re.findall(r"\d", CAMERA_NUMBER_PATTERN)[0])

        if len(text) > required_length:
            # self.camera_number_input.setStyleSheet("border: 2px solid red;")
            self.camera_number_input.setStyleSheet("")
        elif len(text) < required_length:
            self.camera_number_input.setText(text.zfill(required_length))
            self.camera_number_input.setStyleSheet("")
        else:
            self.camera_number_input.setStyleSheet("")

    def format_scene_number(self):
        # Ensures the scene number matches the required pattern.
        text = self.scene_number_input.text()
        required_length = len(re.findall(r"\d", SCENE_NUMBER_PATTERN)[0])

        if len(text) > required_length:
            # self.scene_number_input.setStyleSheet("border: 2px solid red;")
            self.scene_number_input.setStyleSheet("")
        elif len(text) < required_length:
            self.scene_number_input.setText(text.zfill(required_length))
            self.scene_number_input.setStyleSheet("")
        else:
            self.scene_number_input.setStyleSheet("")

    def start_batch_process(self):
        # Validates input and starts the batch process.
        logging.info("Activate button pressed.")
        try:
            if not self.project_name_input.text() or not self.import_path_input.text() or not self.export_path_input.text():
                QMessageBox.warning(self, "Validation Error", "All fields must be filled.")
                return

            logging.debug("Validation passed. Starting the batch process.")
            self.thread = BatchProcessThread(
                self.import_path_input.text(),
                self.export_path_input.text(),
                self.project_name_input.text(),
                self.media_type_dropdown.currentText(),
                self.capture_date_selector.date().toString(DEFAULT_CAPTURE_DATE_FORMAT),
                self.camera_number_input.text(),
                self.scene_number_input.text()
            )
            self.thread.progress_updated.connect(self.progress_bar.setValue)
            self.thread.completed.connect(lambda: QMessageBox.information(self, "Success", "Process completed!"))
            self.thread.error_occurred.connect(lambda msg: QMessageBox.critical(self, "Error", msg))
            self.thread.start()
        except Exception as e:
            logging.error(f"Error during batch process setup: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", str(e))

    def save_settings(self):
        # Saves current GUI inputs to a settings file.
        settings = {
            "project_name": self.project_name_input.text(),
            "import_path": self.import_path_input.text(),
            "export_path": self.export_path_input.text(),
            "media_type": self.media_type_dropdown.currentText(),
            "capture_date": self.capture_date_selector.date().toString(DEFAULT_CAPTURE_DATE_FORMAT),
            "camera_number": self.camera_number_input.text(),
            "scene_number": self.scene_number_input.text(),
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        # Loads previous GUI inputs from a settings file.
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                self.project_name_input.setText(settings.get("project_name", ""))
                self.import_path_input.setText(settings.get("import_path", ""))
                self.export_path_input.setText(settings.get("export_path", ""))
                self.media_type_dropdown.setCurrentText(settings.get("media_type", DEFAULT_MEDIA_TYPE))
                self.capture_date_selector.setDate(QDate.fromString(settings.get("capture_date", ""), DEFAULT_CAPTURE_DATE_FORMAT))
                self.camera_number_input.setText(settings.get("camera_number", ""))
                self.scene_number_input.setText(settings.get("scene_number", ""))

    def handle_batch_error(self, msg):
        # Logs and displays any errors from the batch process.
        logging.error(f"Batch process failed: {msg}")
        QMessageBox.critical(self, "Error", msg)
