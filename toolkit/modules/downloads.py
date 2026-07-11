from toolkit.utils import Colors
import os
import shutil
import subprocess

def check_ytdlp():
    if not shutil.which("yt-dlp"):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} yt-dlp is not installed or not in PATH.")
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} Please run: pip install yt-dlp")
        return False
    return True

def download_video(url, quality="best"):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Video from: {url}")
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} Quality: {quality}")
    
    args = ["yt-dlp", url]
    if quality == "best":
        args.extend(["-f", "bestvideo+bestaudio/best"])
    elif quality == "4k":
        args.extend(["-f", "bestvideo[height<=2160]+bestaudio/best"])
    elif quality == "8k":
        args.extend(["-f", "bestvideo[height<=4320]+bestaudio/best"])
    
    try:
        subprocess.run(args)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Download complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Download failed: {e}")

def download_audio(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Audio from: {url}")
    args = ["yt-dlp", "-x", "--audio-format", "mp3", url]
    try:
        subprocess.run(args)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Audio download complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Download failed: {e}")

def download_playlist(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Playlist from: {url}")
    args = ["yt-dlp", "--yes-playlist", url]
    try:
        subprocess.run(args)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Playlist download complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Download failed: {e}")

def download_thumbnail(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Thumbnail from: {url}")
    args = ["yt-dlp", "--write-thumbnail", "--skip-download", url]
    try:
        subprocess.run(args)
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Thumbnail download complete.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Download failed: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [5] DOWNLOADS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} YT-DLP Status")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Download Video")
        print(f"{Colors.GREEN}[3]{Colors.RESET} Download Playlist")
        print(f"{Colors.GREEN}[4]{Colors.RESET} Download Audio")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Download Thumbnail")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Download 4K Video")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Download 8K Video")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Subtitles")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Cookies")
        print(f"{Colors.GREEN}[10]{Colors.RESET} FFmpeg Status")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            if check_ytdlp():
                subprocess.run(["yt-dlp", "--version"])
        elif choice == '2':
            url = input("Enter URL: ").strip()
            if url: download_video(url, "best")
        elif choice == '3':
            url = input("Enter Playlist URL: ").strip()
            if url: download_playlist(url)
        elif choice == '4':
            url = input("Enter URL: ").strip()
            if url: download_audio(url)
        elif choice == '5':
            url = input("Enter URL: ").strip()
            if url: download_thumbnail(url)
        elif choice == '6':
            url = input("Enter URL: ").strip()
            if url: download_video(url, "4k")
        elif choice == '7':
            url = input("Enter URL: ").strip()
            if url: download_video(url, "8k")
        elif choice == '8':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Subtitles extraction coming soon...")
        elif choice == '9':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Cookies support coming soon...")
        elif choice == '10':
            if shutil.which("ffmpeg"):
                print("[✓] FFmpeg is installed.")
                subprocess.run(["ffmpeg", "-version"])
            else:
                print("[x] FFmpeg is NOT installed. Many yt-dlp features will be limited.")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
