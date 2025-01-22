# Notepad

## Structure

```
SimpleIngest
 |- README.md             # Readme File
 |- .gitignore
 |- simpleingest.sh       # Mac Launch Script
 |- simpleingest.py       # Python Entry Script
 |- config.py             # python variables
 |- requirements.txt      # Python Requirements
 |- settings.json         # Settings File
 |- log
 |   |-simpleingest.log
 |- app
     |- main.py          
     |- threads.py        # Batch Process Thread
```

## Captured Variables

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

## File formats 

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

## File Name format

`{PRJT}-C{C_DATE}-CM{CAM_ID}-S{SHOT_ID}-I{I_DATE}-{F_NUM}.{Existing Extension}`
