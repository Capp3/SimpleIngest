from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QFileDialog, QDateEdit, QProgressBar, QWidget
)
from PyQt5.QtCore import QDate
import os
import shutil
import logging

VALID_EXTENSIONS = {
    "Video": ["mov", "mp4", "m4v", "flv", "avi", "wmv", "mpeg", "raw", "avchd", "mkv"],
    "Image": ["jpg", "jpeg", "gif", "png", "tiff", "psd"],
    "Audio": ["mp3", "m4a", "wav", "flac", "aac", "aiff", "pcm"]
}

media_type = self.media_type_dropdown.currentText()  # Assuming you have a dropdown in your GUI
import_path = self.import_path_input.text()  # Path from the GUI input

if not os.path.exists(import_path):
    print("Invalid import path")
    return

filtered_files = filter_files_by_type(import_path, media_type)
if not filtered_files:
    print(f"No valid {media_type} files found in the directory.")
    return

print(f"Found {len(filtered_files)} {media_type} files.")

class MediaManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Media Ingest Manager")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Import Path
        self.import_path_label = QLabel("Import Path:")
        self.import_path_input = QLineEdit()
        self.import_path_button = QPushButton("Browse")
        self.import_path_button.clicked.connect(self.select_import_path)
        layout.addWidget(self.import_path_label)
        layout.addWidget(self.import_path_input)
        layout.addWidget(self.import_path_button)

        # Export Path
        self.export_path_label = QLabel("Export Path:")
        self.export_path_input = QLineEdit()
        self.export_path_button = QPushButton("Browse")
        self.export_path_button.clicked.connect(self.select_export_path)
        layout.addWidget(self.export_path_label)
        layout.addWidget(self.export_path_input)
        layout.addWidget(self.export_path_button)

        # Capture Date
        self.capture_date_label = QLabel("Capture Date:")
        self.capture_date_input = QDateEdit()
        self.capture_date_input.setCalendarPopup(True)
        self.capture_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.capture_date_label)
        layout.addWidget(self.capture_date_input)

        # Buttons
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.activate_process)
        layout.addWidget(self.activate_button)

        # Media Type Dropdown
        self.media_type_label = QLabel("Select Media Type:")
        self.media_type_dropdown = QComboBox()
        self.media_type_dropdown.addItems(["Video", "Image", "Audio"])  # Add your options here
        layout.addWidget(self.media_type_label)
        layout.addWidget(self.media_type_dropdown)

        # Buttons
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self.activate_process)
        layout.addWidget(self.activate_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_import_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Import Directory")
        if path:
            self.import_path_input.setText(path)

    def select_export_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if path:
            self.export_path_input.setText(path)

    def activate_process(self):

# Application
        # Check if extention matches selected type

        def is_valid_file(file_name, media_type):
            # Get the file extension
            file_extension = os.path.splitext(file_name)[-1].lower().strip('.')
            # Check if it's in the valid extensions for the media type
            return file_extension in VALID_EXTENSIONS.get(media_type, [])

        def filter_files(import_path, file_extensions):
            return [f for f in os.listdir(import_path) if f.lower().endswith(tuple(file_extensions))]
        
        for file in filtered_files:
            if not is_valid_file(file, media_type):
                print(f"Skipping invalid file: {file}")
                continue

        def rename_file(original_name, project, capture_date, camera_id, shot_id, import_date, file_num):
            extension = original_name.split('.')[-1]
            new_name = f"{project}-C{capture_date}-CM{camera_id}-S{shot_id}-I{import_date}-{file_num:04d}.{extension}"
            return new_name
        
        def copy_files(import_path, export_path, files):
            for file in files:
                shutil.copy(os.path.join(import_path, file), export_path)

        logging.basicConfig(filename='media_manager.log', level=logging.INFO)

        self.progress_bar.setValue(int((current_file_index / total_files) * 100))

        def log_action(message):
            logging.info(message)

if __name__ == "__main__":
    app = QApplication([])
    manager = MediaManager()
    manager.show()
    app.exec_()