import os
import subprocess
import shutil
import sys
import asyncio
import argparse
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.table import Table
import yt_dlp
import readline  
try:
    import ttkbootstrap as tbs
    from ttkbootstrap.tooltip import ToolTip
    USE_TTKBOOTSTRAP = True
except ImportError:
    console = Console()
    console.print("[yellow][!] ttkbootstrap not found. Falling back to standard tkinter.[/yellow]")
    USE_TTKBOOTSTRAP = False

# Initialize rich console
console = Console()

# Cache for dependency checks
DEPENDENCY_CACHE = {}

# Check for required external tools
def check_and_install(package_name, install_cmd, pip_package=False):
    if package_name in DEPENDENCY_CACHE:
        return DEPENDENCY_CACHE[package_name]
    found = False
    if pip_package:
        found = is_module_installed(package_name)
    else:
        found = shutil.which(package_name) is not None
        if not found and (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
            venv_bin = os.path.join(sys.prefix, 'bin' if os.name != 'nt' else 'Scripts')
            found = os.path.exists(os.path.join(venv_bin, package_name)) or os.path.exists(os.path.join(venv_bin, f"{package_name}.exe"))
    if not found:
        console.print(f"[red][!] {package_name} not found.[/red]")
        choice = input(f"Do you want to install {package_name}? (y/n): ").lower()
        if choice == 'y':
            console.print(f"[yellow][+] Installing {package_name}...[/yellow]")
            try:
                pip_cmd = f"{sys.executable} -m pip install {package_name}" if pip_package else install_cmd
                result = subprocess.run(pip_cmd, shell=True, check=True, capture_output=True, text=True)
                console.print(f"[green][+] {package_name} installed successfully![/green]")
                DEPENDENCY_CACHE[package_name] = True
                return True
            except subprocess.CalledProcessError as e:
                console.print(f"[red][-] Failed to install {package_name}: {e.stderr}[/red]")
                if package_name == 'ttkbootstrap':
                    console.print("[yellow][!] Continuing with standard tkinter...[/yellow]")
                    return False
                sys.exit(1)
        else:
            console.print(f"[red][-] {package_name} is required. Exiting...[/red]")
            if package_name == 'ttkbootstrap':
                console.print("[yellow][!] Continuing with standard tkinter...[/yellow]")
                return False
            sys.exit(1)
    else:
        DEPENDENCY_CACHE[package_name] = True
        return True

# Check if a Python module is installed
def is_module_installed(module_name):
    try:
        import importlib.util
        return importlib.util.find_spec(module_name) is not None
    except ImportError:
        return False

# Setup tab completion for CLI
def setup_tab_completion():
    options = ['1', '2', '3', '4', '5']
    def complete(text, state):
        matches = [opt for opt in options if opt.startswith(text)]
        return matches[state] if state < len(matches) else None
    readline.set_completer(complete)
    readline.parse_and_bind('tab: complete')

# Sanitize filename to match yt-dlp's output
def sanitize_filename(title):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '_')
    return title.strip()

# Validate and normalize output path
def normalize_output_path(path, download_type):
    if not path or path.strip() == '':
        path = os.path.join(os.getcwd(), 'downloads' if download_type == 'mp3' else 'videos')  # Default based on type
    else:
        path = os.path.expanduser(path.strip())  # Handle ~ for /home/username
        if not os.path.isabs(path):
            path = os.path.abspath(path)
    return path

# Show banner with a professional look
def banner():
    console.print(Panel.fit("""
██╗   ██╗████████╗        ████████╗ ██████╗         ███╗   ███╗██████╗ ██████╗        
╚██╗ ██╔╝╚══██╔══╝        ╚══██╔══╝██╔═══██╗        ████╗ ████║██╔══██╗╚════██╗       
 ╚████╔╝    ██║              ██║   ██║   ██║        ██╔████╔██║██████╔╝ █████╔╝       
  ╚██╔╝     ██║              ██║   ██║   ██║        ██║╚██╔╝██║██╔═══╝  ╚═══██╗       
   ██║      ██║              ██║   ╚██████╔╝        ██║ ╚═╝ ██║██║     ██████╔╝       
   ╚═╝      ╚═╝              ╚═╝    ╚═════╝         ╚═╝     ╚═╝╚═╝     ╚═════╝        
                                                                                      
██████╗  ██████╗ ██╗    ██║███╗   ██║██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
[green]Version:[/green] 2.9.2
[green]Author:[/green] Devdas Gupta
[green]GitHub:[/green] github.com/Devdas-gupta
[green]Description:[/green] A professional tool to download YouTube videos and playlists as MP3 or video with CLI and enhanced GUI support.
""", title="Welcome", border_style="blue"))

