@echo off
setlocal

echo ==============================================
echo        Toolkit Bootstrap Script
echo ==============================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

:: Check if the virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate the virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo [INFO] Checking dependencies...
pip install -r requirements.txt >nul
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

:: Run the application
echo [INFO] Starting Toolkit...
python main.py

:: Keep window open if the app crashes
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application crashed or exited with an error.
    pause
)

endlocal
exit /b 0
