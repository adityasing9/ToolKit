def show_menu():
    while True:
        print("\n=============================================================")
        print("              [7] DOWNLOADS")
        print("=============================================================")
        print("[1] YT-DLP")
        print("[2] Download Video")
        print("[3] Download Playlist")
        print("[4] Download Audio")
        print("[5] Download Thumbnail")
        print("[6] Ultra Quality")
        print("[7] 4K")
        print("[8] 8K")
        print("[9] Subtitles")
        print("[10] Cookies")
        print("[11] FFmpeg")
        print("[12] Download Progress")
        print("[13] History")
        print("[0] Back to Main Menu")
        print("=============================================================")
        
        choice = input("Select > ").strip()
        if choice == '0':
            break
        elif choice == '1':
            print("[INFO] YT-DLP coming soon...")
        elif choice == '2':
            print("[INFO] Download Video coming soon...")
        elif choice == '3':
            print("[INFO] Download Playlist coming soon...")
        elif choice == '4':
            print("[INFO] Download Audio coming soon...")
        elif choice == '5':
            print("[INFO] Download Thumbnail coming soon...")
        elif choice == '6':
            print("[INFO] Ultra Quality coming soon...")
        elif choice == '7':
            print("[INFO] 4K coming soon...")
        elif choice == '8':
            print("[INFO] 8K coming soon...")
        elif choice == '9':
            print("[INFO] Subtitles coming soon...")
        elif choice == '10':
            print("[INFO] Cookies coming soon...")
        elif choice == '11':
            print("[INFO] FFmpeg coming soon...")
        elif choice == '12':
            print("[INFO] Download Progress coming soon...")
        elif choice == '13':
            print("[INFO] History coming soon...")
        else:
            print("[ERROR] Invalid choice.")