# CLI Menu
async def cli_menu():
    setup_tab_completion()
    while True:
        banner()
        table = Table(title="Menu Options", show_header=False, border_style="cyan")
        table.add_row("[1]", "Download YouTube Playlist")
        table.add_row("[2]", "Download Single Video")
        table.add_row("[3]", "Configure Settings")
        table.add_row("[4]", "Launch GUI")
        table.add_row("[5]", "Exit")
        console.print(table)
        
        choice = console.input("[bold cyan]Choose an option: [/bold cyan]").strip()
        if choice == '1':
            url = console.input("[bold green]🎵 Enter Playlist URL: [/bold green]").strip()
            download_type = console.input("[bold green]📥 Download as [1] MP3 or [2] Video? [/bold green]").strip()
            if download_type not in ['1', '2']:
                console.print("[red]⚠️ Invalid choice. Try again.[/red]\n")
                continue
            download_type = 'mp3' if download_type == '1' else 'video'
            output_path = console.input(f"[bold green]📂 Enter output directory (e.g., /home/username/{'songs' if download_type == 'mp3' else 'videos'}) or press Enter for ./{'downloads' if download_type == 'mp3' else 'videos'}: [/bold green]").strip()
            output_path = normalize_output_path(output_path, download_type)
            if download_type == 'mp3':
                quality = console.input("[bold green]🎚️ Choose audio quality (e.g., best, 192k, 128k, 64k) [default: best]: [/bold green]").strip() or 'best'
            else:
                quality = console.input("[bold green]🎚️ Choose video quality (e.g., 4K, 2K, 1080p, 720p, 480p, 360p, 144p) [default: best]: [/bold green]").strip() or 'best'
            await download_media(url, is_playlist=True, output_path=output_path, download_type=download_type, quality=quality)
        elif choice == '2':
            url = console.input("[bold green]🎵 Enter Video URL: [/bold green]").strip()
            download_type = console.input("[bold green]📥 Download as [1] MP3 or [2] Video? [/bold green]").strip()
            if download_type not in ['1', '2']:
                console.print("[red]⚠️ Invalid choice. Try again.[/red]\n")
                continue
            download_type = 'mp3' if download_type == '1' else 'video'
            output_path = console.input(f"[bold green]📂 Enter output directory (e.g., /home/username/{'songs' if download_type == 'mp3' else 'videos'}) or press Enter for ./{'downloads' if download_type == 'mp3' else 'videos'}: [/bold green]").strip()
            output_path = normalize_output_path(output_path, download_type)
            if download_type == 'mp3':
                quality = console.input("[bold green]🎚️ Choose audio quality (e.g., best, 192k, 128k, 64k) [default: best]: [/bold green]").strip() or 'best'
            else:
                quality = console.input("[bold green]🎚️ Choose video quality (e.g., 4K, 2K, 1080p, 720p, 480p, 360p, 144p) [default: best]: [/bold green]").strip() or 'best'
            await download_media(url, is_playlist=False, output_path=output_path, download_type=download_type, quality=quality)
        elif choice == '3':
            configure_settings()
        elif choice == '4':
            console.print("[yellow][+] Launching GUI...[/yellow]")
            gui_main()
            return
        elif choice == '5':
            console.print("[bold blue]👋 Goodbye![/bold blue]")
            return
        else:
            console.print("[red]⚠️ Invalid choice. Try again.[/red]\n")

