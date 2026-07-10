import os
import shutil
import hashlib
import subprocess
import zipfile

def set_hidden(path, hide=True):
    if not os.path.exists(path):
        print(f"[ERROR] Path does not exist: {path}")
        return
    try:
        if hide:
            subprocess.run(["attrib", "+h", path])
            print(f"[SUCCESS] {path} is now hidden.")
        else:
            subprocess.run(["attrib", "-h", path])
            print(f"[SUCCESS] {path} is now unhidden.")
    except Exception as e:
        print(f"[ERROR] Failed to change attributes: {e}")

def get_folder_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(bytes):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor
    return "0B"

def calculate_folder_size():
    folder = input("Enter folder path: ").strip()
    if os.path.isdir(folder):
        print("[INFO] Calculating...")
        size = get_folder_size(folder)
        print(f"\n[SUCCESS] Size of {folder}: {format_size(size)}")
    else:
        print("[ERROR] Invalid folder path.")

def find_large_files():
    folder = input("Enter folder path to search: ").strip()
    if not os.path.isdir(folder):
        print("[ERROR] Invalid folder path.")
        return
    min_mb = input("Enter minimum file size in MB (default 100): ").strip()
    min_mb = int(min_mb) if min_mb.isdigit() else 100
    min_bytes = min_mb * 1024 * 1024
    
    print(f"\n[INFO] Searching for files > {min_mb}MB in {folder}...")
    found = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
                if size > min_bytes:
                    found.append((fp, size))
            except:
                pass
                
    found.sort(key=lambda x: x[1], reverse=True)
    if not found:
        print(f"[INFO] No files > {min_mb}MB found.")
        return
        
    print(f"\n{'Size':<10} | Path")
    print("-" * 60)
    for fp, size in found[:50]:  # Top 50
        print(f"{format_size(size):<10} | {fp}")

def compress_folder():
    folder = input("Enter folder to compress: ").strip()
    if not os.path.isdir(folder):
        print("[ERROR] Invalid folder path.")
        return
    dest = input("Enter destination ZIP filename (e.g. backup.zip): ").strip()
    if not dest:
        return
    if not dest.endswith('.zip'):
        dest += '.zip'
        
    print(f"[INFO] Compressing {folder} into {dest}...")
    try:
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folder))
                    zipf.write(file_path, arcname)
        print("[SUCCESS] Compression complete.")
    except Exception as e:
        print(f"[ERROR] Compression failed: {e}")

def extract_zip():
    zip_path = input("Enter ZIP file path: ").strip()
    if not os.path.isfile(zip_path) or not zip_path.endswith('.zip'):
        print("[ERROR] Invalid ZIP file.")
        return
    dest = input("Enter extraction folder (default current): ").strip() or "."
    print(f"[INFO] Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(dest)
        print("[SUCCESS] Extraction complete.")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")

def calculate_file_hash():
    file_path = input("Enter file path: ").strip()
    if not os.path.isfile(file_path):
        print("[ERROR] Invalid file.")
        return
        
    print("\n[INFO] Calculating hashes...")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            print(f"MD5:    {hashlib.md5(data).hexdigest()}")
            print(f"SHA1:   {hashlib.sha1(data).hexdigest()}")
            print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [6] FILE & FOLDER")
        print("=============================================================")
        print("[1] Hide File")
        print("[2] Unhide File")
        print("[3] Hide Folder")
        print("[4] Unhide Folder")
        print("[5] Secure Folder")
        print("[6] Unlock Folder")
        print("[7] Encrypt Folder")
        print("[8] Decrypt Folder")
        print("[9] Find Large Files")
        print("[10] Duplicate Finder")
        print("[11] Folder Size")
        print("[12] Rename Multiple Files")
        print("[13] Compress (ZIP)")
        print("[14] Extract (ZIP)")
        print("[15] File Hash")
        print("[16] Secure Delete")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            path = input("Enter file path to hide: ").strip()
            if path: set_hidden(path, True)
        elif choice == '2':
            path = input("Enter file path to unhide: ").strip()
            if path: set_hidden(path, False)
        elif choice == '3':
            path = input("Enter folder path to hide: ").strip()
            if path: set_hidden(path, True)
        elif choice == '4':
            path = input("Enter folder path to unhide: ").strip()
            if path: set_hidden(path, False)
        elif choice == '5':
            print("[INFO] Secure Folder (Password Protection) coming soon...")
        elif choice == '6':
            print("[INFO] Unlock Folder coming soon...")
        elif choice == '7':
            print("[INFO] Encrypt Folder coming soon...")
        elif choice == '8':
            print("[INFO] Decrypt Folder coming soon...")
        elif choice == '9':
            find_large_files()
        elif choice == '10':
            print("[INFO] Duplicate Finder coming soon...")
        elif choice == '11':
            calculate_folder_size()
        elif choice == '12':
            print("[INFO] Mass Renamer coming soon...")
        elif choice == '13':
            compress_folder()
        elif choice == '14':
            extract_zip()
        elif choice == '15':
            calculate_file_hash()
        elif choice == '16':
            print("[INFO] Secure Delete (Shredding) coming soon...")
        else:
            print("[ERROR] Invalid choice.")
