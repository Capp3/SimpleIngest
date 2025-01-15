import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

# Set up logging
logging.basicConfig(filename='media_ingest.log', level=logging.INFO)

class MediaIngestApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Media Ingest Application')

        # Define variables
        self.import_path = tk.StringVar()
        self.export_path = tk.StringVar()
        self.capture_date = tk.StringVar()
        self.import_date = datetime.datetime.now().strftime('%Y%m%d')
        self.camera_id = tk.StringVar()
        self.scene_id = tk.StringVar()
        self.project_name = tk.StringVar()
        self.media_type = tk.StringVar()
        self.log_path = tk.StringVar()

        self.create_gui()

    def create_gui(self):
        # Create the GUI components
        tk.Label(self.root, text="Import Path").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.import_path).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_import).grid(row=0, column=2)

        tk.Label(self.root, text="Export Path").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.export_path).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_export).grid(row=1, column=2)

        tk.Label(self.root, text="Capture Date (DD/MM/YYYY)").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.capture_date).grid(row=2, column=1)

        tk.Label(self.root, text="Camera ID (2 digits)").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.camera_id).grid(row=3, column=1)

        tk.Label(self.root, text="Scene ID (4 digits)").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.scene_id).grid(row=4, column=1)

        tk.Label(self.root, text="Project Name (max 16 chars)").grid(row=5, column=0)
        tk.Entry(self.root, textvariable=self.project_name).grid(row=5, column=1)

        tk.Label(self.root, text="Media Type").grid(row=6, column=0)
        tk.OptionMenu(self.root, self.media_type, 'Video', 'Image', 'Audio').grid(row=6, column=1)

        tk.Label(self.root, text="Log File Path").grid(row=7, column=0)
        tk.Entry(self.root, textvariable=self.log_path).grid(row=7, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_log).grid(row=7, column=2)

        tk.Button(self.root, text="Activate", command=self.activate_process).grid(row=8, column=1)
        tk.Button(self.root, text="Exit", command=self.root.quit).grid(row=9, column=1)

    def browse_import(self):
        self.import_path.set(filedialog.askdirectory())

    def browse_export(self):
        self.export_path.set(filedialog.askdirectory())

    def browse_log(self):
        self.log_path.set(filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")]))

    def activate_process(self):
        # Step 1: Validate inputs
        # Step 2: Rename files
        # Step 3: Check for conflicts
        # Step 4: Transfer files with progress bar
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaIngestApp(root)
    root.mainloop()
