# YouTube to MP3 or Video Downloader 🎵📹

A professional-grade tool to download YouTube videos and playlists as MP3 or video files with advanced features like CLI and enhanced GUI support.

## Features
- **CLI and Enhanced GUI Interfaces**: Choose between a sleek command-line interface with tab completion or a modern Tkinter GUI with `ttkbootstrap` for a polished look, tooltips, and responsive design (falls back to standard `tkinter` if `ttkbootstrap` is unavailable).
- **MP3 or Video Downloads**: Download as MP3 audio or video with quality selection.
- **Command-Line Arguments**: Run directly with `python YT-Downloader.py --url <URL> --type mp3 --quality 192k --output /home/username/songs`.
- **Download Single Videos or Playlists**: Convert YouTube videos or entire playlists (100+ items) to MP3 or video.
- **Large Playlist Support**: Handles 100-200 item playlists with sequential processing and retry logic.
- **Audio Quality Options**: For MP3, choose from best, 192k, 128k, 64k.
- **Video Quality Options**: For video, choose from 4K, 2K, 1080p, 720p, 480p, 360p, 144p with automatic fallback to the highest available quality.
- **Custom Output Path**: Supports absolute paths (e.g., `/home/username/songs` for MP3, `/home/username/videos` for video) or defaults to `./downloads` (MP3) or `./videos` (video).
- **File Picker in GUI**: Select output folder using the system’s file manager.
- **Tab Completion**: Press Tab to complete menu options in CLI.
- **Quiet Output**: Suppresses verbose `yt-dlp` logs for a clean UI, including repetitive HTTP 403 errors.
- **Retry Mechanism**: Automatically retries failed downloads up to 3 times.
- **Rich CLI Interface**: Beautiful progress bars and menus using the `rich` library.
- **Configurable Settings**: Save default audio and video quality and max parallel downloads.
- **Enhanced GUI**: Larger window (800x600), modern `flatly` theme (if `ttkbootstrap` installed), tooltips, persistent quality selection when switching between MP3 and Video, and robust error handling.
- **Bypass Restrictions**: Uses `--cookies-from-browser firefox` to handle HTTP 403 errors (requires Firefox installed; can be changed to `chrome` or other browsers).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Devdas-gupta/YouTube-to-MP3-Downloader.git
   cd YouTube-to-MP3-Downloader
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   sudo apt install ffmpeg -y  # On Ubuntu/Debian
   # For macOS: brew install ffmpeg
   # For Windows: Install ffmpeg and add to PATH
   ```
   If `ttkbootstrap` installation fails, the script will fall back to standard `tkinter` for the GUI.

4. **Run the Tool**:
   ```bash
   python YT-Downloader.py
   ```

## Requirements
- Python 3.8+
- `yt-dlp`
- `ffmpeg`
- `rich`
- `ttkbootstrap` (optional, falls back to `tkinter` if not installed)
- Firefox (or another browser like Chrome) for cookie extraction to bypass HTTP 403 errors

Install them with:
```bash
pip install yt-dlp rich ttkbootstrap
```

If you encounter issues with `ttkbootstrap`, try:
```bash
pip install ttkbootstrap --force-reinstall
```

To update `yt-dlp` for the latest fixes:
```bash
pip install yt-dlp --upgrade
```

## Usage

### CLI Usage
Run the script to access the interactive menu:
```bash
python YT-Downloader.py
```
Choose from (press Tab to complete options):
- **Option 1**: Download a playlist as MP3 or video (supports 100+ items).
- **Option 2**: Download a single video as MP3 or video.
- **Option 3**: Configure settings (default audio/video quality, max parallel downloads).
- **Option 4**: Launch the GUI.
- **Option 5**: Exit.

For playlists or single videos, choose:
- **Download as [1] MP3 or [2] Video**
- For MP3: Select audio quality (best, 192k, 128k, 64k).
- For Video: Select video quality (4K, 2K, 1080p, 720p, 480p, 360p, 144p) with fallback to highest available.

Or use command-line arguments:
```bash
python YT-Downloader.py --url <YouTube_URL> --type <mp3|video> --quality <quality> --output <directory> [--playlist] [--gui]
```
Examples:
```bash
python YT-Downloader.py --url https://www.youtube.com/playlist?list=example --type mp3 --quality 192k --output /home/username/songs --playlist
python YT-Downloader.py --url https://www.youtube.com/watch?v=example --type video --quality 1080p --output /home/username/videos
```

### GUI Usage
Launch the GUI directly:
```bash
python YT-Downloader.py --gui
```
Or select option 4 from the CLI menu. Choose “MP3” or “Video” from the dropdown, select quality (MP3: best, 192k, 128k, 64k; Video: 4K, 2K, 1080p, 720p, 480p, 360p, 144p), enter the URL, select output folder via the "Browse Folder" button or type a path (e.g., `/home/username/songs` or `/videos`), check the playlist option if needed, and click "Download". Press Enter for default `./downloads` (MP3) or `./videos` (video). Tooltips guide you through each field. Quality selection persists when switching between MP3 and Video.

## Example
### CLI Example (Single Video as Video)
```bash
🎵 YouTube to MP3 or Video Downloader 🎵
Version: 2.9.2
Author: Devdas Gupta
GitHub: github.com/Devdas-gupta

┌────────────── Menu Options ──────────────┐
│ [1] Download YouTube Playlist            │
│ [2] Download Single Video                │
│ [3] Configure Settings                   │
│ [4] Launch GUI                           │
│ [5] Exit                                 │
└──────────────────────────────────────────┘
Choose an option: 2
🎵 Enter Video URL: https://youtu.be/Abk7L9zmbG4
📥 Download as [1] MP3 or [2] Video? 2
📂 Enter output directory (e.g., /home/username/videos) or press Enter for ./videos: /home/username/Videos
🎚️ Choose video quality (e.g., 4K, 2K, 1080p, 720p, 480p, 360p, 144p) [default: best]: 1080p
[+] Preparing download...
[+] Found 1 video(s) in video
[+] Processing video 1/1: Aasman Ko Chukar Dekha | Return Of Hanuman (Animation) I Daler Mehndi (Video at 720p)
[████████████████████████████] 00:00:05 Downloading...
✅ Downloaded Aasman Ko Chukar Dekha | Return Of Hanuman (Animation) I Daler Mehndi
✅ Completed: 1/1 downloads successful!
```

### GUI Example
Run `python YT-Downloader.py --gui`, select “Video” from the “Download Type” dropdown, choose “1080p” from the “Quality” dropdown, switch to “MP3” and verify quality options update to [best, 192k, 128k, 64k], switch back to “Video” and verify “1080p” is restored, click “Browse Folder” to select `/home/username/videos` or press Enter for `./videos`, enter a video URL, and click “Download”. The status label updates with progress, e.g., “Downloading Aasman Ko Chukar Dekha at 720p…”.

## Troubleshooting
- **HTTP Error 403**: Ensure Firefox (or your preferred browser) is installed and has accessed YouTube recently to generate cookies. Alternatively, update `yt-dlp`:
  ```bash
  pip install yt-dlp --upgrade
  ```
- **Dependency Issues**: If `ttkbootstrap` fails, the script falls back to `tkinter`. Install manually:
  ```bash
  pip install ttkbootstrap --force-reinstall
  ```

## Contributing
Submit issues or pull requests on [GitHub](https://github.com/Devdas-gupta/YouTube-to-MP3-Downloader).

## License
MIT License. See [LICENSE](LICENSE) for details.

## Author
Devdas Gupta | [GitHub Profile](https://github.com/Devdas-gupta)
