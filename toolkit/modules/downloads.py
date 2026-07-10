import os
import shutil
import subprocess

def check_ytdlp():
    if not shutil.which("yt-dlp"):
        print("[ERROR] yt-dlp is not installed or not in PATH.")
        print("[INFO] Please run: pip install yt-dlp")
        return False
    return True

def download_video(url, quality="best"):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Video from: {url}")
    print(f"[INFO] Quality: {quality}")
    
    args = ["yt-dlp", url]
    if quality == "best":
        args.extend(["-f", "bestvideo+bestaudio/best"])
    elif quality == "4k":
        args.extend(["-f", "bestvideo[height<=2160]+bestaudio/best"])
    elif quality == "8k":
        args.extend(["-f", "bestvideo[height<=4320]+bestaudio/best"])
    
    try:
        subprocess.run(args)
        print("[SUCCESS] Download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

def download_audio(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Audio from: {url}")
    args = ["yt-dlp", "-x", "--audio-format", "mp3", url]
    try:
        subprocess.run(args)
        print("[SUCCESS] Audio download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

def download_playlist(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Playlist from: {url}")
    args = ["yt-dlp", "--yes-playlist", url]
    try:
        subprocess.run(args)
        print("[SUCCESS] Playlist download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

def download_thumbnail(url):
    if not check_ytdlp():
        return
    print(f"\n[INFO] Downloading Thumbnail from: {url}")
    args = ["yt-dlp", "--write-thumbnail", "--skip-download", url]
    try:
        subprocess.run(args)
        print("[SUCCESS] Thumbnail download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [7] DOWNLOADS")
        print("=============================================================")
        print("[1] YT-DLP Status")
        print("[2] Download Video")
        print("[3] Download Playlist")
        print("[4] Download Audio")
        print("[5] Download Thumbnail")
        print("[6] Download 4K Video")
        print("[7] Download 8K Video")
        print("[8] Subtitles")
        print("[9] Cookies")
        print("[10] FFmpeg Status")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
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
            print("[INFO] Subtitles extraction coming soon...")
        elif choice == '9':
            print("[INFO] Cookies support coming soon...")
        elif choice == '10':
            if shutil.which("ffmpeg"):
                print("[✓] FFmpeg is installed.")
                subprocess.run(["ffmpeg", "-version"])
            else:
                print("[x] FFmpeg is NOT installed. Many yt-dlp features will be limited.")
        else:
            print("[ERROR] Invalid choice.")
