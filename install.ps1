# ToolKit Web Installer

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "       Toolkit Web Installer (PowerShell)     " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# 1. Check if Git is installed
try {
    $null = Get-Command git -ErrorAction Stop
} catch {
    Write-Host "[ERROR] Git is not installed or not in your PATH." -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# 2. Check if Python is installed
try {
    $null = Get-Command python -ErrorAction Stop
} catch {
    Write-Host "[ERROR] Python is not installed or not in your PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 3. Define target directory
$TargetDir = "$env:USERPROFILE\Desktop\ToolKit"

# 4. Clone or Pull repository
if (Test-Path "$TargetDir\.git") {
    Write-Host "[INFO] ToolKit already exists at $TargetDir. Pulling latest changes..." -ForegroundColor Green
    Set-Location $TargetDir
    git pull
} else {
    Write-Host "[INFO] Cloning ToolKit to $TargetDir..." -ForegroundColor Green
    git clone https://github.com/adityasing9/ToolKit.git $TargetDir
    Set-Location $TargetDir
}

# 5. Create Virtual Environment
if (-Not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# 6. Install Dependencies
Write-Host "[INFO] Installing/Updating dependencies..." -ForegroundColor Green
& ".\venv\Scripts\pip.exe" install -r requirements.txt | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install requirements." -ForegroundColor Red
    exit 1
}

# 7. Run the Application
Write-Host "[INFO] Setup complete! Launching Toolkit..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" main.py
