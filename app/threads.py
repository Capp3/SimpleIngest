from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil
from datetime import datetime
from app.config import (
    VALID_FILE_EXTENSIONS
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