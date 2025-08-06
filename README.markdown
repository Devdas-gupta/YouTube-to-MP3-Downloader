# YouTube to MP3 Downloader 🎵

A professional-grade tool to download YouTube videos and playlists as MP3 files with advanced features like CLI and GUI support.

## Features
- **CLI and GUI Interfaces**: Choose between a sleek command-line interface with tab completion or a user-friendly Tkinter GUI with file picker.
- **Command-Line Arguments**: Run directly with `python youtube_to_mp3.py --url <URL> --quality 192k --output /home/username/songs`.
- **Download Single Videos or Playlists**: Convert YouTube videos or entire playlists (100+ songs) to MP3.
- **Large Playlist Support**: Handles 100-200 song playlists with sequential processing and retry logic.
- **Custom Audio Quality**: Choose from best, 192k, 128k, 64k, or other bitrates.
- **Custom Output Path**: Supports absolute paths (e.g., `/home/username/songs`) or defaults to `./downloads` if not specified.
- **File Picker in GUI**: Select output folder using the system’s file manager.
- **Tab Completion**: Press Tab to complete menu options in CLI.
- **Quiet Output**: Suppresses verbose `yt-dlp` logs for a clean UI.
- **Retry Mechanism**: Automatically retries failed downloads up to 3 times.
- **Rich CLI Interface**: Beautiful progress bars and menus using the `rich` library.
- **Configurable Settings**: Save default quality and parallel download settings.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Devdas-gupta/YouTube-to-MP3-Downloader
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

4. **Run the Tool**:
   ```bash
   python youtube_to_mp3.py
   ```

## Requirements
- Python 3.8+
- `yt-dlp`
- `ffmpeg`
- `rich`

Install them with:
```bash
pip install yt-dlp rich
```

## Usage

### CLI Usage
Run the script to access the interactive menu:
```bash
python youtube_to_mp3.py
```
Choose from (press Tab to complete options):
- **Option 1**: Download a playlist as MP3s (supports 100+ songs).
- **Option 2**: Download a single video as an MP3.
- **Option 3**: Configure settings (default quality, max parallel downloads).
- **Option 4**: Launch the GUI.
- **Option 5**: Exit.

Or use command-line arguments:
```bash
python youtube_to_mp3.py --url <YouTube_URL> --quality <quality> --output <directory> [--playlist] [--gui]
```
Example:
```bash
python youtube_to_mp3.py --url https://www.youtube.com/playlist?list=example --quality 192k --output /home/username/songs --playlist
```

### GUI Usage
Launch the GUI directly:
```bash
python youtube_to_mp3.py --gui
```
Or select option 4 from the CLI menu. Enter the URL, select output folder via the "Browse" button or type a path (e.g., `/home/username/songs`), choose quality, check the playlist option if needed, and click "Download". Press Enter for default `./downloads`.

## Example
### CLI Example (Playlist with 100+ songs)
```bash
🎵 YouTube to MP3 Downloader 🎵
Version: 2.7.0
Author: Devdas Gupta
GitHub: github.com/Devdas-gupta

┌────────────── Menu Options ──────────────┐
│ [1] Download YouTube Playlist as MP3     │
│ [2] Download Single Video as MP3         │
│ [3] Configure Settings                   │
│ [4] Launch GUI                           │
│ [5] Exit                                 │
└──────────────────────────────────────────┘
Choose an option: 1
🎵 Enter Playlist URL: https://www.youtube.com/playlist?list=example
📂 Enter output directory (e.g., /home/username/songs) or press Enter for ./downloads: 
🎚️ Choose audio quality (e.g., best, 192k, 128k, 64k) [default: best]: 192k

[+] Preparing download...
[+] Found 150 video(s) in playlist
[+] Processing video 1/150: Song Title 1
[████████████████████████████] 00:00:01 Downloading Song Title 1...
✅ Downloaded Song Title 1
[+] Processing video 2/150: Song Title 2
...
✅ Completed: 150/150 downloads successful!
```

### GUI Example
Run `python youtube_to_mp3.py --gui`, enter the playlist URL, click "Browse" to select `/home/username/songs` or press Enter for `./downloads`, select quality, check "Download as Playlist", and click "Download". The status label updates with progress.

## Contributing
Submit issues or pull requests on [GitHub](https://github.com/Devdas-gupta/YouTube-to-MP3-Downloader).

## License
MIT License. See [LICENSE](LICENSE) for details.

## Author
Devdas Gupta | [GitHub Profile](https://github.com/Devdas-gupta)
