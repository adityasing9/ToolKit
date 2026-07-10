from toolkit.utils import Colors
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
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} QR Code saved to {save_path}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to save QR code: {e}")

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
    print(f"\n{Colors.CYAN}--- Generate WiFi QR Code ---{Colors.RESET}")
    ssid = input("SSID (Network Name): ").strip()
    password = input("Password: ").strip()
    encryption = input("Encryption (WEP/WPA/blank for None): ").strip().upper()
    
    if not ssid:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} SSID is required.")
        return
        
    if not encryption:
        wifi_string = f"WIFI:T:nopass;S:{ssid};;"
    else:
        wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        
    print_qr_to_console(wifi_string)

def email_qr():
    print(f"\n{Colors.CYAN}--- Generate Email QR Code ---{Colors.RESET}")
    email = input("Email Address: ").strip()
    subject = input("Subject: ").strip()
    body = input("Body: ").strip()
    
    if not email:
        return
        
    mailto_url = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    print_qr_to_console(mailto_url)

def phone_qr():
    print(f"\n{Colors.CYAN}--- Generate Phone QR Code ---{Colors.RESET}")
    phone = input("Phone Number: ").strip()
    if phone:
        print_qr_to_console(f"tel:{phone}")

def save_png_prompt():
    print(f"\n{Colors.CYAN}--- Save QR as PNG ---{Colors.RESET}")
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
        print(f"\n{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}              [10] QR / BARCODE{Colors.RESET}")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.RESET} Generate QR")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Generate Barcode")
        print(f"{Colors.GREEN}[3]{Colors.RESET} QR from Text")
        print(f"{Colors.GREEN}[4]{Colors.RESET} QR from URL")
        print(f"{Colors.GREEN}[5]{Colors.RESET} WiFi QR")
        print(f"{Colors.GREEN}[6]{Colors.RESET} Email QR")
        print(f"{Colors.GREEN}[7]{Colors.RESET} Phone QR")
        print(f"{Colors.GREEN}[8]{Colors.RESET} Scan QR")
        print(f"{Colors.GREEN}[9]{Colors.RESET} Save PNG")
        print(f"{Colors.GREEN}[10]{Colors.RESET} SVG Export")
        print(f"{Colors.GREEN}[0]{Colors.RESET} Back to Main Menu")
        print(f"{Colors.CYAN}============================================================={Colors.RESET}")
        
        choice = input(f"{Colors.MAGENTA}Select > {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice == '1':
            qr_from_text()
        elif choice == '2':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Barcode generation coming soon...")
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
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} Scanning QR codes via webcam coming soon...")
        elif choice == '9':
            save_png_prompt()
        elif choice == '10':
            print(f"{Colors.BLUE}[INFO]{Colors.RESET} SVG Export coming soon...")
        else:
            print(f"{Colors.RED}[ERROR]{Colors.RESET} Invalid choice.")
