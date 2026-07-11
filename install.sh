#!/bin/bash

# ToolKit Linux Installer & Manager

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}==============================================${RESET}"
    echo -e "         Toolkit CLI Manager (Linux/Bash)      "
    echo -e "${CYAN}==============================================${RESET}"
    echo "1) Install / Update & Run Linux Toolkit"
    echo "2) Run Linux Toolkit (If already installed)"
    echo "3) Run Portable (No Installation / Temp Dir)"
    echo "4) Uninstall & Remove Linux Toolkit Completely"
    echo "5) Exit"
    echo -e "${CYAN}==============================================${RESET}"
}

check_prerequisites() {
    if ! command -v git &> /dev/null; then
        echo -e "${RED}[ERROR] Git is not installed or not in your PATH.${RESET}"
        echo -e "${YELLOW}Please install git via your package manager (e.g. sudo apt install git).${RESET}"
        exit 1
    fi

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[ERROR] Python3 is not installed or not in your PATH.${RESET}"
        echo -e "${YELLOW}Please install python3 (e.g. sudo apt install python3 python3-venv python3-pip).${RESET}"
        exit 1
    fi
}

add_to_path() {
    local target_dir="$1"
    local shell_rc=""
    
    # Identify shell config file
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.bashrc"
    fi
    
    if [ -f "$shell_rc" ]; then
        if ! grep -q "$target_dir" "$shell_rc"; then
            echo "export PATH=\"\$PATH:$target_dir\"" >> "$shell_rc"
            # Add alias 'tool' for easy launch
            echo "alias tool=\"$target_dir/venv/bin/python $target_dir/main.py\"" >> "$shell_rc"
            echo -e "${GREEN}[INFO] Added global environment alias! Restart your terminal or run 'source $shell_rc' to use 'tool' from anywhere.${RESET}"
        fi
    fi
}

install_toolkit() {
    check_prerequisites
    local target_dir="$HOME/Desktop/ToolKit-Linux"
    
    if [ -d "$target_dir/.git" ]; then
        echo -e "${GREEN}[INFO] ToolKit-Linux already exists. Pulling latest changes...${RESET}"
        cd "$target_dir" || exit 1
        git pull
    else
        echo -e "${GREEN}[INFO] Cloning ToolKit-Linux to $target_dir...${RESET}"
        git clone https://github.com/adityasing9/ToolKit-Linux.git "$target_dir"
        cd "$target_dir" || exit 1
    fi
    
    if [ ! -f "venv/bin/activate" ]; then
        echo -e "${GREEN}[INFO] Creating virtual environment...${RESET}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERROR] Failed to create virtual environment.${RESET}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}[INFO] Installing/Updating dependencies...${RESET}"
    ./venv/bin/pip install -r requirements.txt > /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to install requirements.${RESET}"
        exit 1
    fi
    
    add_to_path "$target_dir"
    echo -e "${CYAN}[INFO] Setup complete! Launching Toolkit...${RESET}"
    ./venv/bin/python main.py
}

run_toolkit() {
    local target_dir="$HOME/Desktop/ToolKit-Linux"
    if [ ! -d "$target_dir" ]; then
        echo -e "${RED}[ERROR] Toolkit is not installed at $target_dir!${RESET}"
        echo -e "${YELLOW}Please select option 1 to install it first.${RESET}"
        read -n 1 -s -r -p "Press any key to continue..." < /dev/tty
        return
    fi
    
    cd "$target_dir" || exit 1
    if [ ! -f "venv/bin/python" ]; then
        echo -e "${RED}[ERROR] Virtual environment not found. Please select option 1 to reinstall.${RESET}"
        read -n 1 -s -r -p "Press any key to continue..." < /dev/tty
        return
    fi
    
    add_to_path "$target_dir"
    echo -e "${CYAN}[INFO] Launching Toolkit...${RESET}"
    ./venv/bin/python main.py
}

run_portable() {
    check_prerequisites
    local target_dir="/tmp/ToolKit_Portable"
    
    if [ -d "$target_dir/.git" ]; then
        echo -e "${GREEN}[INFO] Portable Toolkit found in temp. Updating...${RESET}"
        cd "$target_dir" || exit 1
        git pull --quiet
    else
        echo -e "${GREEN}[INFO] Downloading Portable Toolkit to temp directory...${RESET}"
        git clone --depth 1 https://github.com/adityasing9/ToolKit-Linux.git "$target_dir"
        cd "$target_dir" || exit 1
    fi
    
    echo -e "${GREEN}[INFO] Installing Temporary Dependencies...${RESET}"
    python3 -m pip install -r requirements.txt --user
    
    echo -e "${CYAN}[INFO] Launching Portable Toolkit...${RESET}"
    python3 main.py
}

uninstall_toolkit() {
    echo -e "${YELLOW}[WARNING] This will completely delete the Linux Toolkit from your machine.${RESET}"
    read -p "Are you sure? (y/n) " confirm < /dev/tty
    if [ "$confirm" != "y" ]; then
        echo -e "${GREEN}Uninstallation cancelled.${RESET}"
        return
    fi
    
    local desktop_dir="$HOME/Desktop/ToolKit-Linux"
    local temp_dir="/tmp/ToolKit_Portable"
    local deleted=false
    
    if [ -d "$desktop_dir" ]; then
        echo -e "${CYAN}[INFO] Deleting installation at $desktop_dir...${RESET}"
        rm -rf "$desktop_dir"
        deleted=true
    fi
    
    if [ -d "$temp_dir" ]; then
        echo -e "${CYAN}[INFO] Deleting portable cache...${RESET}"
        rm -rf "$temp_dir"
        deleted=true
    fi
    
    # Remove path alias from RC file
    local shell_rc=""
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.bashrc"
    fi
    
    if [ -f "$shell_rc" ]; then
        # Remove alias and path entries
        sed -i '/ToolKit-Linux/d' "$shell_rc"
    fi
    
    if [ "$deleted" = true ]; then
        echo -e "${GREEN}[SUCCESS] Linux Toolkit has been completely removed.${RESET}"
    else
        echo -e "${YELLOW}[INFO] No Toolkit installation found.${RESET}"
    fi
    read -n 1 -s -r -p "Press any key to continue..." < /dev/tty
}

# Main Loop
while true; do
    show_menu
    read -p "Select an option (1-5): " choice < /dev/tty
    case "$choice" in
        1)
            install_toolkit
            ;;
        2)
            run_toolkit
            ;;
        3)
            run_portable
            ;;
        4)
            uninstall_toolkit
            ;;
        5)
            echo -e "${CYAN}Exiting...${RESET}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice, please try again.${RESET}"
            sleep 2
            ;;
    esac
done
