from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil
import logging
from datetime import datetime
from app.config import (
    VALID_FILE_EXTENSIONS
)

# The BatchProcessThread class handles batch file processing in a separate thread.
# It uses PyQt5 signals to communicate progress, completion, and errors with the main thread.
class BatchProcessThread(QThread):
    # Signal emitted to update the progress bar in the GUI. Emits an integer representing progress percentage.
    progress_updated = pyqtSignal(int)
    # Signal emitted when the batch process is completed successfully.
    completed = pyqtSignal()
    # Signal emitted when an error occurs during the batch process. Emits an error message as a string.
    error_occurred = pyqtSignal(str)

    # Constructor to initialize the thread with user-provided parameters.
    def __init__(self, import_path, export_path, project_name, media_type, capture_date, camera_number, scene_number):
        super().__init__()
        # Initialize instance variables with input parameters.
        self.import_path = import_path  # Path to import files from
        self.export_path = export_path  # Path to export files to
        self.project_name = project_name  # Name of the project
        self.media_type = media_type  # Type of media (e.g., Video, Audio, Images)
        self.capture_date = capture_date  # Date when the files were captured
        self.camera_number = camera_number  # Camera number used for the capture
        self.scene_number = scene_number  # Scene number of the media

    # Main execution function of the thread.
    # This function performs scanning, filtering, renaming, copying, and progress updates.
    def run(self):
        try:
            # Log the start of the batch process with details about the input parameters.
            logging.info("Batch process started.")
            logging.debug(f"Parameters: Import Path: {self.import_path}, Export Path: {self.export_path}, "
                        f"Project Name: {self.project_name}, Media Type: {self.media_type}, "
                        f"Capture Date: {self.capture_date}, Camera Number: {self.camera_number}, "
                        f"Scene Number: {self.scene_number}")

            # Scan the import directory for files and log the file list.
            logging.info(f"Scanning directory: {self.import_path}")
            file_list = [
                os.path.join(self.import_path, f)
                for f in os.listdir(self.import_path)
                if os.path.isfile(os.path.join(self.import_path, f)) and not f.startswith(".")
            ]
            logging.debug(f"Found files: {file_list}")
            if not file_list:
                # Raise an error if no files are found in the import directory.
                raise ValueError("No files found in the import directory.")

            # Filter files based on the selected media type and log the filtered list.
            valid_extensions = VALID_FILE_EXTENSIONS.get(self.media_type, [])
            filtered_files = [
                f for f in file_list if os.path.splitext(f)[1].lower() in valid_extensions
            ]
            logging.debug(f"Filtered files: {filtered_files}")
            if not filtered_files:
                # Raise an error if no valid files are found.
                raise ValueError(f"No files matching {self.media_type} extensions found.")

            # Prepare for file processing by formatting the capture date and getting the current date.
            total_files = len(filtered_files)
            formatted_capture_date = datetime.strptime(self.capture_date, "%d/%m/%Y").strftime("%Y%m%d")
            import_date = datetime.now().strftime("%Y%m%d")
            logging.info(f"Total files to process: {total_files}")

            # Iterate over each filtered file for processing.
            for index, file_path in enumerate(filtered_files, start=1):
                logging.debug(f"Processing file {index}/{total_files}: {file_path}")

                # Generate the new file name based on the naming convention.
                ext = os.path.splitext(file_path)[1]
                new_name = (
                    f"{self.project_name}-C{formatted_capture_date}-CM{self.camera_number}-"
                    f"S{self.scene_number}-I{import_date}-{index:04d}{ext}"
                )
                renamed_path = os.path.join(self.import_path, new_name)

                # Rename the file and log the action.
                logging.debug(f"Renaming file {file_path} to {renamed_path}")
                os.rename(file_path, renamed_path)
                logging.info(f"File renamed: {renamed_path}")

                # Copy the renamed file to the export path and log the action.
                export_path = os.path.join(self.export_path, new_name)
                os.makedirs(self.export_path, exist_ok=True)
                logging.debug(f"Copying file {renamed_path} to {export_path}")
                shutil.copy(renamed_path, export_path)
                logging.info(f"File copied to export path: {export_path}")

                # Calculate and emit the progress percentage.
                progress = int((index / total_files) * 100)
                logging.debug(f"Progress updated to {progress}%")
                self.progress_updated.emit(progress)

            # Log the successful completion of the batch process.
            logging.info("Batch processing completed successfully.")
            self.completed.emit()

        except Exception as e:
            # Log and emit any error that occurs during the batch process.
            logging.error(f"Batch processing failed: {e}")
            self.error_occurred.emit(str(e))
