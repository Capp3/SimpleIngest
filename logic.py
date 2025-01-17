import os
import shutil
import logging
from datetime import datetime
from config import VALID_FILE_EXTENSIONS, LOGGING, LOG_FILE

# Configure Logging
def setup_logging():
    """Sets up logging using the configuration from config.py."""
    log_level = getattr(logging, LOGGING.get("level", "INFO").upper(), logging.INFO)
    log_format = LOGGING.get("format", "%(asctime)s - %(levelname)s - %(message)s")
    date_format = LOGGING.get("datefmt", "%Y-%m-%d %H:%M:%S")
    log_file = LOGGING.get("log_file")

    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        filename=LOG_FILE,
        filemode="a",
    )
    if not log_file:
        # Add a console handler if no log file is specified
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        logging.getLogger().addHandler(console_handler)

# Call setup_logging at the beginning of your script
setup_logging()

# Example log messages to verify setup
logging.debug("Debugging mode enabled.")
logging.info("Starting the script.")
logging.warning("This is a warning message.")
logging.error("An error occurred.")
logging.critical("Critical error encountered.")

# Scan Import and Export Directories
def scan_directory(directory):
    """Scans a directory and returns a list of files."""
    try:
        logging.debug(f"Scanning directory: {directory}")
        file_list = [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file))
        ]
        logging.info(f"Scanned {directory}, found {len(file_list)} files.")
        return file_list
    except Exception as e:
        logging.error(f"Error scanning directory {directory}: {e}")
        raise

# Alphabetise Files
def alphabetise_files(file_list):
    """Sorts a list of file paths alphabetically by file name."""
    logging.debug("Sorting files alphabetically.")
    return sorted(file_list, key=lambda x: os.path.basename(x))

# Filter Files by Extension
def filter_files_by_extension(file_list, media_type):
    """Filters files by valid extensions for the selected media type."""
    valid_extensions = VALID_FILE_EXTENSIONS.get(media_type, [])
    filtered_files = [file for file in file_list if os.path.splitext(file)[1].lower() in valid_extensions]

    if not filtered_files:
        logging.error(f"No valid files found for media type: {media_type}")
        raise ValueError(f"No files matching {media_type} extensions found.")
    
    logging.debug(f"Filtered files for media type {media_type}: {filtered_files}")
    return filtered_files

# Rename Files
def rename_files(file_list, project_name, capture_date, camera_id, scene_id, import_date):
    """
    Renames files in the import directory based on the defined schema.
    """
    try:
        formatted_capture_date = datetime.strptime(capture_date, "%d/%m/%Y").strftime("%Y%m%d")
    except ValueError:
        logging.error(f"Invalid capture date format: {capture_date}")
        raise ValueError(f"Capture date must be in 'DD/MM/YYYY' format, got '{capture_date}'.")

    renamed_files = []
    for idx, file in enumerate(file_list, start=1):
        dir_path = os.path.dirname(file)
        ext = os.path.splitext(file)[1]
        new_name = (
            f"{project_name}-C{formatted_capture_date}-CM{camera_id}-S{scene_id}-I{import_date}-{idx:04d}{ext}"
        )
        new_path = os.path.join(dir_path, new_name)
        os.rename(file, new_path)
        renamed_files.append(new_path)
        logging.info(f"Renamed {file} to {new_path}")

    return renamed_files

# Copy Files
def copy_files(filtered_files, export_path):
    """Copies files from the import directory to the export directory."""
    for file in filtered_files:
        destination = os.path.join(export_path, os.path.basename(file))
        shutil.copy(file, destination)
        logging.info(f"Copied {file} to {destination}")

# Verify Files
def verify_files(filtered_files, export_path):
    """Verifies that all files were successfully copied."""
    export_files = scan_directory(export_path)
    export_names = {os.path.basename(file) for file in export_files}
    filtered_names = {os.path.basename(file) for file in filtered_files}

    if not filtered_names <= export_names:
        missing_files = filtered_names - export_names
        logging.error(f"Verification failed. Missing files: {missing_files}")
        raise ValueError("File transfer verification failed.")
    logging.info("All files successfully copied.")

# Run Process
def process_batch(import_path, export_path, project_name, media_type, capture_date, camera_id, scene_id):
    """Main function to execute the batch process."""
    try:
        logging.info(f"Starting batch process for project: {project_name}")

        # Step 1: Scan directories
        import_files = scan_directory(import_path)
        
        # Step 2: Alphabetise files
        import_files = alphabetise_files(import_files)

        # Step 3: Filter by extension
        filtered_files = filter_files_by_extension(import_files, media_type)

        # Step 4: Rename files
        import_date = datetime.now().strftime("%Y%m%d")
        renamed_files = rename_files(filtered_files, project_name, capture_date, camera_id, scene_id, import_date)

        # Step 5: Copy files to the export directory
        copy_files(renamed_files, export_path)

        # Step 6: Verify files
        verify_files(renamed_files, export_path)

        logging.info("Batch process completed successfully.")
        return True

    except Exception as e:
        logging.error(f"Batch process failed: {e}")
        raise
