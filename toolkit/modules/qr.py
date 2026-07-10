import os
import qrcode
import urllib.parse

def print_qr_to_console(data):
    """Generates and prints a QR code directly to the terminal."""
    print(f"\n[INFO] Generating QR Code for: {data}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    # Print ascii to terminal
    qr.print_ascii(invert=True)
    print("\n[SUCCESS] QR Code generated successfully.")

def save_qr_to_file(data, filename="qrcode.png"):
    """Generates and saves a QR code as a PNG."""
    print(f"\n[INFO] Saving QR Code for: {data}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    save_path = os.path.join(os.getcwd(), filename)
    try:
        img.save(save_path)
        print(f"[SUCCESS] QR Code saved to {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save QR code: {e}")

def qr_from_text():
    text = input("Enter text for QR Code: ").strip()
    if text:
        print_qr_to_console(text)

def qr_from_url():
    url = input("Enter URL for QR Code: ").strip()
    if url:
        if not url.startswith("http"):
            url = "https://" + url
        print_qr_to_console(url)

def wifi_qr():
    print("\n--- Generate WiFi QR Code ---")
    ssid = input("SSID (Network Name): ").strip()
    password = input("Password: ").strip()
    encryption = input("Encryption (WEP/WPA/blank for None): ").strip().upper()
    
    if not ssid:
        print("[ERROR] SSID is required.")
        return
        
    if not encryption:
        wifi_string = f"WIFI:T:nopass;S:{ssid};;"
    else:
        wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        
    print_qr_to_console(wifi_string)

def email_qr():
    print("\n--- Generate Email QR Code ---")
    email = input("Email Address: ").strip()
    subject = input("Subject: ").strip()
    body = input("Body: ").strip()
    
    if not email:
        return
        
    mailto_url = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    print_qr_to_console(mailto_url)

def phone_qr():
    print("\n--- Generate Phone QR Code ---")
    phone = input("Phone Number: ").strip()
    if phone:
        print_qr_to_console(f"tel:{phone}")

def save_png_prompt():
    print("\n--- Save QR as PNG ---")
    data = input("Enter data to encode: ").strip()
    if not data:
        return
    filename = input("Enter filename (default: qrcode.png): ").strip()
    if not filename:
        filename = "qrcode.png"
    if not filename.endswith(".png"):
        filename += ".png"
    save_qr_to_file(data, filename)

def show_menu():
    while True:
        print("\n=============================================================")
        print("              [10] QR / BARCODE")
        print("=============================================================")
        print("[1] Generate QR")
        print("[2] Generate Barcode")
        print("[3] QR from Text")
        print("[4] QR from URL")
        print("[5] WiFi QR")
        print("[6] Email QR")
        print("[7] Phone QR")
        print("[8] Scan QR")
        print("[9] Save PNG")
        print("[10] SVG Export")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            qr_from_text()
        elif choice == '2':
            print("[INFO] Barcode generation coming soon...")
        elif choice == '3':
            qr_from_text()
        elif choice == '4':
            qr_from_url()
        elif choice == '5':
            wifi_qr()
        elif choice == '6':
            email_qr()
        elif choice == '7':
            phone_qr()
        elif choice == '8':
            print("[INFO] Scanning QR codes via webcam coming soon...")
        elif choice == '9':
            save_png_prompt()
        elif choice == '10':
            print("[INFO] SVG Export coming soon...")
        else:
            print("[ERROR] Invalid choice.")
