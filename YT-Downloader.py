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
import readline  # For tab completion

# Initialize rich console
console = Console()

# Cache for dependency checks
DEPENDENCY_CACHE = {}

# Check for required external tools
def check_and_install(package_name, install_cmd, pip_package=False):
    if package_name in DEPENDENCY_CACHE:
        return True
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
                sys.exit(1)
        else:
            console.print(f"[red][-] {package_name} is required. Exiting...[/red]")
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
def normalize_output_path(path):
    if not path or path.strip() == '':
        path = os.path.join(os.getcwd(), 'downloads')  # Default to ./downloads
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
                                                                                      
██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
[green]Version:[/green] 2.7.0
[green]Author:[/green] Devdas Gupta
[green]GitHub:[/green] github.com/Devdas-gupta
[green]Description:[/green] A professional tool to download YouTube videos and playlists as MP3s with CLI and GUI support.
""", title="Welcome", border_style="blue"))

# CLI Menu
async def cli_menu():
    setup_tab_completion()
    while True:
        banner()
        table = Table(title="Menu Options", show_header=False, border_style="cyan")
        table.add_row("[1]", "Download YouTube Playlist as MP3")
        table.add_row("[2]", "Download Single Video as MP3")
        table.add_row("[3]", "Configure Settings")
        table.add_row("[4]", "Launch GUI")
        table.add_row("[5]", "Exit")
        console.print(table)
        
        choice = console.input("[bold cyan]Choose an option: [/bold cyan]").strip()
        if choice == '1':
            url = console.input("[bold green]🎵 Enter Playlist URL: [/bold green]").strip()
            output_path = console.input("[bold green]📂 Enter output directory (e.g., /home/username/songs) or press Enter for ./downloads: [/bold green]").strip()
            output_path = normalize_output_path(output_path)
            await download_media(url, is_playlist=True, output_path=output_path)
        elif choice == '2':
            url = console.input("[bold green]🎵 Enter Video URL: [/bold green]").strip()
            output_path = console.input("[bold green]📂 Enter output directory (e.g., /home/username/songs) or press Enter for ./downloads: [/bold green]").strip()
            output_path = normalize_output_path(output_path)
            await download_media(url, is_playlist=False, output_path=output_path)
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
    root = tk.Tk()
    root.title("YouTube to MP3 Downloader")
    root.geometry("600x400")
    root.resizable(False, False)

    # Styling
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=10)
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 10))

    # Main frame
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # URL input
    ttk.Label(frame, text="YouTube URL:").pack(anchor="w")
    url_entry = ttk.Entry(frame, width=50)
    url_entry.pack(fill=tk.X, pady=5)

    # Output directory
    ttk.Label(frame, text="Output Directory (e.g., /home/username/songs):").pack(anchor="w")
    output_entry = ttk.Entry(frame, width=50)
    output_entry.insert(0, os.path.join(os.getcwd(), 'downloads'))
    output_entry.pack(fill=tk.X, pady=5)

    # File picker button
    def browse_folder():
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Output Folder")
        if folder:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, folder)

    ttk.Button(frame, text="Browse", command=browse_folder).pack(anchor="w", pady=5)

    # Quality selection
    ttk.Label(frame, text="Audio Quality:").pack(anchor="w")
    quality_var = tk.StringVar(value="best")
    quality_menu = ttk.Combobox(frame, textvariable=quality_var, values=["best", "192k", "128k", "64k"], state="readonly")
    quality_menu.pack(fill=tk.X, pady=5)

    # Playlist checkbox
    playlist_var = tk.BooleanVar()
    ttk.Checkbutton(frame, text="Download as Playlist", variable=playlist_var).pack(anchor="w", pady=5)

    # Status label
    status_label = ttk.Label(frame, text="Ready", foreground="blue")
    status_label.pack(anchor="w", pady=10)

    # Download button
    def start_download():
        url = url_entry.get().strip()
        output_path = normalize_output_path(output_entry.get().strip())
        quality = quality_var.get()
        is_playlist = playlist_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        status_label.config(text="Downloading...", foreground="orange")
        root.update()
        asyncio.run(download_media(url, is_playlist, output_path, quality=quality, status_label=status_label))
        status_label.config(text="Download Complete!", foreground="green")

    ttk.Button(frame, text="Download", command=start_download).pack(pady=10)

    # Exit button
    ttk.Button(frame, text="Exit", command=root.quit).pack(pady=5)

    root.mainloop()

# Configure settings
def configure_settings():
    console.print(Panel.fit("[bold yellow]⚙️ Settings Configuration[/bold yellow]", border_style="yellow"))
    default_quality = console.input("[bold green]🎚️ Set default audio quality (e.g., best, 192k, 128k, 64k): [/bold green]").strip() or "best"
    max_parallel = console.input("[bold green]🔄 Set max parallel downloads (1-10, default 3): [/bold green]").strip() or "3"
    try:
        max_parallel = int(max_parallel)
        if not 1 <= max_parallel <= 10:
            raise ValueError
    except ValueError:
        console.print("[red]⚠️ Invalid number. Using default (3).[/red]")
        max_parallel = 3
    with open("config.ini", "w") as f:
        f.write(f"[Settings]\ndefault_quality={default_quality}\nmax_parallel={max_parallel}")
    console.print("[green]✅ Settings saved![/green]")

# Load settings
def load_settings():
    default_quality = "best"
    max_parallel = 3
    if os.path.exists("config.ini"):
        with open("config.ini", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "default_quality=" in line:
                    default_quality = line.split("=")[1].strip()
                if "max_parallel=" in line:
                    max_parallel = int(line.split("=")[1].strip())
    return default_quality, max_parallel

# Download with rich progress
async def download_with_progress(command, output_path, video_info, retries=3, status_label=None):
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
                    progress.update(task, advance=1, description=line[:80])
                    if status_label:
                        status_label.config(text=line[:80], foreground="orange")
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
        status_label.config(text=f"Failed to download {video_info.get('title', 'video')}", foreground="red")
    return False

# Main download function
async def download_media(url, is_playlist, output_path, quality=None, status_label=None):
    default_quality, max_parallel = load_settings()
    if not quality:
        quality = console.input(f"[bold green]🎚️ Choose audio quality (e.g., best, 192k, 128k, 64k) [default: {default_quality}]: [/bold green]").strip() or default_quality
    
    console.print(f"\n[yellow][+] Preparing download for {url}...[/yellow]\n")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality if quality != 'best' else '0',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            videos = info['entries'] if is_playlist else [info]
            total_videos = len(videos)
            console.print(f"[cyan][+] Found {total_videos} video(s) in {'playlist' if is_playlist else 'video'}[/cyan]")
            
            success_count = 0
            for i, video in enumerate(videos, 1):
                console.print(f"[cyan][+] Processing video {i}/{total_videos}: {video.get('title', 'Unknown Title')}[/cyan]")
                command = [
                    'yt-dlp',
                    '-x',
                    '--audio-format', 'mp3',
                    '--audio-quality', quality,
                    '--output', os.path.join(output_path, '%(title)s.%(ext)s'),
                    '--quiet',
                    '--no-warnings',
                    video['webpage_url']
                ]
                if is_playlist:
                    command.append('--yes-playlist')
                else:
                    command.append('--no-playlist')
                success = await download_with_progress(command, output_path, video, status_label=status_label)
                if success:
                    success_count += 1
            console.print(f"\n[green]✅ Completed: {success_count}/{total_videos} downloads successful![/green]")
            if status_label and success_count == total_videos:
                status_label.config(text="All downloads complete!", foreground="green")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if status_label:
            status_label.config(text=f"Error: {e}", foreground="red")

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="YouTube to MP3 Downloader")
    parser.add_argument('--url', help="YouTube video or playlist URL")
    parser.add_argument('--quality', default="best", help="Audio quality (e.g., best, 192k, 128k)")
    parser.add_argument('--output', default="downloads", help="Output directory (e.g., /home/username/songs)")
    parser.add_argument('--playlist', action='store_true', help="Download as playlist")
    parser.add_argument('--gui', action='store_true', help="Launch GUI interface")
    return parser.parse_args()

# Run everything
if __name__ == "__main__":
    # Dependency checks
    dependencies = [
        ('yt-dlp', f'{sys.executable} -m pip install yt-dlp', True),
        ('ffmpeg', 'sudo apt install ffmpeg -y', False),
        ('rich', f'{sys.executable} -m pip install rich', True)
    ]
    for pkg, cmd, is_pip in dependencies:
        check_and_install(pkg, cmd, is_pip)

    args = parse_args()
    if args.gui:
        gui_main()
    elif args.url:
        asyncio.run(download_media(args.url, args.playlist, normalize_output_path(args.output), quality=args.quality))
    else:
        asyncio.run(cli_menu())