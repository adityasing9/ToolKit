# ToolKit Web Installer / Manager

function Show-Menu {
    Clear-Host
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "       Toolkit CLI Manager (PowerShell)       " -ForegroundColor Cyan
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "1) Install / Update & Run Toolkit"
    Write-Host "2) Run Toolkit (If already installed)"
    Write-Host "3) Run Portable (No Installation / Temp Dir)"
    Write-Host "4) Exit"
    Write-Host "==============================================" -ForegroundColor Cyan
}

function Check-Prerequisites {
    try {
        $null = Get-Command git -ErrorAction Stop
    } catch {
        Write-Host "[ERROR] Git is not installed or not in your PATH." -ForegroundColor Red
        Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
        exit 1
    }

    try {
        $null = Get-Command python -ErrorAction Stop
    } catch {
        Write-Host "[ERROR] Python is not installed or not in your PATH." -ForegroundColor Red
        Write-Host "Please install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

function Install-Toolkit {
    Check-Prerequisites
    $TargetDir = "$env:USERPROFILE\Desktop\ToolKit"

    if (Test-Path "$TargetDir\.git") {
        Write-Host "[INFO] ToolKit already exists at $TargetDir. Pulling latest changes..." -ForegroundColor Green
        Set-Location $TargetDir
        git pull
    } else {
        Write-Host "[INFO] Cloning ToolKit to $TargetDir..." -ForegroundColor Green
        git clone https://github.com/adityasing9/ToolKit.git $TargetDir
        Set-Location $TargetDir
    }

    if (-Not (Test-Path "venv\Scripts\activate.ps1")) {
        Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Green
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to create virtual environment." -ForegroundColor Red
            exit 1
        }
    }

    Write-Host "[INFO] Installing/Updating dependencies..." -ForegroundColor Green
    & ".\venv\Scripts\pip.exe" install -r requirements.txt | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install requirements." -ForegroundColor Red
        exit 1
    }

    Write-Host "[INFO] Setup complete! Launching Toolkit..." -ForegroundColor Cyan
    & ".\venv\Scripts\python.exe" main.py
}

function Run-Toolkit {
    $TargetDir = "$env:USERPROFILE\Desktop\ToolKit"
    if (-Not (Test-Path $TargetDir)) {
        Write-Host "[ERROR] Toolkit is not installed at $TargetDir!" -ForegroundColor Red
        Write-Host "Please select option 1 to install it first." -ForegroundColor Yellow
        pause
        return
    }
    
    Set-Location $TargetDir
    if (-Not (Test-Path "venv\Scripts\python.exe")) {
        Write-Host "[ERROR] Virtual environment not found. Please select option 1 to reinstall." -ForegroundColor Red
        pause
        return
    }
    
    Write-Host "[INFO] Launching Toolkit..." -ForegroundColor Cyan
    & ".\venv\Scripts\python.exe" main.py
}

function Run-Portable {
    Check-Prerequisites
    $TargetDir = "$env:TEMP\ToolKit_Portable"
    
    if (Test-Path "$TargetDir") {
        Remove-Item -Recurse -Force "$TargetDir"
    }

    Write-Host "[INFO] Downloading Portable Toolkit to Temp Directory..." -ForegroundColor Green
    git clone --depth 1 https://github.com/adityasing9/ToolKit.git $TargetDir
    Set-Location $TargetDir
    
    Write-Host "[INFO] Installing Temporary Dependencies..." -ForegroundColor Green
    # In portable mode, we just use the global python to avoid the slow venv creation, 
    # but we suppress output.
    python -m pip install -r requirements.txt --quiet
    
    Write-Host "[INFO] Launching Portable Toolkit..." -ForegroundColor Cyan
    python main.py
}

# Main Loop
while ($true) {
    Show-Menu
    $choice = Read-Host "Select an option (1-4)"

    switch ($choice) {
        '1' {
            Install-Toolkit
            break
        }
        '2' {
            Run-Toolkit
            break
        }
        '3' {
            Run-Portable
            break
        }
        '4' {
            Write-Host "Exiting..." -ForegroundColor Cyan
            exit 0
        }
        default {
            Write-Host "Invalid choice, please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}
