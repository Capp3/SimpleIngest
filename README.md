# SimpleIngest

Simple media file renaming and importing tool

## General Information

### Captured Variables

| Name         | Type   | input format  | Var Name | Desc.                 | Notes                                                           |
|--------------|--------|---------------|----------|-----------------------|-----------------------------------------------------------------|
| Import Path  | path   | file explorer | I_PATH   | content directory     |                                                                 |
| Export Path  | path   | file explorer | E_PATH   | Destination Directory | must allow for new directory creation                           |
| Capture Date | DATE   | DD/MM/YYYY    | C_DATE   | Date media captured   | needs to be reformated in file name to YYYYMMDD                 |
| Import Date  | DATE   | YYYYMMDD      | I_DATE   | Date media imported   | should be automatically populated                               |
| Camera Num   | int    | ##            | CAM_ID   | Camera Used           | Should be required to be 2 numerical digits                     |
| Scene Num    | int    | ####          | SHOT_ID  | Scene Number          | Should be required to be 4 numerical digits                     |
| Project      | string | text          | PRJT     | Project Name          | Limit 16 digits, no special char., spaces changed to underscore |
| Media Type   | vars   | drop down     | M_TYPE   | Image or Video Files  |                                                                 |
| File Num     | int    | auto          | F_NUM    | File Number           | Automated counter to number files as they are renamed           |
| Log File     | path   | file explorer | LOG_PATH | Log file location     | Should be saved between sessions                                |

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

## Installation and Run

### Prerequisites

- Python 3
- Pip

### Running via Python and CLI

create venv and install requirements

```bash
python3 -m venv ingest
source ingest/bin/activate
pip install -r requirements.txt
```
