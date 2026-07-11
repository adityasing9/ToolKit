from toolkit.utils import Colors
import os
import subprocess
import shutil
from PIL import Image

def get_temp_file(suffix):
    import tempfile
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
    os.close(temp_fd)
    return temp_path

def check_ffmpeg():
    """Verify if FFmpeg is in the system PATH. If not, suggest winget installation."""
    if shutil.which("ffmpeg"):
        return True
    
    print(f"\n{Colors.YELLOW}[WARNING]{Colors.RESET} FFmpeg is not installed or not in your PATH.")
    print("FFmpeg is required to perform Audio and Video conversion.")
    confirm = input("Would you like to automatically install it via Winget? (y/n): ").strip().lower()
    if confirm == 'y':
        print(f"\n[INFO] Starting FFmpeg installation via Winget...")
        try:
            res = subprocess.run(["winget", "install", "Gyan.FFmpeg"], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} FFmpeg installed successfully! Please restart the terminal to apply PATH changes.")
                return False # Need restart
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} Winget installation failed: {res.stderr or res.stdout}")
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not launch Winget: {e}")
    return False

def image_optimizer():
    print(f"\n{Colors.CYAN}--- Image Optimizer ---{Colors.RESET}")
    filepath = input("Enter image path (PNG, JPG, JPEG, WEBP): ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    try:
        quality = input("Enter optimization quality (1-100, default 85): ").strip()
        q_val = int(quality) if quality.isdigit() else 85
        
        img = Image.open(filepath)
        dir_name, file_name = os.path.split(filepath)
        base_name, ext = os.path.splitext(file_name)
        dest_path = os.path.join(dir_name, f"{base_name}_optimized{ext}")
        
        # Save optimized image
        if img.mode in ('RGBA', 'P') and ext.lower() in ('.jpg', '.jpeg'):
            img = img.convert('RGB')
            
        img.save(dest_path, optimize=True, quality=q_val)
        
        original_size = os.path.getsize(filepath) / 1024
        new_size = os.path.getsize(dest_path) / 1024
        
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Image optimized successfully!")
        print(f"  Saved to: {dest_path}")
        print(f"  Original Size: {original_size:.2f} KB")
        print(f"  Optimized Size: {new_size:.2f} KB (Reduced by {((original_size - new_size)/original_size)*100:.1f}%)")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to optimize image: {e}")

def resize_image():
    print(f"\n{Colors.CYAN}--- Resize Image ---{Colors.RESET}")
    filepath = input("Enter image path: ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    try:
        img = Image.open(filepath)
        print(f"Current Dimensions: {img.width}x{img.height} px")
        
        w_in = input("Enter new width (or leave blank to scale proportionally): ").strip()
        h_in = input("Enter new height (or leave blank to scale proportionally): ").strip()
        
        if not w_in and not h_in:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Width and/or height must be specified.")
            return
            
        if w_in and not h_in:
            width = int(w_in)
            height = int((width / img.width) * img.height)
        elif h_in and not w_in:
            height = int(h_in)
            width = int((height / img.height) * img.width)
        else:
            width = int(w_in)
            height = int(h_in)
            
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
        dir_name, file_name = os.path.split(filepath)
        base_name, ext = os.path.splitext(file_name)
        dest_path = os.path.join(dir_name, f"{base_name}_resized{ext}")
        
        resized_img.save(dest_path)
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Image resized to {width}x{height} px!")
        print(f"  Saved to: {dest_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to resize image: {e}")

def pdf_merge():
    print(f"\n{Colors.CYAN}--- PDF Merge ---{Colors.RESET}")
    print("Enter PDF file paths to merge in order (separated by commas):")
    paths_in = input("Paths: ").strip()
    if not paths_in:
        return
        
    paths = [p.strip().strip('"').strip("'") for p in paths_in.split(",")]
    valid_paths = [p for p in paths if os.path.exists(p)]
    
    if len(valid_paths) < 2:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Please provide at least 2 valid PDF file paths.")
        return
        
    dest_path = input("Enter output PDF path (e.g. combined.pdf): ").strip().strip('"').strip("'")
    if not dest_path:
        dest_path = "merged_output.pdf"
        
    try:
        from pypdf import PdfMerger
        merger = PdfMerger()
        for path in valid_paths:
            print(f" Adding: {path}")
            merger.append(path)
            
        merger.write(dest_path)
        merger.close()
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} PDFs merged successfully!")
        print(f" Saved to: {os.path.abspath(dest_path)}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to merge PDFs: {e}")

def pdf_split():
    print(f"\n{Colors.CYAN}--- PDF Split ---{Colors.RESET}")
    filepath = input("Enter PDF path to split: ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        print(f"Total Pages in PDF: {total_pages}")
        
        print("\nChoose Split Method:")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Split every single page into separate files")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Extract a specific page range (e.g. 1-3, 5)")
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        
        dir_name, file_name = os.path.split(filepath)
        base_name, ext = os.path.splitext(file_name)
        
        if choice == '1':
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                output_name = os.path.join(dir_name, f"{base_name}_page_{i+1}.pdf")
                with open(output_name, "wb") as f:
                    writer.write(f)
            print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Split complete! Saved {total_pages} files in: {dir_name}")
            
        elif choice == '2':
            range_in = input("Enter pages to extract (e.g. 1-3, 5): ").strip()
            if not range_in:
                return
            
            pages_to_extract = set()
            for part in range_in.split(","):
                part = part.strip()
                if "-" in part:
                    start, end = part.split("-")
                    pages_to_extract.update(range(int(start), int(end) + 1))
                else:
                    pages_to_extract.add(int(part))
            
            writer = PdfWriter()
            extracted_count = 0
            for page_num in sorted(list(pages_to_extract)):
                if 1 <= page_num <= total_pages:
                    writer.add_page(reader.pages[page_num - 1])
                    extracted_count += 1
                    
            if extracted_count > 0:
                output_name = os.path.join(dir_name, f"{base_name}_extracted.pdf")
                with open(output_name, "wb") as f:
                    writer.write(f)
                print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Extracted {extracted_count} pages successfully!")
                print(f" Saved to: {output_name}")
            else:
                print(f"{Colors.RED}[ERROR]{Colors.RESET} No pages matched your range.")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to split PDF: {e}")

def run_ocr():
    print(f"\n{Colors.CYAN}--- Offline OCR (Text Extraction) ---{Colors.RESET}")
    print("[INFO] Utilizing native Windows OcrEngine (no internet required).")
    filepath = input("Enter image path (PNG, JPG, JPEG, BMP): ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    print("\n[INFO] Extracting text, please wait...")
    
    # PowerShell WinRT Ocr script payload
    ps_script = f"""
    [CmdletBinding()]
    param([string]$ImagePath)
    try {{
        Add-Type -AssemblyName System.Runtime.WindowsRuntime -ErrorAction Stop
        $asyncHelper = [System.WindowsRuntimeSystemExtensions]
        
        $file = Get-Item -LiteralPath $ImagePath
        $stream = [Windows.Storage.Streams.RandomAccessStreamReference]::CreateFromFile($file)
        $asyncOperation = $stream.OpenReadAsync()
        $streamResult = $asyncHelper.GetAwaiter($asyncOperation).GetResult()
        
        $decoderAsync = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($streamResult)
        $decoder = $asyncHelper.GetAwaiter($decoderAsync).GetResult()
        $softwareBitmapAsync = $decoder.GetSoftwareBitmapAsync()
        $softwareBitmap = $asyncHelper.GetAwaiter($softwareBitmapAsync).GetResult()
        
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
        if (-not $engine) {{
            Write-Error "Could not create native Windows OcrEngine. Check system language packages."
            exit 1
        }}
        $ocrAsync = $engine.RecognizeAsync($softwareBitmap)
        $ocrResult = $asyncHelper.GetAwaiter($ocrAsync).GetResult()
        
        Write-Output $ocrResult.Text
    }} catch {{
        Write-Error $_.Exception.Message
        exit 1
    }}
    """
    
    # Save script payload temporarily
    temp_script = get_temp_file(".ps1")
    try:
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(ps_script)
            
        res = subprocess.run([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", temp_script, "-ImagePath", os.path.abspath(filepath)
        ], capture_output=True, text=True, errors="ignore")
        
        if res.returncode == 0 and res.stdout.strip():
            print(f"\n{Colors.GREEN}================== EXTRACTED TEXT =================={Colors.RESET}")
            print(res.stdout.strip())
            print(f"{Colors.GREEN}===================================================={Colors.RESET}")
            
            save = input("\nWould you like to save this text to a file? (y/n): ").strip().lower()
            if save == 'y':
                dest = input("Enter output path (default: ocr_result.txt): ").strip().strip('"').strip("'")
                if not dest:
                    dest = "ocr_result.txt"
                with open(dest, "w", encoding="utf-8") as out_f:
                    out_f.write(res.stdout.strip())
                print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Saved to: {os.path.abspath(dest)}")
        else:
            err = res.stderr.strip() if res.stderr else "No text could be extracted or identified."
            print(f"{Colors.RED}[ERROR] OCR Failed:{Colors.RESET} {err}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} OCR wrapper execution failed: {e}")
    finally:
        if os.path.exists(temp_script):
            os.remove(temp_script)

def audio_converter():
    print(f"\n{Colors.CYAN}--- Audio Converter ---{Colors.RESET}")
    if not check_ffmpeg():
        return
        
    filepath = input("Enter input audio file: ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    print("\nFormats: mp3, wav, aac, flac, m4a, ogg")
    target_format = input("Enter target format (e.g. mp3): ").strip().lower().replace(".", "")
    if not target_format:
        return
        
    dir_name, file_name = os.path.split(filepath)
    base_name, _ = os.path.splitext(file_name)
    dest_path = os.path.join(dir_name, f"{base_name}.{target_format}")
    
    print(f"\n[INFO] Converting audio to {target_format} format...")
    try:
        subprocess.run(["ffmpeg", "-y", "-i", filepath, dest_path])
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Conversion complete!")
        print(f" Saved to: {dest_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to convert audio: {e}")

def video_converter():
    print(f"\n{Colors.CYAN}--- Video Converter ---{Colors.RESET}")
    if not check_ffmpeg():
        return
        
    filepath = input("Enter input video file: ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    print("\nFormats: mp4, mkv, avi, webm, flv, gif")
    target_format = input("Enter target format (e.g. mp4): ").strip().lower().replace(".", "")
    if not target_format:
        return
        
    dir_name, file_name = os.path.split(filepath)
    base_name, _ = os.path.splitext(file_name)
    dest_path = os.path.join(dir_name, f"{base_name}.{target_format}")
    
    print(f"\n[INFO] Converting video to {target_format} format...")
    try:
        subprocess.run(["ffmpeg", "-y", "-i", filepath, dest_path])
        print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Conversion complete!")
        print(f" Saved to: {dest_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to convert video: {e}")

def metadata_viewer():
    print(f"\n{Colors.CYAN}--- Metadata Viewer ---{Colors.RESET}")
    filepath = input("Enter file path: ").strip().strip('"').strip("'")
    if not filepath or not os.path.exists(filepath):
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid file path.")
        return
        
    try:
        # File Statistics
        stats = os.stat(filepath)
        import datetime
        print(f"\n{Colors.BOLD}{Colors.YELLOW}[File Properties]{Colors.RESET}")
        print(f"  Name:         {os.path.basename(filepath)}")
        print(f"  Path:         {os.path.abspath(filepath)}")
        print(f"  Size:         {stats.st_size / 1024:.2f} KB ({stats.st_size} bytes)")
        print(f"  Created:      {datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Modified:     {datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Image Specific EXIF Metadata
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.tiff', '.webp'):
            img = Image.open(filepath)
            print(f"\n{Colors.BOLD}{Colors.YELLOW}[Image Specifications]{Colors.RESET}")
            print(f"  Format:       {img.format}")
            print(f"  Dimensions:   {img.width}x{img.height} px")
            print(f"  Color Mode:   {img.mode}")
            
            exif = img._getexif() if hasattr(img, '_getexif') else None
            if exif:
                from PIL.ExifTags import TAGS
                print(f"\n{Colors.BOLD}{Colors.YELLOW}[EXIF Metadata]{Colors.RESET}")
                for tag, value in exif.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded not in ('MakerNote', 'UserComment', 'PrintImageMatching'):
                        print(f"  {decoded:<20}: {value}")
                        
        # PDF Specific Metadata
        elif ext == '.pdf':
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            print(f"\n{Colors.BOLD}{Colors.YELLOW}[PDF Specifications]{Colors.RESET}")
            print(f"  Total Pages:  {len(reader.pages)}")
            
            info = reader.metadata
            if info:
                print(f"\n{Colors.BOLD}{Colors.YELLOW}[PDF Document Metadata]{Colors.RESET}")
                for key, val in info.items():
                    clean_key = key.replace("/", "")
                    print(f"  {clean_key:<15}: {val}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to read metadata: {e}")

def show_menu():
    while True:
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [18] MEDIA TOOLS{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Image Optimizer")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Resize Image")
        print(f"{Colors.GREEN}[3]{Colors.RESET} PDF Merge")
        print(f"{Colors.GREEN}[4]{Colors.RESET} PDF Split")
        print(f"{Colors.GREEN}[5]{Colors.RESET} Offline OCR (Extract Text from Image)")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Audio Converter")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Video Converter")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Metadata & EXIF Viewer")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            image_optimizer()
        elif choice == '2':
            resize_image()
        elif choice == '3':
            pdf_merge()
        elif choice == '4':
            pdf_split()
        elif choice == '5':
            run_ocr()
        elif choice == '6':
            audio_converter()
        elif choice == '7':
            video_converter()
        elif choice == '8':
            metadata_viewer()
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
