from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QProgressBar, QWidget, QFileDialog, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
import json

class MediaIngestGUI(QMainWindow):
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        super().__init__()
        self.init_ui()

        # Variables to store input data
        self.project_name = ""
        self.import_path = ""
        self.export_path = ""
        self.media_type = ""
        self.capture_date = None
        self.camera_number = ""
        self.scene_number = ""

        # Load previous settings
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("Media Ingest Manager")
        self.setGeometry(100, 100, 600, 400)

        # Main layout for the interface
        main_layout = QVBoxLayout()

        # Project Name Entry with informational default text (Above Media Type and Capture Date)
        project_layout = QHBoxLayout()

        self.project_name_label = QLabel("Project Name:")
        self.project_name_input = QLineEdit()
        self.project_name_input.setMaxLength(16)  # Limit to 16 characters
        self.project_name_input.setPlaceholderText("Project Name")  # Informational default

        project_layout.addWidget(self.project_name_label)
        project_layout.addWidget(self.project_name_input)

        # Add project layout to main layout
        main_layout.addLayout(project_layout)

        # Media Type and Capture Date in a horizontal layout
        row_layout = QHBoxLayout()

        # Media Type Dropdown
        self.media_type_label = QLabel("Media Type:")
        self.media_type_dropdown = QComboBox()
        self.media_type_dropdown.addItems(["Video", "Images", "Audio"])

        # Capture Date Selector
        self.capture_date_label = QLabel("Capture Date:")
        self.capture_date_selector = QDateEdit()
        self.capture_date_selector.setDisplayFormat("dd/MM/yyyy")
        self.capture_date_selector.setDate(QDate.currentDate())  # Default to today

        # Add widgets to row layout
        row_layout.addWidget(self.media_type_label)
        row_layout.addWidget(self.media_type_dropdown)
        row_layout.addWidget(self.capture_date_label)
        row_layout.addWidget(self.capture_date_selector)

        # Add row layout to main layout
        main_layout.addLayout(row_layout)

        # Import Path with label next to input
        import_layout = QHBoxLayout()

        self.import_label = QLabel("Import Path:")
        self.import_path_input = QLineEdit()
        self.import_browse_button = QPushButton("Browse")
        self.import_browse_button.clicked.connect(self.browse_import_path)

        import_layout.addWidget(self.import_label)
        import_layout.addWidget(self.import_path_input)
        import_layout.addWidget(self.import_browse_button)

        main_layout.addLayout(import_layout)

        # Export Path with label next to input
        export_layout = QHBoxLayout()

        self.export_label = QLabel("Export Path:")
        self.export_path_input = QLineEdit()
        self.export_browse_button = QPushButton("Browse")
        self.export_browse_button.clicked.connect(self.browse_export_path)

        export_layout.addWidget(self.export_label)
        export_layout.addWidget(self.export_path_input)
        export_layout.addWidget(self.export_browse_button)

        main_layout.addLayout(export_layout)

        # Camera Number and Scene Number in a horizontal layout
        line_layout = QHBoxLayout()

        # Camera Number Entry
        self.camera_number_label = QLabel("Camera Number:")
        self.camera_number_input = QLineEdit()

        # Scene Number Entry
        self.scene_number_label = QLabel("Scene Number:")
        self.scene_number_input = QLineEdit()

        # Add widgets to line layout
        line_layout.addWidget(self.camera_number_label)
        line_layout.addWidget(self.camera_number_input)
        line_layout.addWidget(self.scene_number_label)
        line_layout.addWidget(self.scene_number_input)

        # Add line layout to main layout
        main_layout.addLayout(line_layout)

        # Activate Button
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.store_data)  # Connect to data storage method
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

    def store_data(self):
        # Validate if all fields are filled
        if not self.validate_fields():
            return  # If validation fails, return and don't proceed

        # Fetch values from the GUI
        self.project_name = self.project_name_input.text().replace(" ", "_")
        self.import_path = self.import_path_input.text()
        self.export_path = self.export_path_input.text()
        self.media_type = self.media_type_dropdown.currentText()
        self.capture_date = self.capture_date_selector.date().toString("dd/MM/yyyy")
        self.camera_number = self.camera_number_input.text()
        self.scene_number = self.scene_number_input.text()

        # Save settings
        self.save_settings()

        # Debugging: Print values to the console
        print(f"Project Name: {self.project_name}")
        print(f"Import Path: {self.import_path}")
        print(f"Export Path: {self.export_path}")
        print(f"Media Type: {self.media_type}")
        print(f"Capture Date: {self.capture_date}")
        print(f"Camera Number: {self.camera_number}")
        print(f"Scene Number: {self.scene_number}")

    def validate_fields(self):
        """Validate if all fields are filled in"""
        if not self.project_name_input.text():
            self.show_error_message("Project Name is required.")
            return False
        if not self.import_path_input.text():
            self.show_error_message("Import Path is required.")
            return False
        if not self.export_path_input.text():
            self.show_error_message("Export Path is required.")
            return False
        if not self.camera_number_input.text():
            self.show_error_message("Camera Number is required.")
            return False
        if not self.scene_number_input.text():
            self.show_error_message("Scene Number is required.")
            return False
        return True

    def show_error_message(self, message):
        """Show an error message to the user"""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Validation Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    def save_settings(self):
        """Save current settings to a file."""
        settings = {
            "project_name": self.project_name_input.text().replace(" ", "_"),
            "import_path": self.import_path_input.text(),
            "export_path": self.export_path_input.text(),
            "media_type": self.media_type_dropdown.currentText(),
            "capture_date": self.capture_date_selector.date().toString("dd/MM/yyyy"),
            "camera_number": self.camera_number_input.text(),
            "scene_number": self.scene_number_input.text(),
        }
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        """Load settings from a file."""
        try:
            with open(self.SETTINGS_FILE, "r") as file:
                settings = json.load(file)

                # Restore values to the GUI
                self.project_name_input.setText(settings.get("project_name", "").replace("_", " "))
                self.import_path_input.setText(settings.get("import_path", ""))
                self.export_path_input.setText(settings.get("export_path", ""))
                media_type = settings.get("media_type", "Video")
                if media_type in ["Video", "Images", "Audio"]:
                    self.media_type_dropdown.setCurrentText(media_type)
                self.capture_date_selector.setDate(
                    QDate.fromString(settings.get("capture_date", ""), "dd/MM/yyyy")
                )
                self.camera_number_input.setText(settings.get("camera_number", ""))
                self.scene_number_input.setText(settings.get("scene_number", ""))
        except FileNotFoundError:
            # No settings file, use defaults
            pass


# Run the application
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    gui = MediaIngestGUI()
    gui.show()
    sys.exit(app.exec_())
