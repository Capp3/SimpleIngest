# SimpleIngest

A lightweight tool for renaming, organising, and importing video, audio, and photo media files.

![Interface](/images/simpleingest.PNG)

## Overview

SimpleIngest is designed to meet straightforward media ingest needs by standardising file naming and simplifying workflows. It renames and copies files without altering or managing metadata.

While there are many simular tools, this one suits our workflow and removes unnecessary clutter from the operator. File extensions and groups can be modified in the `config.py` file.

This tool is written in Python and provides an intuitive interface for users to streamline the organisation of their media files.

---

- [SimpleIngest](#simpleingest)
  - [Overview](#overview)
  - [How It Works](#how-it-works)
    - [Workflow](#workflow)
  - [Installation and Usage](#installation-and-usage)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Manual Installation](#manual-installation)
    - [Running](#running)
      - [Running with python](#running-with-python)
      - [Creating Launch Icon on MacOS](#creating-launch-icon-on-macos)
  - [Future Plans](#future-plans)
  - [Contributing](#contributing)
  - [License](#license)
  - [Support](#support)

## How It Works

After launching the application, a simple graphical user interface (GUI) is presented, requesting the following details:

| Field         | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **Project Name**  | A unique 16-character identifier for the project.                        |
| **Import Path**   | Directory where the source files are located.                            |
| **Export Path**   | Directory where the processed files will be saved.                       |
| **Media Type**    | Type of media being imported (filters files by extension).               |
| **Capture Date**  | Date the media was captured (in `DD/MM/YYYY` format).                    |
| **Camera Number** | A 2-digit identifier for the camera or source.                           |
| **Scene Number**  | A 4-digit identifier for the scene or shot.                              |

### Workflow

1. **File Filtering**:
   - Only media files matching the selected type are processed.
2. **Renaming**:
   - Files are renamed based on a standardised format:

     ```text
     {Project Name}-C{Capture Date}-CM{Camera Number}-S{Scene Number}-I{Import Date}-{Number}.{Extension}
     ```

   - Example: `MyProject-C20230101-CM01-S0001-I20250117-0001.mp4`
3. **File Copying**:
   - Files are copied to the specified export directory.
4. **Verification**:
   - Ensures all files are successfully moved.

> **Note**: Files are renamed in place to support workflows that require SD card formatting applications to scan local storage before erasing media.

---

## Installation and Usage

### Prerequisites

- Python 3.x
- Pip (Python package manager)

### Installation

These instructions are tested on macOS and should also apply to Linux. Windows instructions may follow in future releases. For Windows users, keep an eye on the [Releases Page](https://github.com/Capp3/SimpleIngest/releases) for a standalone executable.

#### Manual Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Capp3/SimpleIngest.git
   ```

2. Navigate to the project directory:

   ```bash
   cd SimpleIngest
   ```

3. Create a Python virtual environment:

   ```bash
   python3 -m venv ingest
   ```

4. Activate the virtual environment:

   ```bash
   source ingest/bin/activate
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the application:

   ```bash
   python3 simpleingest.py
   ```

### Running

#### Running with python

Once the program is installed it can then be run from the command line

1. Navigate to Program Direcoty

   ```bash
   /path/Simplingest
   ```

2. Start VENV

   ```bash
   source ingest/bin/activate
   ```

3. Start the application:

   ```bash
   python3 simpleingest.py
   ```

#### Creating Launch Icon on MacOS

Launch `Shortcuts`

I'll be back right after this candy bar....

---

## Future Plans

- Fix persistent settings
- Selected field inclusion
- Add Windows installation instructions.
- Release standalone executables for macOS and Windows.
- Incorporate additional metadata management features.

---

## Contributing

Contributions are welcome! If you'd like to improve the tool or add features:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

---

## Support

If you encounter issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/Capp3/SimpleIngest/issues).
