"""
CLI Bookmark Manager - A powerful command-line bookmark management tool.

A user-friendly bookmark manager built with Python and SQLite that allows you to
save, organize, search, and manage your bookmarks efficiently from the terminal.

Features:
- SQLite database for fast, reliable local storage
- Advanced search by title, URL, description, or tags
- Flexible tagging system for organization
- Import/Export functionality (JSON, CSV)
- Browser integration
- Visit tracking and statistics
- Colored terminal output
- Cross-platform support (Windows, Linux, macOS)
- Auto-fetch webpage titles
- Pagination support

Author: Ersin KOÇ
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Ersin KOÇ"
__email__ = "ersinkoc@gmail.com"
__license__ = "MIT"
__description__ = "A powerful command-line bookmark manager built with Python and SQLite"

# Import main classes for easy access
from .bookmark_manager import BookmarkManager
from .models import Bookmark
from .database import DatabaseManager

__all__ = [
    "BookmarkManager",
    "Bookmark", 
    "DatabaseManager",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__"
]