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
    $global:HasGit = $false
    $global:HasPython = $false
    
    try {
        $null = Get-Command git -ErrorAction Stop
        $global:HasGit = $true
    } catch {}

    try {
        $null = Get-Command python -ErrorAction Stop
        $global:HasPython = $true
    } catch {}
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

function Install-StandaloneEXE {
    param($TargetDir)
    
    $ExeUrl = "https://github.com/adityasing9/ToolKit/raw/main/dist/tool.exe"
    $TargetExe = Join-Path $TargetDir "tool.exe"
    
    Write-Host "[INFO] Downloading standalone tool.exe from GitHub..." -ForegroundColor Green
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $ExeUrl -OutFile $TargetExe -UseBasicParsing
        Write-Host "[SUCCESS] Standalone EXE downloaded successfully!" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to download standalone EXE: $_" -ForegroundColor Red
        pause
        return
    }
    
    # Set up global PATH so user can type `tool` from anywhere
    Add-ToPath $TargetDir
    
    # Create batch and PowerShell helper scripts in target directory
    $BatchFile = Join-Path $TargetDir "tool.bat"
    "@echo off`r`n`\"$TargetExe`\" %*" | Out-File -FilePath $BatchFile -Encoding ascii -Force
    
    $PsFile = Join-Path $TargetDir "tool.ps1"
    "& `\"$TargetExe`\" `$args" | Out-File -FilePath $PsFile -Encoding ascii -Force
    
    Write-Host "[INFO] Launching Standalone Toolkit..." -ForegroundColor Cyan
    & $TargetExe
}

function Install-DeveloperSource {
    param($TargetDir)
    
    $RepoUrl = "https://github.com/adityasing9/ToolKit.git"
    $EditionName = "Windows Toolkit (Developer Edition)"
    
    if (Test-Path "$TargetDir\.git") {
        Write-Host "[INFO] $EditionName already exists. Pulling latest changes..." -ForegroundColor Green
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
            pause
            return
        }
    }

    Write-Host "[INFO] Installing/Updating dependencies..." -ForegroundColor Green
    & ".\venv\Scripts\pip.exe" install -r requirements.txt | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install requirements." -ForegroundColor Red
        pause
        return
    }

    Add-ToPath $TargetDir
    Write-Host "[INFO] Setup complete! Launching $EditionName..." -ForegroundColor Cyan
    & ".\venv\Scripts\python.exe" main.py
}

function Install-Toolkit {
    Check-Prerequisites
    
    $TargetDir = "$env:USERPROFILE\Desktop\ToolKit"
    if (-Not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    }
    
    # If they don't have git or python, default to Standalone EXE
    if (-Not $global:HasGit -Or -Not $global:HasPython) {
        Write-Host "[INFO] Git or Python is not installed. Defaulting to Standalone EXE Edition..." -ForegroundColor Yellow
        Install-StandaloneEXE $TargetDir
        return
    }
    
    # Both are installed, ask the user for their preference
    Write-Host ""
    Write-Host "Both Git and Python are available on this system." -ForegroundColor Green
    Write-Host "Select installation type:" -ForegroundColor Cyan
    Write-Host "1) Standalone EXE Edition (Fast, no external requirements, single file)" -ForegroundColor Yellow
    Write-Host "2) Developer Source Edition (Clones repo, creates venv, requires git/python)" -ForegroundColor White
    $InstallChoice = Read-Host "Choice (1 or 2)"
    
    if ($InstallChoice -eq "2") {
        Install-DeveloperSource $TargetDir
    } else {
        Install-StandaloneEXE $TargetDir
    }
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
    
    if (Test-Path "tool.exe") {
        Write-Host "[INFO] Launching Standalone Toolkit..." -ForegroundColor Cyan
        & ".\tool.exe"
    } elseif (Test-Path "venv\Scripts\python.exe") {
        Add-ToPath $TargetDir
        Write-Host "[INFO] Launching Developer Toolkit..." -ForegroundColor Cyan
        & ".\venv\Scripts\python.exe" main.py
    } else {
        Write-Host "[ERROR] Neither tool.exe nor virtual environment found in $TargetDir." -ForegroundColor Red
        Write-Host "Please choose option 1 to reinstall." -ForegroundColor Yellow
        pause
    }
}

function Run-Portable {
    Check-Prerequisites
    $TargetDir = "$env:TEMP\ToolKit_Portable"
    if (-Not (Test-Path $TargetDir)) {
        New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
    }
    
    # If they don't have git or python, default to downloading tool.exe
    if (-Not $global:HasGit -Or -Not $global:HasPython) {
        Write-Host "[INFO] Git or Python is not installed. Defaulting to Portable Standalone EXE..." -ForegroundColor Yellow
        $ExeUrl = "https://github.com/adityasing9/ToolKit/raw/main/dist/tool.exe"
        $TargetExe = Join-Path $TargetDir "tool.exe"
        
        Write-Host "[INFO] Downloading Portable standalone tool.exe..." -ForegroundColor Green
        try {
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $ExeUrl -OutFile $TargetExe -UseBasicParsing
        } catch {
            Write-Host "[ERROR] Failed to download standalone EXE: $_" -ForegroundColor Red
            pause
            return
        }
        
        Write-Host "[INFO] Launching Portable Standalone Toolkit..." -ForegroundColor Cyan
        & $TargetExe
        return
    }
    
    # Otherwise, ask the user
    Write-Host ""
    Write-Host "Select Portable type to run:" -ForegroundColor Cyan
    Write-Host "1) Standalone EXE Edition (Fast, no requirements, no install)" -ForegroundColor Yellow
    Write-Host "2) Developer Source Edition (Clones to temp, requires python/pip)" -ForegroundColor White
    $PortableChoice = Read-Host "Choice (1 or 2)"
    
    if ($PortableChoice -eq "2") {
        if (Test-Path "$TargetDir\.git") {
            Write-Host "[INFO] Portable Toolkit found in Temp. Updating..." -ForegroundColor Green
            Set-Location $TargetDir
            git pull --quiet
        } else {
            Write-Host "[INFO] Downloading Portable Toolkit to Temp Directory..." -ForegroundColor Green
            git clone --depth 1 https://github.com/adityasing9/ToolKit.git $TargetDir
            Set-Location $TargetDir
        }
        
        Write-Host "[INFO] Installing Temporary Dependencies..." -ForegroundColor Green
        python -m pip install -r requirements.txt --user
        
        Write-Host "[INFO] Launching Portable Toolkit..." -ForegroundColor Cyan
        python main.py
    } else {
        $ExeUrl = "https://github.com/adityasing9/ToolKit/raw/main/dist/tool.exe"
        $TargetExe = Join-Path $TargetDir "tool.exe"
        Write-Host "[INFO] Downloading Portable standalone tool.exe..." -ForegroundColor Green
        try {
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $ExeUrl -OutFile $TargetExe -UseBasicParsing
        } catch {
            Write-Host "[ERROR] Failed to download: $_" -ForegroundColor Red
            pause
            return
        }
        Write-Host "[INFO] Launching Portable Standalone Toolkit..." -ForegroundColor Cyan
        & $TargetExe
    }
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
