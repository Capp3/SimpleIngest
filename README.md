# SimpleIngest

Simple media file renaming and importing tool

## General Information

Meeting simple needs, this is for video file ingest. This tool does not manage metadata in anyway. It renames, and copies files.

The primary intention is for standardization of file naming. It intends to also build in a simple work flow.

The application is written in Python.

### How it works

After the application is started a simple GUI is provided and information requested

| Field         | Description                                                         |
|---------------|---------------------------------------------------------------------|
| Project Name  | 16 Digits to identify the project                                   |
| Import Path   | Select the directory where the files to import are                  |
| Export Path   | Select the directory where the files are to end up                  |
| Media Type    | What type of media are you importing, filters what files are copied |
| Capture Date  | Date media was captured                                             |
| Camera Number | 2 digits to identify camera (or source)                             |
| Scene Number  | 4 digits to identify scene/shot                                     |

Once Activated the script does a few things

- Filters only the media files of the type selected
- Renames the files to a standardized scheme, in place
  - {Project Name}-C{Capture Date}-CM{Camera Number}-S{Scene Number}-I{Import Date}-{Number}.{Extension}
- copies the files to the export directory
- verifies the files have been moved

The files are renamed in place to allow for SD formatting applications that search local storage before erasing media.

## Installation and Run

### Prerequisites

- Python 3
- Pip

### Installation

These instructions are used and tested on an Apple computer. Linux should be much the same. Windows instructions may come, but keep an eye on the releases page for an executable.

#### Manual Installation

```bash
# Clone Github Repo
git clone https://github.com/Capp3/SimpleIngest.git
# Navigate to Simple Ingest Directory
cd SimpleIngest
# Create Python Virtual Environment
python3 -m venv ingest
# Activate Python Environment
source ingest/bin/activate
# Install Requirements
pip install -r requirements.txt
```

The application can then be started

```bash
python3 simpleingest.py
```

## Programming notes below, be warned

### Captured Variables

| Name         | Type   | input format  | Var Name | Desc.                 | Notes                                        |
|--------------|--------|---------------|----------|-----------------------|----------------------------------------------|
| Import Path  | path   | file explorer | I_PATH   | content directory     |                                              |
| Export Path  | path   | file explorer | E_PATH   | Destination Directory | must allow for new directory creation        |
| Capture Date | DATE   | DD/MM/YYYY    | C_DATE   | Date media captured   | convert to YYYYMMDD                          |
| Import Date  | DATE   | YYYYMMDD      | I_DATE   | Date media imported   | auto                                         |
| Camera Num   | int    | ##            | CAM_ID   | Camera Used           |                                              |
| Scene Num    | int    | ####          | SHOT_ID  | Scene Number          |                                              |
| Project      | string | text          | PRJT     | Project Name          | Limit 16 digits,spaces changed to underscore |
| Media Type   | vars   | drop down     | M_TYPE   | Image or Video Files  |                                              |
| File Num     | int    | auto          | F_NUM    | File Number           | Automated counter                            |
| Log File     | path   | file explorer | LOG_PATH | Log file location     |                                              |

### File formats 

1. Video
   1. MOV
   2. MP4
   3. M4V
   4. FLV
   5. AVI
   6. WMV
   7. MPEG
   8. RAW
   9. AVCHD
   10. MKV
2. Images
    1. JPG
    2. JPEG
    3. GIF
    4. PNG
    5. TIFF
    6. PSD
3. Audio
   1. MP3
   2. M4A
   3. WAV
   4. FLAC
   5. AAC
   6. AIFF
   7. PCM

### File Name format

`{PRJT}-C{C_DATE}-CM{CAM_ID}-S{SHOT_ID}-I{I_DATE}-{F_NUM}.{Existing Extension}`


