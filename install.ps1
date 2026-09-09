# ToolKit Web Installer / Manager

function Show-Menu {
    Clear-Host
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "       Toolkit CLI Manager (PowerShell)       " -ForegroundColor Cyan
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "1) Install / Update & Run Toolkit"
    Write-Host "2) Run Toolkit (If already installed)"
    Write-Host "3) Run Portable (No Installation / Temp Dir)"
    Write-Host "4) Uninstall & Remove Toolkit Completely"
    Write-Host "5) Exit"
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

function Add-ToPath {
    param ($Folder)
    try {
        $UserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
        if ($UserPath -notlike "*$Folder*") {
            [System.Environment]::SetEnvironmentVariable("Path", "$UserPath;$Folder", "User")
            Write-Host "[INFO] Added global environment alias! Restart terminal to use 'tool <cmd>' from anywhere." -ForegroundColor Green
        }
    } catch {
        Write-Host "[WARNING] Could not configure environment PATH automatically." -ForegroundColor Yellow
    }
}

function Install-Toolkit {
    Check-Prerequisites
    
    $RepoUrl = "https://github.com/adityasing9/ToolKit.git"
    $TargetDir = "$env:USERPROFILE\Desktop\ToolKit"
    $EditionName = "Windows Toolkit"

    if (Test-Path "$TargetDir\.git") {
        Write-Host "[INFO] $EditionName already exists at $TargetDir. Pulling latest changes..." -ForegroundColor Green
        Set-Location $TargetDir
        git pull
    } else {
        Write-Host "[INFO] Cloning $EditionName to $TargetDir..." -ForegroundColor Green
        git clone $RepoUrl $TargetDir
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

    Add-ToPath $TargetDir
    Write-Host "[INFO] Setup complete! Launching $EditionName..." -ForegroundColor Cyan
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
    
    Add-ToPath $TargetDir
    Write-Host "[INFO] Launching Toolkit from $TargetDir..." -ForegroundColor Cyan
    & ".\venv\Scripts\python.exe" main.py
}

function Run-Portable {
    Check-Prerequisites
    $TargetDir = "$env:TEMP\ToolKit_Portable"
    
    if (Test-Path "$TargetDir\.git") {
        Write-Host "[INFO] Portable Toolkit found in Temp. Updating..." -ForegroundColor Green
        Set-Location $TargetDir
        git pull --quiet
    } else {
        Write-Host "[INFO] Downloading Portable Toolkit to Temp Directory..." -ForegroundColor Green
        git clone --depth 1 https://github.com/adityasing9/ToolKit.git $TargetDir
        Set-Location $TargetDir
    }
    
    Write-Host "[INFO] Installing Temporary Dependencies (this may take a minute)..." -ForegroundColor Green
    # We use --user to ensure it doesn't require Admin rights for global Python installs.
    # Removed --quiet so you can see the progress bar.
    python -m pip install -r requirements.txt --user
    
    Write-Host "[INFO] Launching Portable Toolkit..." -ForegroundColor Cyan
    python main.py
}

function Uninstall-Toolkit {
    Write-Host "[WARNING] This will completely delete the Toolkit from your machine." -ForegroundColor Yellow
    $confirm = Read-Host "Are you sure? (y/n)"
    if ($confirm -ne 'y') {
        Write-Host "Uninstallation cancelled." -ForegroundColor Green
        return
    }

    $DesktopDir = "$env:USERPROFILE\Desktop\ToolKit"
    $TempDir = "$env:TEMP\ToolKit_Portable"
    $deleted = $false

    if (Test-Path $DesktopDir) {
        Write-Host "[INFO] Deleting permanent Windows installation at $DesktopDir..." -ForegroundColor Cyan
        Remove-Item -Recurse -Force $DesktopDir -ErrorAction SilentlyContinue
        $deleted = $true
    }
    
    if (Test-Path $TempDir) {
        Write-Host "[INFO] Deleting portable cache at $TempDir..." -ForegroundColor Cyan
        Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
        $deleted = $true
    }

    if ($deleted) {
        Write-Host "[SUCCESS] Toolkit has been completely removed from your system." -ForegroundColor Green
    } else {
        Write-Host "[INFO] No Toolkit installation found on this system." -ForegroundColor Yellow
    }
    pause
}

# Main Loop
while ($true) {
    Show-Menu
    $choice = Read-Host "Select an option (1-5)"

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
            Uninstall-Toolkit
            break
        }
        '5' {
            Write-Host "Exiting..." -ForegroundColor Cyan
            exit 0
        }
        default {
            Write-Host "Invalid choice, please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}