# GUI Interface
def gui_main():
    if USE_TTKBOOTSTRAP:
        root = tbs.Window(themename="flatly")
    else:
        root = tk.Tk()
    root.title("YouTube to MP3 or Video Downloader")
    root.geometry("800x600")
    root.resizable(False, False)

    # Styling
    if USE_TTKBOOTSTRAP:
        style = tbs.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=12)
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))
    else:
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=12)
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))

    # Main frame
    if USE_TTKBOOTSTRAP:
        frame = tbs.Frame(root, padding="30")
    else:
        frame = ttk.Frame(root, padding="30")
    frame.pack(fill=tk.BOTH, expand=True)

    # Title label
    if USE_TTKBOOTSTRAP:
        tbs.Label(frame, text="YouTube Downloader", font=("Helvetica", 18, "bold"), bootstyle="primary").grid(row=0, column=0, columnspan=2, pady=15)
    else:
        ttk.Label(frame, text="YouTube Downloader", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

    # URL input
    if USE_TTKBOOTSTRAP:
        tbs.Label(frame, text="YouTube URL:").grid(row=1, column=0, sticky="w", pady=10)
        url_entry = tbs.Entry(frame, width=50)
    else:
        ttk.Label(frame, text="YouTube URL:").grid(row=1, column=0, sticky="w", pady=10)
        url_entry = ttk.Entry(frame, width=50)
    url_entry.grid(row=1, column=1, pady=5, sticky="ew")
    if USE_TTKBOOTSTRAP:
        ToolTip(url_entry, "Enter a YouTube video or playlist URL")

    # Download type selection
    if USE_TTKBOOTSTRAP:
        tbs.Label(frame, text="Download Type:").grid(row=2, column=0, sticky="w", pady=10)
        download_type_var = tk.StringVar(value="mp3")
        download_type_menu = tbs.Combobox(frame, textvariable=download_type_var, values=["MP3", "Video"], state="readonly")
    else:
        ttk.Label(frame, text="Download Type:").grid(row=2, column=0, sticky="w", pady=10)
        download_type_var = tk.StringVar(value="mp3")
        download_type_menu = ttk.Combobox(frame, textvariable=download_type_var, values=["MP3", "Video"], state="readonly")
    download_type_menu.grid(row=2, column=1, pady=5, sticky="ew")
    if USE_TTKBOOTSTRAP:
        ToolTip(download_type_menu, "Choose whether to download as MP3 audio or video")

    # Output directory
    if USE_TTKBOOTSTRAP:
        tbs.Label(frame, text="Output Directory:").grid(row=3, column=0, sticky="w", pady=10)
        output_entry = tbs.Entry(frame, width=50)
    else:
        ttk.Label(frame, text="Output Directory:").grid(row=3, column=0, sticky="w", pady=10)
        output_entry = ttk.Entry(frame, width=50)
    output_entry.insert(0, os.path.join(os.getcwd(), 'downloads'))
    output_entry.grid(row=3, column=1, pady=5, sticky="ew")
    if USE_TTKBOOTSTRAP:
        ToolTip(output_entry, "Enter output path or browse to select a folder")

    # File picker button
    def browse_folder():
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Output Folder")
        if folder:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, folder)

    if USE_TTKBOOTSTRAP:
        tbs.Button(frame, text="Browse Folder", command=browse_folder, bootstyle="primary").grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        if USE_TTKBOOTSTRAP:
            ToolTip(frame.children['!button'], "Browse to select output folder")
    else:
        ttk.Button(frame, text="Browse Folder", command=browse_folder).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    # Quality selection
    if USE_TTKBOOTSTRAP:
        tbs.Label(frame, text="Quality:").grid(row=5, column=0, sticky="w", pady=10)
        quality_var = tk.StringVar(value="best")
        quality_menu = tbs.Combobox(frame, textvariable=quality_var, state="readonly")
    else:
        ttk.Label(frame, text="Quality:").grid(row=5, column=0, sticky="w", pady=10)
        quality_var = tk.StringVar(value="best")
        quality_menu = ttk.Combobox(frame, textvariable=quality_var, state="readonly")
    quality_menu.grid(row=5, column=1, pady=5, sticky="ew")
    if USE_TTKBOOTSTRAP:
        ToolTip(quality_menu, "Select audio quality for MP3 or video resolution for Video")

    # Store last selected quality for each type
    last_quality = {'mp3': 'best', 'video': 'best'}

    def update_quality_options(*args):
        current_type = download_type_var.get().lower()
        if current_type == 'mp3':
            quality_menu['values'] = ["best", "192k", "128k", "64k"]
        else:
            quality_menu['values'] = ["4K", "2K", "1080p", "720p", "480p", "360p", "144p"]
        # Restore last selected quality for this type or default to 'best'
        quality_var.set(last_quality.get(current_type, 'best'))

    def save_quality_selection(*args):
        last_quality[download_type_var.get().lower()] = quality_var.get()

    download_type_var.trace("w", update_quality_options)
    quality_var.trace("w", save_quality_selection)
    update_quality_options()  # Initial setup

    # Playlist checkbox
    playlist_var = tk.BooleanVar()
    if USE_TTKBOOTSTRAP:
        tbs.Checkbutton(frame, text="Download as Playlist", variable=playlist_var, bootstyle="primary").grid(row=6, column=0, columnspan=2, pady=10, sticky="w")
        if USE_TTKBOOTSTRAP:
            ToolTip(frame.children['!checkbutton'], "Check to download entire playlist")
    else:
        ttk.Checkbutton(frame, text="Download as Playlist", variable=playlist_var).grid(row=6, column=0, columnspan=2, pady=10, sticky="w")

    # Status label
    if USE_TTKBOOTSTRAP:
        status_label = tbs.Label(frame, text="Ready", bootstyle="info", font=("Helvetica", 12))
    else:
        status_label = ttk.Label(frame, text="Ready", foreground="blue", font=("Helvetica", 12))
    status_label.grid(row=7, column=0, columnspan=2, pady=15)

    # Download button
    def start_download():
        url = url_entry.get().strip()
        output_path = normalize_output_path(output_entry.get().strip(), download_type_var.get().lower())
        quality = quality_var.get()
        is_playlist = playlist_var.get()
        download_type = download_type_var.get().lower()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        status_label.config(text="Downloading...", **({'bootstyle': "warning"} if USE_TTKBOOTSTRAP else {'foreground': "orange"}))
        root.update()
        asyncio.run(download_media(url, is_playlist, output_path, download_type=download_type, quality=quality, status_label=status_label))
        status_label.config(text="Download Complete!", **({'bootstyle': "success"} if USE_TTKBOOTSTRAP else {'foreground': "green"}))

    if USE_TTKBOOTSTRAP:
        tbs.Button(frame, text="Download", command=start_download, bootstyle="success-outline").grid(row=8, column=0, columnspan=2, pady=15, sticky="ew")
        if USE_TTKBOOTSTRAP:
            ToolTip(frame.children['!button2'], "Start downloading the YouTube content")
    else:
        ttk.Button(frame, text="Download", command=start_download).grid(row=8, column=0, columnspan=2, pady=15, sticky="ew")

    # Exit button
    if USE_TTKBOOTSTRAP:
        tbs.Button(frame, text="Exit", command=root.quit, bootstyle="danger-outline").grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")
        if USE_TTKBOOTSTRAP:
            ToolTip(frame.children['!button3'], "Close the application")
    else:
        ttk.Button(frame, text="Exit", command=root.quit).grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

    # Configure grid weights for responsiveness
    frame.columnconfigure(1, weight=1)

    root.mainloop()

