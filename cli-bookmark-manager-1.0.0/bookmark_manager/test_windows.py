#!/usr/bin/env python3

"""
Windows compatibility test script for CLI Bookmark Manager
This script tests all major functionality on Windows systems.
"""

import sys
import os
import tempfile
import shutil
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from database import DatabaseManager
    from models import Bookmark
    from utils import validate_url, export_to_json, import_from_json
    from main import BookmarkManager
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

def test_database_operations():
    """Test database operations."""
    print("\n=== Testing Database Operations ===")
    
    # Create temporary database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        db = DatabaseManager(temp_db.name)
        
        # Test adding bookmark
        bookmark = Bookmark(
            title="Test Bookmark",
            url="https://example.com",
            description="Test description",
            tags="test,demo"
        )
        
        bookmark_id = db.add_bookmark(bookmark)
        print(f"✓ Added bookmark with ID: {bookmark_id}")
        
        # Test retrieving bookmark
        retrieved = db.get_bookmark_by_id(bookmark_id)
        if retrieved and retrieved.title == "Test Bookmark":
            print("✓ Retrieved bookmark successfully")
        else:
            print("✗ Failed to retrieve bookmark")
            return False
        
        # Test search
        results = db.search_bookmarks("test")
        if len(results) > 0:
            print("✓ Search functionality working")
        else:
            print("✗ Search functionality failed")
            return False
        
        # Test statistics
        stats = db.get_bookmark_stats()
        if stats['total'] > 0:
            print("✓ Statistics working")
        else:
            print("✗ Statistics failed")
            return False
        
        # Test deletion
        success = db.delete_bookmark(bookmark_id)
        if success:
            print("✓ Bookmark deletion working")
        else:
            print("✗ Bookmark deletion failed")
            return False
        
        return True
        
    finally:
        # Clean up
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)

def test_url_validation():
    """Test URL validation."""
    print("\n=== Testing URL Validation ===")
    
    test_cases = [
        ("https://github.com", True),
        ("http://example.com", True),
        ("not_a_url", False),
        ("", False),
        ("https://example.com/path?query=value", True),
    ]
    
    for url, expected in test_cases:
        result = validate_url(url)
        if result == expected:
            print(f"✓ URL validation: {url} -> {result}")
        else:
            print(f"✗ URL validation failed: {url} -> {result} (expected {expected})")
            return False
    
    return True

def test_import_export():
    """Test import/export functionality."""
    print("\n=== Testing Import/Export ===")
    
    # Create test bookmarks
    bookmarks = [
        Bookmark(
            title="Test 1",
            url="https://example1.com",
            description="Test description 1",
            tags="test1"
        ),
        Bookmark(
            title="Test 2",
            url="https://example2.com",
            description="Test description 2",
            tags="test2"
        )
    ]
    
    # Test JSON export
    temp_json = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_json.close()
    
    try:
        success = export_to_json(bookmarks, temp_json.name)
        if success and os.path.exists(temp_json.name):
            print("✓ JSON export successful")
        else:
            print("✗ JSON export failed")
            return False
        
        # Test JSON import
        imported = import_from_json(temp_json.name)
        if len(imported) == 2:
            print("✓ JSON import successful")
        else:
            print(f"✗ JSON import failed: got {len(imported)} bookmarks")
            return False
        
    finally:
        if os.path.exists(temp_json.name):
            os.unlink(temp_json.name)
    
    return True

def test_bookmark_manager():
    """Test the main BookmarkManager class."""
    print("\n=== Testing BookmarkManager ===")
    
    # Create temporary database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        manager = BookmarkManager(temp_db.name)
        
        # Test adding bookmark
        success = manager.add_bookmark(
            url="https://github.com",
            title="GitHub",
            description="Code hosting platform",
            tags="dev,git"
        )
        
        if success:
            print("✓ BookmarkManager add successful")
        else:
            print("✗ BookmarkManager add failed")
            return False
        
        # Test listing bookmarks
        success = manager.list_bookmarks()
        if success:
            print("✓ BookmarkManager list successful")
        else:
            print("✗ BookmarkManager list failed")
            return False
        
        # Test search
        success = manager.search_bookmarks("github")
        if success:
            print("✓ BookmarkManager search successful")
        else:
            print("✗ BookmarkManager search failed")
            return False
        
        # Test update
        success = manager.update_bookmark("1", title="Updated GitHub")
        if success:
            print("✓ BookmarkManager update successful")
        else:
            print("✗ BookmarkManager update failed")
            return False
        
        # Test statistics
        success = manager.show_stats()
        if success:
            print("✓ BookmarkManager stats successful")
        else:
            print("✗ BookmarkManager stats failed")
            return False
        
        return True
        
    finally:
        # Clean up
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)

def test_windows_paths():
    """Test Windows-specific path handling."""
    print("\n=== Testing Windows Path Handling ===")
    
    if os.name == 'nt':
        # Test Windows path handling
        home_dir = os.path.expanduser("~")
        if os.path.exists(home_dir):
            print(f"✓ Windows home directory accessible: {home_dir}")
        else:
            print("✗ Windows home directory not accessible")
            return False
        
        # Test current directory
        current_dir = os.getcwd()
        if os.path.exists(current_dir):
            print(f"✓ Current directory accessible: {current_dir}")
        else:
            print("✗ Current directory not accessible")
            return False
        
        return True
    else:
        print("ℹ Not running on Windows, skipping Windows path tests")
        return True

def main():
    """Run all tests."""
    print("CLI Bookmark Manager - Windows Compatibility Test")
    print("=" * 50)
    
    tests = [
        test_url_validation,
        test_database_operations,
        test_import_export,
        test_bookmark_manager,
        test_windows_paths,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"✗ {test.__name__} failed")
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The bookmark manager is compatible with Windows.")
        return 0
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())