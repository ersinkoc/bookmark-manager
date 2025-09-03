# CLI Bookmark Manager - Windows Installation Guide

A simple command-line bookmark manager built with Python and SQLite. Save, organize, search, and manage your bookmarks efficiently from the Windows command prompt.

## Windows Installation

### Method 1: Using the Installer (Recommended)

1. **Download the files** to a folder on your computer
2. **Double-click `install.bat`** to run the installer
3. **Follow the prompts** - the installer will:
   - Copy files to your user directory
   - Add the program to your PATH
   - Create a desktop shortcut
   - Install required Python packages

### Method 2: Manual Installation

1. **Install Python** (if not already installed):
   - Download Python from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. **Install required packages**:
   ```cmd
   pip install colorama requests beautifulsoup4
   ```

3. **Download the bookmark manager files** to a folder

4. **Run the program**:
   ```cmd
   python main.py --help
   ```

## Usage on Windows

### Using the Desktop Shortcut
- Double-click the "Bookmark Manager" shortcut on your desktop

### Using Command Prompt
- Open Command Prompt and type:
  ```cmd
  bookmark_manager add --url "https://github.com" --title "GitHub"
  ```

### Using Batch File
- Navigate to the bookmark_manager folder
- Double-click `bookmark_manager.bat`

## Basic Commands

### Add a Bookmark
```cmd
bookmark_manager add --url "https://github.com" --title "GitHub" --tags "dev,git"
```

### List Bookmarks
```cmd
bookmark_manager list
bookmark_manager list --limit 10 --page 1
```

### Search Bookmarks
```cmd
bookmark_manager search "python"
bookmark_manager search "github" --in url
```

### Update a Bookmark
```cmd
bookmark_manager update 1 --title "New Title"
```

### Delete a Bookmark
```cmd
bookmark_manager delete 1
```

### Open in Browser
```cmd
bookmark_manager open 1
```

### Export Bookmarks
```cmd
bookmark_manager export --format json --file my_bookmarks.json
bookmark_manager export --format csv --file my_bookmarks.csv
```

### Import Bookmarks
```cmd
bookmark_manager import --file my_bookmarks.json
bookmark_manager import --file my_bookmarks.csv
```

### View Statistics
```cmd
bookmark_manager stats
```

### List Tags
```cmd
bookmark_manager tags
```

## Windows-Specific Features

### Database Location
- On Windows, the database is stored in your user directory: `C:\Users\YourUsername\bookmarks.db`
- This ensures the database is accessible and backed up with your user profile

### Path Handling
- The program automatically handles Windows file paths
- Export files are saved to the current working directory by default

### Error Handling
- Windows-specific error messages for common issues
- Automatic dependency checking and installation

### Browser Integration
- Automatically opens URLs in your default Windows browser
- Supports Chrome, Firefox, Edge, and other browsers

## Troubleshooting

### Python Not Found
If you see "Python is not installed or not in PATH":
1. Install Python from [python.org](https://python.org)
2. Make sure to check "Add Python to PATH" during installation
3. Restart Command Prompt after installation

### Permission Errors
If you see permission errors:
1. Run Command Prompt as Administrator
2. Or install the program in your user directory instead of Program Files

### Dependencies Not Installing
If packages fail to install:
```cmd
python -m pip install --upgrade pip
pip install colorama requests beautifulsoup4
```

### Database Location Issues
If the database is not found:
1. The program will automatically create it in your user directory
2. You can specify a custom location: `python main.py --db-path "C:\custom\path\bookmarks.db"`

### Browser Not Opening
If URLs don't open in browser:
1. Check that you have a default browser set in Windows
2. Try opening the URL manually in your browser

## Advanced Usage

### Running from Python Directly
```cmd
python main.py add --url "https://example.com" --title "Test"
```

### Using Custom Database Location
```cmd
python main.py --db-path "C:\MyBookmarks\bookmarks.db" add --url "https://example.com" --title "Test"
```

### Batch Operations
Create a text file with commands and run:
```cmd
@echo off
python main.py add --url "https://github.com" --title "GitHub"
python main.py add --url "https://stackoverflow.com" --title "Stack Overflow"
python main.py list
```

## File Locations

### Program Files
- Installed to: `%USERPROFILE%\bookmark_manager\`
- Main executable: `%USERPROFILE%\bookmark_manager\main.py`
- Launcher: `%USERPROFILE%\bookmark_manager\bookmark_manager.bat`

### Database
- Default location: `%USERPROFILE%\bookmarks.db`
- SQLite database file with all your bookmarks

### Exports
- Default location: Current working directory
- JSON format: `bookmarks_export_YYYYMMDD_HHMMSS.json`
- CSV format: `bookmarks_export_YYYYMMDD_HHMMSS.csv`

## Uninstallation

### Using the Uninstaller
1. Double-click `uninstall.bat` in the bookmark_manager folder
2. Follow the prompts to remove the program

### Manual Uninstallation
1. Remove the desktop shortcut
2. Delete the bookmark_manager folder from your user directory
3. Remove the database file if desired
4. Remove from PATH (if manually added)

## Windows Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new bookmark | `add --url "https://github.com" --title "GitHub"` |
| `list` | List bookmarks | `list --limit 10` |
| `search` | Search bookmarks | `search "python" --in title` |
| `update` | Update bookmark | `update 1 --title "New Title"` |
| `delete` | Delete bookmark | `delete 1` |
| `open` | Open in browser | `open 1` |
| `export` | Export bookmarks | `export --format json --file backup.json` |
| `import` | Import bookmarks | `import --file backup.json` |
| `stats` | Show statistics | `stats` |
| `tags` | List all tags | `tags` |

## Support

For issues and feature requests:
1. Check the troubleshooting section above
2. Run with debug mode: `set BOOKMARK_DEBUG=1` then `bookmark_manager stats`
3. Create an issue in the project repository

## System Requirements

- Windows 7, 8, 10, or 11
- Python 3.8 or higher
- Internet connection for fetching titles and opening URLs
- 10MB of disk space

---

**Tip**: Right-click on the Command Prompt title bar and go to Properties → Options to enable QuickEdit mode for easier copying and pasting!