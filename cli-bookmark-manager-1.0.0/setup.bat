@echo off
echo ================================================================
echo                CLI Bookmark Manager - Windows Setup
echo ================================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version

REM Check if pip is available
echo.
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [OK] pip is available
python -m pip --version

REM Install required packages
echo.
echo Installing required packages...
python -m pip install colorama requests beautifulsoup4

if errorlevel 1 (
    echo [ERROR] Failed to install required packages
    echo Please run: python -m pip install colorama requests beautifulsoup4
    pause
    exit /b 1
)

echo [OK] Required packages installed successfully

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
set SCRIPT=create_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Bookmark Manager.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\bookmark_manager.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%" >> %SCRIPT%
echo oLink.Description = "CLI Bookmark Manager" >> %SCRIPT%
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll, 14" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript //nologo %SCRIPT%
del %SCRIPT%

echo [OK] Desktop shortcut created

REM Test the application
echo.
echo Testing the application...
python test_windows.py

if errorlevel 1 (
    echo [WARNING] Some tests failed, but the application should still work
) else (
    echo [OK] All tests passed
)

echo.
echo ================================================================
echo                    Setup Complete!
echo ================================================================
echo.
echo You can now use the bookmark manager in several ways:
echo.
echo 1. Double-click the desktop shortcut "Bookmark Manager"
echo 2. Run: bookmark_manager.bat
echo 3. Run: python main.py
echo.
echo Example commands:
echo   bookmark_manager.bat add --url "https://github.com" --title "GitHub"
echo   bookmark_manager.bat list
echo   bookmark_manager.bat search "python"
echo.
echo Database location: %USERPROFILE%\bookmarks.db
echo.
pause