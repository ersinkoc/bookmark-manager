@echo off
REM Uninstallation script for CLI Bookmark Manager on Windows
echo Uninstalling CLI Bookmark Manager...

REM Remove from PATH
echo Removing from PATH...
for /f "tokens=2,*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set OLD_PATH=%%B
set NEW_PATH=%OLD_PATH:%USERPROFILE%\bookmark_manager;=%
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%NEW_PATH%" /f

REM Remove desktop shortcut
echo Removing desktop shortcut...
if exist "%USERPROFILE%\Desktop\Bookmark Manager.lnk" (
    del "%USERPROFILE%\Desktop\Bookmark Manager.lnk"
)

REM Ask if user wants to remove the database
echo.
set /p remove_db="Do you want to remove the database file? (y/N): "
if /i "%remove_db%"=="y" (
    if exist "%USERPROFILE%\bookmarks.db" (
        del "%USERPROFILE%\bookmarks.db"
        echo Database file removed.
    )
)

REM Ask if user wants to remove the application files
set /p remove_files="Do you want to remove the application files? (y/N): "
if /i "%remove_files%"=="y" (
    if exist "%USERPROFILE%\bookmark_manager" (
        rmdir /s /q "%USERPROFILE%\bookmark_manager"
        echo Application files removed.
    )
)

echo.
echo Uninstallation complete!
pause