# Configure settings
def configure_settings():
    console.print(Panel.fit("[bold yellow]⚙️ Settings Configuration[/bold yellow]", border_style="yellow"))
    default_quality = console.input("[bold green]🎚️ Set default audio quality (e.g., best, 192k, 128k, 64k): [/bold green]").strip() or "best"
    default_video_quality = console.input("[bold green]🎚️ Set default video quality (e.g., 4K, 2K, 1080p, 720p, 480p, 360p, 144p): [/bold green]").strip() or "best"
    max_parallel = console.input("[bold green]🔄 Set max parallel downloads (1-10, default 3): [/bold green]").strip() or "3"
    try:
        max_parallel = int(max_parallel)
        if not 1 <= max_parallel <= 10:
            raise ValueError
    except ValueError:
        console.print("[red]⚠️ Invalid number. Using default (3).[/red]")
        max_parallel = 3
    with open("config.ini", "w") as f:
        f.write(f"[Settings]\ndefault_quality={default_quality}\ndefault_video_quality={default_video_quality}\nmax_parallel={max_parallel}")
    console.print("[green]✅ Settings saved![/green]")

# Load settings
def load_settings():
    default_quality = "best"
    default_video_quality = "best"
    max_parallel = 3
    if os.path.exists("config.ini"):
        with open("config.ini", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "default_quality=" in line:
                    default_quality = line.split("=")[1].strip()
                if "default_video_quality=" in line:
                    default_video_quality = line.split("=")[1].strip()
                if "max_parallel=" in line:
                    max_parallel = int(line.split("=")[1].strip())
    return default_quality, default_video_quality, max_parallel

# Download with rich progress
async def download_with_progress(command, output_path, video_info, download_type, retries=3, status_label=None):
    error_count = 0
    for attempt in range(retries):
        try:
            os.makedirs(output_path, exist_ok=True)
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"[green]Downloading {video_info.get('title', 'video')} (Attempt {attempt+1}/{retries})...", total=None)
                process = await asyncio.create_subprocess_exec(
                    *command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT
                )
                async for line in process.stdout:
                    line = line.decode().strip()
                    if "HTTP Error 403: Forbidden" in line:
                        error_count += 1
                        if error_count <= 1:  # Show only the first 403 error
                            progress.update(task, description=f"[red]HTTP Error 403: Possible rate-limiting or restricted content[/red]")
                        continue
                    progress.update(task, advance=1, description=line[:80])
                    if status_label:
                        status_label.config(text=line[:80], **({'bootstyle': "warning"} if USE_TTKBOOTSTRAP else {'foreground': "orange"}))
                await process.wait()
                if process.returncode == 0:
                    console.print(f"[green]✅ Downloaded {video_info.get('title', 'video')}[/green]")
                    return True
                else:
                    console.print(f"[red]❌ Failed to download {video_info.get('title', 'video')} (Attempt {attempt+1}/{retries})[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error on attempt {attempt+1}/{retries}: {e}[/red]")
        if attempt < retries - 1:
            await asyncio.sleep(2)
    console.print(f"[red]❌ Failed to download {video_info.get('title', 'video')} after {retries} attempts[/red]")
    if status_label:
        status_label.config(text=f"Failed to download {video_info.get('title', 'video')}", **({'bootstyle': "danger"} if USE_TTKBOOTSTRAP else {'foreground': "red"}))
    return False

