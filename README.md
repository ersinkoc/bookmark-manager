# CLI Bookmark Manager

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

A powerful, user-friendly command-line bookmark manager built with Python and SQLite. Save, organize, search, and manage your bookmarks efficiently from the terminal.

## ✨ Features

- 🗄️ **SQLite Database**: Fast, reliable local storage
- 🔍 **Advanced Search**: Search by title, URL, description, or tags
- 🏷️ **Tag System**: Organize bookmarks with flexible tagging
- 📤 **Import/Export**: JSON and CSV format support
- 🌐 **Browser Integration**: Open bookmarks directly in your default browser
- 📊 **Visit Tracking**: Track how many times you've visited each bookmark
- 📈 **Statistics**: View comprehensive statistics about your bookmark collection
- 🎨 **Colored Output**: Beautiful terminal output with colorama
- 🤖 **Auto-fetch Titles**: Automatically fetch webpage titles
- 📄 **Pagination**: Navigate through large bookmark collections
- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 Quick Start

### Installation

**Option 1: Using pip (Recommended)**
```bash
pip install cli-bookmark-manager
```

**Option 2: From Source**
```bash
git clone https://github.com/ersinkoc/bookmark-manager.git
cd bookmark-manager
pip install -r requirements.txt
```

**Windows Users:**
```bash
# Double-click setup.bat for automatic installation
# Or run:
python setup.py
```

### Basic Usage

```bash
# Add a bookmark
bookmark-manager add --url "https://github.com" --title "GitHub" --tags "dev,git"

# List all bookmarks
bookmark-manager list

# Search bookmarks
bookmark-manager search "python" --in all

# Update a bookmark
bookmark-manager update 1 --title "New Title"

# Delete a bookmark
bookmark-manager delete 1

# Open in browser
bookmark-manager open 1

# Export bookmarks
bookmark-manager export --format json --file bookmarks.json

# View statistics
bookmark-manager stats

# List all tags
bookmark-manager tags
```

## 📋 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new bookmark | `add --url "https://github.com" --title "GitHub" --tags "dev,git"` |
| `list` | List bookmarks | `list --limit 10 --page 1` |
| `search` | Search bookmarks | `search "python" --in title` |
| `update` | Update bookmark | `update 1 --title "New Title"` |
| `delete` | Delete bookmark | `delete 1` |
| `open` | Open in browser | `open 1` |
| `export` | Export bookmarks | `export --format json --file backup.json` |
| `import` | Import bookmarks | `import --file backup.json` |
| `stats` | Show statistics | `stats` |
| `tags` | List all tags | `tags` |

## 🏗️ Project Structure

```
bookmark-manager/
├── bookmark_manager/          # Main package
│   ├── __init__.py
│   ├── main.py               # Main CLI entry point
│   ├── bookmark_manager.py   # Core functionality
│   ├── database.py           # Database operations
│   ├── models.py             # Data models
│   ├── utils.py              # Utility functions
│   └── test_bookmark_manager.py  # Unit tests
├── setup.py                  # Package setup
├── pyproject.toml           # Modern packaging config
├── requirements.txt         # Dependencies
├── LICENSE                  # MIT License
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
├── CODE_OF_CONDUCT.md      # Code of conduct
├── CHANGELOG.md            # Changelog
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

### Database Location
- **Default**: `~/.bookmarks.db` (Linux/macOS) or `%USERPROFILE%\bookmarks.db` (Windows)
- **Custom**: Use `--db-path` option or set `BOOKMARK_DB_PATH` environment variable

### Environment Variables
```bash
export BOOKMARK_DB_PATH="/path/to/custom.db"
export BOOKMARK_DEBUG=1  # Enable debug mode
```

## 📊 Database Schema

```sql
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    description TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit_count INTEGER DEFAULT 0
);
```

## 🧪 Development

### Setup Development Environment
```bash
git clone https://github.com/ersinkoc/bookmark-manager.git
cd bookmark-manager
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

### Running Tests
```bash
python -m pytest bookmark_manager/test_bookmark_manager.py
python bookmark_manager/test_windows.py  # Windows compatibility tests
```

### Code Style
This project follows PEP 8 style guidelines. Use tools like `black` and `flake8` for formatting and linting.

```bash
pip install black flake8
black bookmark_manager/
flake8 bookmark_manager/
```

## 📝 Examples

### Example Workflow
```bash
# Add some bookmarks
bookmark-manager add --url "https://github.com" --title "GitHub" --tags "dev,git"
bookmark-manager add --url "https://stackoverflow.com" --title "Stack Overflow" --tags "programming,qa"
bookmark-manager add --url "https://python.org" --title "Python.org" --tags "python,programming"

# List all bookmarks
bookmark-manager list

# Search for programming-related bookmarks
bookmark-manager search "programming" --in tags

# Export to JSON
bookmark-manager export --format json --file bookmarks.json

# View statistics
bookmark-manager stats
```

### Advanced Usage
```bash
# Import bookmarks from browser export
bookmark-manager import --file bookmarks_export.json

# Search with specific criteria
bookmark-manager search "github" --in url
bookmark-manager search "python" --in title --in tags

# Batch operations with scripts
for url in $(cat urls.txt); do
    bookmark-manager add --url "$url" --fetch-title
done
```

## 🌍 Cross-Platform Support

### Windows
- Use `setup.bat` for automatic installation
- Desktop shortcut creation
- Windows-specific path handling
- Batch file launcher

### Linux/macOS
- Standard pip installation
- Bash completion support
- Unix-style path handling

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/ersinkoc/bookmark-manager/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ersinkoc/bookmark-manager/discussions)

---

⭐ If this project helped you, please consider giving it a star on [GitHub](https://github.com/ersinkoc/bookmark-manager)!