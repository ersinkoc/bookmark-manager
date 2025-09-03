# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CLI Bookmark Manager built with Python and SQLite. It's a command-line tool for managing bookmarks with features like tagging, search, import/export, and browser integration.

## Key Commands

### Development Commands
```bash
# Run tests
python -m pytest bookmark_manager/test_bookmark_manager.py
python bookmark_manager/test_windows.py  # Windows compatibility tests

# Code formatting and linting
black bookmark_manager/
flake8 bookmark_manager/

# Install development dependencies
pip install -e .[dev]

# Run the application
bookmark-manager --help
bm --help  # short alias
```

### Testing Commands
```bash
# Run all tests with coverage
pytest --cov=bookmark_manager --cov-report=term-missing

# Run specific test file
python -m pytest bookmark_manager/test_bookmark_manager.py -v

# Run with coverage report
pytest --cov=bookmark_manager --cov-report=html
```

## Architecture Overview

### Core Components

1. **main.py** - Entry point with CLI argument parsing and command routing
2. **bookmark_manager.py** - Main BookmarkManager class with business logic
3. **database.py** - DatabaseManager class handling all SQLite operations
4. **models.py** - Bookmark dataclass and related data structures
5. **utils.py** - Utility functions for validation, export/import, display, etc.

### Key Design Patterns

- **Data Model**: Uses `@dataclass` for Bookmark model with automatic serialization
- **Database Layer**: SQLite with context managers for connection management
- **CLI Interface**: argparse with subcommands for different operations
- **Cross-Platform**: Special handling for Windows paths and batch files

### Database Schema

```sql
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    description TEXT,
    tags TEXT,  -- Comma-separated
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit_count INTEGER DEFAULT 0
);
```

## Development Notes

### File Structure
- Two main entry points: `main.py` (standalone) and `bookmark_manager.py` (package)
- Windows compatibility: Special path handling and batch files (`*.bat`)
- Tests: `test_bookmark_manager.py` (unit tests) and `test_windows.py` (Windows-specific)

### Dependencies
- **Core**: requests, beautifulsoup4, colorama
- **Dev**: black, flake8, mypy, pytest, pytest-cov
- **Python**: Requires 3.8+

### Entry Points
The package provides two console commands:
- `bookmark-manager` - Full command
- `bm` - Short alias

Both point to `bookmark_manager.main:main`

### Cross-Platform Considerations
- Windows uses different path handling (`sys.path.insert` for module imports)
- Batch files for Windows installation/setup
- Database location varies by platform (home directory vs user profile)

### Code Style
- Follows PEP 8
- Uses Black formatter (88 character line length)
- Type hints throughout
- MyPy for static type checking