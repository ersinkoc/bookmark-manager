@echo off
REM CLI Bookmark Manager - Windows Launcher
REM This script makes it easy to run the bookmark manager on Windows

echo Starting CLI Bookmark Manager...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import colorama, requests, beautifulsoup4" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install colorama requests beautifulsoup4
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        echo Please run: pip install colorama requests beautifulsoup4
        pause
        exit /b 1
    )
)

REM Run the bookmark manager
cd /d "%~dp0"
python main.py %*

if errorlevel 1 (
    echo.
    echo Program exited with an error.
    pause
)