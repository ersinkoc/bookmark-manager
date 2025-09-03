@echo off
REM Installation script for CLI Bookmark Manager on Windows
echo Installing CLI Bookmark Manager...

REM Create directory if it doesn't exist
if not exist "%USERPROFILE%\bookmark_manager" (
    mkdir "%USERPROFILE%\bookmark_manager"
)

REM Copy files to user directory
echo Copying files to %USERPROFILE%\bookmark_manager...
xcopy /s /y "%~dp0*" "%USERPROFILE%\bookmark_manager\"

REM Add to PATH (optional)
echo.
echo Adding to PATH...
setx PATH "%PATH%;%USERPROFILE%\bookmark_manager" /M

REM Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT=create_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Bookmark Manager.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%USERPROFILE%\bookmark_manager\bookmark_manager.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%USERPROFILE%\bookmark_manager" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript //nologo %SCRIPT%
del %SCRIPT%

echo.
echo Installation complete!
echo.
echo You can now run the bookmark manager by:
echo 1. Double-clicking the desktop shortcut
echo 2. Typing 'bookmark_manager' in Command Prompt
echo 3. Running '%USERPROFILE%\bookmark_manager\bookmark_manager.bat'
echo.
echo Example usage:
echo bookmark_manager add --url "https://github.com" --title "GitHub"
echo bookmark_manager list
echo bookmark_manager search "python"
echo.
pause