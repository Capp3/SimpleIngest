from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QProgressBar, QWidget, QFileDialog, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate, QThread, pyqtSignal
import logging
import os
import json
import shutil
from datetime import datetime
from config import (
    SETTINGS_FILE, LOG_FILE, VALID_FILE_EXTENSIONS,
    DEFAULT_MEDIA_TYPE, DEFAULT_CAPTURE_DATE_FORMAT,
    CAMERA_NUMBER_PATTERN, SCENE_NUMBER_PATTERN,
    APP_NAME, VERSION
)

class BatchProcessThread(QThread):
    progress_updated = pyqtSignal(int)
    completed = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, import_path, export_path, project_name, media_type, capture_date, camera_number, scene_number):
        super().__init__()
        self.import_path = import_path
        self.export_path = export_path
        self.project_name = project_name
        self.media_type = media_type
        self.capture_date = capture_date
        self.camera_number = camera_number
        self.scene_number = scene_number

    def run(self):
        try:
            # Scan directory
            file_list = [
                os.path.join(self.import_path, f)
                for f in os.listdir(self.import_path)
                if os.path.isfile(os.path.join(self.import_path, f))
            ]
            if not file_list:
                raise ValueError("No files found in the import directory.")

            # Filter files
            valid_extensions = VALID_FILE_EXTENSIONS.get(self.media_type, [])
            filtered_files = [
                f for f in file_list if os.path.splitext(f)[1].lower() in valid_extensions
            ]
            if not filtered_files:
                raise ValueError(f"No files matching {self.media_type} extensions found.")

            # Prepare file renaming and copying
            total_files = len(filtered_files)
            formatted_capture_date = datetime.strptime(self.capture_date, "%d/%m/%Y").strftime("%Y%m%d")
            import_date = datetime.now().strftime("%Y%m%d")

            for index, file_path in enumerate(filtered_files, start=1):
                ext = os.path.splitext(file_path)[1]
                new_name = (
                    f"{self.project_name}-C{formatted_capture_date}-CM{self.camera_number}-"
                    f"S{self.scene_number}-I{import_date}-{index:04d}{ext}"
                )
                renamed_path = os.path.join(self.import_path, new_name)

                # Rename the file
                os.rename(file_path, renamed_path)

                # Copy the renamed file to export path
                export_path = os.path.join(self.export_path, new_name)
                os.makedirs(self.export_path, exist_ok=True)
                shutil.copy(renamed_path, export_path)

                # Update progress
                self.progress_updated.emit(int((index / total_files) * 100))

            # Signal completion
            self.completed.emit()

        except Exception as e:
            self.error_occurred.emit(str(e))


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
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="gui - %(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info(f"Starting {APP_NAME} v{VERSION}")

    def init_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        main_layout = QVBoxLayout()

        # Project Name
        project_layout = QHBoxLayout()
        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
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

        # Camera Number and Scene Number
        camera_scene_layout = QHBoxLayout()
        self.camera_number_label = QLabel("Camera Number:")
        self.camera_number_input = QLineEdit()
        self.scene_number_label = QLabel("Scene Number:")
        self.scene_number_input = QLineEdit()
        camera_scene_layout.addWidget(self.camera_number_label)
        camera_scene_layout.addWidget(self.camera_number_input)
        camera_scene_layout.addWidget(self.scene_number_label)
        camera_scene_layout.addWidget(self.scene_number_input)
        main_layout.addLayout(camera_scene_layout)

        # Activate Button and Progress Bar
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.start_batch_process)
        main_layout.addWidget(self.activate_button)
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
        # Validation
        if not self.project_name_input.text() or not self.import_path_input.text() or not self.export_path_input.text():
            QMessageBox.warning(self, "Validation Error", "All fields must be filled.")
            return

        # Start processing
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

    def save_settings(self):
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


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    gui = MediaIngestGUI()
    gui.show()
    sys.exit(app.exec_())