# Main download function
async def download_media(url, is_playlist, output_path, download_type, quality, status_label=None):
    default_quality, default_video_quality, max_parallel = load_settings()
    if not quality:
        quality = default_quality if download_type == 'mp3' else default_video_quality
    
    console.print(f"\n[yellow][+] Preparing download for {url}...[/yellow]\n")
    quality_map = {
        '4K': 'bestvideo[height<=?2160]+bestaudio/best',
        '2K': 'bestvideo[height<=?1440]+bestaudio/best',
        '1080p': 'bestvideo[height<=?1080]+bestaudio/best',
        '720p': 'bestvideo[height<=?720]+bestaudio/best',
        '480p': 'bestvideo[height<=?480]+bestaudio/best',
        '360p': 'bestvideo[height<=?360]+bestaudio/best',
        '144p': 'bestvideo[height<=?144]+bestaudio/best',
    }
    ydl_opts = {
        'format': 'bestaudio/best' if download_type == 'mp3' else quality_map.get(quality, 'bestvideo+bestaudio/best'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality if quality != 'best' else '0',
        }] if download_type == 'mp3' else [],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('firefox',),  # Use Firefox cookies to bypass 403
    }
    if download_type == 'video':
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            videos = info['entries'] if is_playlist else [info]
            total_videos = len(videos)
            console.print(f"[cyan][+] Found {total_videos} video(s) in {'playlist' if is_playlist else 'video'}[/cyan]")
            
            success_count = 0
            for i, video in enumerate(videos, 1):
                actual_quality = quality if download_type == 'mp3' else get_actual_quality(video, quality)
                console.print(f"[cyan][+] Processing video {i}/{total_videos}: {video.get('title', 'Unknown Title')} ({'Audio' if download_type == 'mp3' else f'Video at {actual_quality}'})[/cyan]")
                command = [
                    'yt-dlp',
                    '-x' if download_type == 'mp3' else '',
                ]
                if download_type == 'mp3':
                    command.extend(['--audio-format', 'mp3', '--audio-quality', quality if quality != 'best' else '0'])
                command.extend([
                    '--format', ydl_opts['format'],
                    '--output', os.path.join(output_path, '%(title)s.%(ext)s'),
                    '--quiet',
                    '--no-warnings',
                    '--cookies-from-browser', 'firefox',
                    video['webpage_url']
                ])
                if download_type == 'video':
                    command.extend(['--merge-output-format', 'mp4'])
                if is_playlist:
                    command.append('--yes-playlist')
                else:
                    command.append('--no-playlist')
                success = await download_with_progress(command, output_path, video, download_type, status_label=status_label)
                if success:
                    success_count += 1
            console.print(f"\n[green]✅ Completed: {success_count}/{total_videos} downloads successful![/green]")
            if status_label and success_count == total_videos:
                status_label.config(text="All downloads complete!", **({'bootstyle': "success"} if USE_TTKBOOTSTRAP else {'foreground': "green"}))
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if status_label:
            status_label.config(text=f"Error: {e}", **({'bootstyle': "danger"} if USE_TTKBOOTSTRAP else {'foreground': "red"}))

def get_actual_quality(video_info, selected_quality):
    if selected_quality == 'best':
        return 'best'
    quality_map = {'4K': 2160, '2K': 1440, '1080p': 1080, '720p': 720, '480p': 480, '360p': 360, '144p': 144}
    selected_height = quality_map.get(selected_quality, 2160)
    available_formats = video_info.get('formats', [])
    max_height = 0
    for fmt in available_formats:
        height = fmt.get('height', 0)
        if height and height <= selected_height and height > max_height:
            max_height = height
    for q, h in quality_map.items():
        if max_height >= h:
            return q
    return '144p'  # Fallback to lowest if no match

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="YouTube to MP3 or Video Downloader")
    parser.add_argument('--url', help="YouTube video or playlist URL")
    parser.add_argument('--type', choices=['mp3', 'video'], default='mp3', help="Download type: mp3 or video")
    parser.add_argument('--quality', default="best", help="Quality: for mp3 (best, 192k, 128k, 64k); for video (4K, 2K, 1080p, 720p, 480p, 360p, 144p)")
    parser.add_argument('--output', default=None, help="Output directory (e.g., /home/username/songs or /videos)")
    parser.add_argument('--playlist', action='store_true', help="Download as playlist")
    parser.add_argument('--gui', action='store_true', help="Launch GUI interface")
    return parser.parse_args()

# Run everything
if __name__ == "__main__":
    # Clear dependency cache to ensure fresh checks
    DEPENDENCY_CACHE.clear()
    # Dependency checks
    dependencies = [
        ('yt-dlp', f'{sys.executable} -m pip install yt-dlp', True),
        ('ffmpeg', 'sudo apt install ffmpeg -y', False),
        ('rich', f'{sys.executable} -m pip install rich', True),
        ('ttkbootstrap', f'{sys.executable} -m pip install ttkbootstrap', True)
    ]
    for pkg, cmd, is_pip in dependencies:
        check_and_install(pkg, cmd, is_pip)
    args = parse_args()
    if args.gui:
        gui_main()
    elif args.url:
        output_path = normalize_output_path(args.output, args.type)
        asyncio.run(download_media(args.url, args.playlist, output_path, download_type=args.type, quality=args.quality))
    else:
        asyncio.run(cli_menu())
