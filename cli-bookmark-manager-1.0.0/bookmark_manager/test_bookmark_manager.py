import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import tempfile
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bookmark_manager.database import DatabaseManager
from bookmark_manager.models import Bookmark
from bookmark_manager.utils import validate_url, fetch_title_from_url, export_to_json, import_from_json
from bookmark_manager.bookmark_manager import BookmarkManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager class."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        os.unlink(self.temp_db.name)
    
    def test_init_database(self):
        """Test database initialization."""
        # Check if the bookmarks table was created
        bookmarks = self.db.get_all_bookmarks()
        self.assertEqual(len(bookmarks), 0)
    
    def test_add_bookmark(self):
        """Test adding a bookmark."""
        bookmark = Bookmark(
            title="Test Bookmark",
            url="https://example.com",
            description="A test bookmark",
            tags="test,demo"
        )
        
        bookmark_id = self.db.add_bookmark(bookmark)
        self.assertIsInstance(bookmark_id, int)
        self.assertGreater(bookmark_id, 0)
        
        # Verify the bookmark was added
        retrieved = self.db.get_bookmark_by_id(bookmark_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Test Bookmark")
        self.assertEqual(retrieved.url, "https://example.com")
    
    def test_add_duplicate_url(self):
        """Test adding duplicate URL."""
        bookmark1 = Bookmark(title="First", url="https://example.com")
        bookmark2 = Bookmark(title="Second", url="https://example.com")
        
        self.db.add_bookmark(bookmark1)
        with self.assertRaises(Exception):
            self.db.add_bookmark(bookmark2)
    
    def test_get_bookmark_by_id(self):
        """Test retrieving bookmark by ID."""
        bookmark = Bookmark(title="Test", url="https://example.com")
        bookmark_id = self.db.add_bookmark(bookmark)
        
        retrieved = self.db.get_bookmark_by_id(bookmark_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Test")
        
        # Test non-existent ID
        retrieved = self.db.get_bookmark_by_id(99999)
        self.assertIsNone(retrieved)
    
    def test_get_bookmark_by_url(self):
        """Test retrieving bookmark by URL."""
        bookmark = Bookmark(title="Test", url="https://example.com")
        self.db.add_bookmark(bookmark)
        
        retrieved = self.db.get_bookmark_by_url("https://example.com")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Test")
        
        # Test non-existent URL
        retrieved = self.db.get_bookmark_by_url("https://nonexistent.com")
        self.assertIsNone(retrieved)
    
    def test_update_bookmark(self):
        """Test updating a bookmark."""
        bookmark = Bookmark(title="Original", url="https://example.com")
        bookmark_id = self.db.add_bookmark(bookmark)
        
        updates = {"title": "Updated", "description": "New description"}
        success = self.db.update_bookmark(bookmark_id, updates)
        self.assertTrue(success)
        
        retrieved = self.db.get_bookmark_by_id(bookmark_id)
        self.assertEqual(retrieved.title, "Updated")
        self.assertEqual(retrieved.description, "New description")
    
    def test_delete_bookmark(self):
        """Test deleting a bookmark."""
        bookmark = Bookmark(title="Test", url="https://example.com")
        bookmark_id = self.db.add_bookmark(bookmark)
        
        success = self.db.delete_bookmark(bookmark_id)
        self.assertTrue(success)
        
        retrieved = self.db.get_bookmark_by_id(bookmark_id)
        self.assertIsNone(retrieved)
    
    def test_search_bookmarks(self):
        """Test searching bookmarks."""
        # Add test bookmarks
        bookmarks = [
            Bookmark(title="Python Tutorial", url="https://python.org", tags="python,programming"),
            Bookmark(title="JavaScript Guide", url="https://javascript.com", tags="javascript,web"),
            Bookmark(title="Learn Python", url="https://learnpython.com", tags="python,tutorial")
        ]
        
        for bookmark in bookmarks:
            self.db.add_bookmark(bookmark)
        
        # Search by title
        results = self.db.search_bookmarks("python", "title")
        self.assertEqual(len(results), 2)
        
        # Search by tags
        results = self.db.search_bookmarks("python", "tags")
        self.assertEqual(len(results), 2)
        
        # Search in all fields
        results = self.db.search_bookmarks("python", "all")
        self.assertEqual(len(results), 2)
    
    def test_get_bookmark_stats(self):
        """Test getting bookmark statistics."""
        # Add test bookmarks
        bookmark1 = Bookmark(title="First", url="https://first.com")
        bookmark2 = Bookmark(title="Second", url="https://second.com")
        
        self.db.add_bookmark(bookmark1)
        self.db.add_bookmark(bookmark2)
        
        # Increment visit count for one bookmark
        self.db.increment_visit_count(1)
        self.db.increment_visit_count(1)
        
        stats = self.db.get_bookmark_stats()
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['visited'], 1)
        self.assertEqual(stats['max_visits'], 2)
    
    def test_get_all_tags(self):
        """Test getting all unique tags."""
        # Add test bookmarks with tags
        bookmarks = [
            Bookmark(title="Python", url="https://python.org", tags="python,programming"),
            Bookmark(title="JavaScript", url="https://javascript.com", tags="javascript,web"),
            Bookmark(title="Java", url="https://java.com", tags="java,programming")
        ]
        
        for bookmark in bookmarks:
            self.db.add_bookmark(bookmark)
        
        tags = self.db.get_all_tags()
        expected_tags = ['java', 'javascript', 'programming', 'python', 'web']
        self.assertEqual(sorted(tags), expected_tags)


class TestBookmarkModel(unittest.TestCase):
    """Test cases for Bookmark model."""
    
    def test_bookmark_creation(self):
        """Test creating a bookmark."""
        bookmark = Bookmark(
            title="Test Bookmark",
            url="https://example.com",
            description="A test bookmark",
            tags="test,demo"
        )
        
        self.assertEqual(bookmark.title, "Test Bookmark")
        self.assertEqual(bookmark.url, "https://example.com")
        self.assertEqual(bookmark.description, "A test bookmark")
        self.assertEqual(bookmark.tags, "test,demo")
        self.assertEqual(bookmark.visit_count, 0)
    
    def test_get_tags_list(self):
        """Test getting tags as list."""
        bookmark = Bookmark(tags="python,programming,web")
        tags = bookmark.get_tags_list()
        self.assertEqual(tags, ["python", "programming", "web"])
        
        # Test empty tags
        bookmark.tags = None
        tags = bookmark.get_tags_list()
        self.assertEqual(tags, [])
    
    def test_set_tags_list(self):
        """Test setting tags from list."""
        bookmark = Bookmark()
        bookmark.set_tags_list(["python", "programming", "web"])
        self.assertEqual(bookmark.tags, "python,programming,web")
        
        # Test with empty strings
        bookmark.set_tags_list(["python", "", "programming", "  "])
        self.assertEqual(bookmark.tags, "python,programming")
    
    def test_to_dict(self):
        """Test converting bookmark to dictionary."""
        bookmark = Bookmark(
            id=1,
            title="Test",
            url="https://example.com",
            description="Test description",
            tags="test,demo"
        )
        
        result = bookmark.to_dict()
        self.assertEqual(result['title'], "Test")
        self.assertEqual(result['url'], "https://example.com")
        self.assertEqual(result['tags'], ["test", "demo"])
    
    def test_from_dict(self):
        """Test creating bookmark from dictionary."""
        data = {
            'id': 1,
            'title': 'Test',
            'url': 'https://example.com',
            'description': 'Test description',
            'tags': ['test', 'demo'],
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00',
            'visit_count': 5
        }
        
        bookmark = Bookmark.from_dict(data)
        self.assertEqual(bookmark.title, "Test")
        self.assertEqual(bookmark.url, "https://example.com")
        self.assertEqual(bookmark.tags, "test,demo")
        self.assertEqual(bookmark.visit_count, 5)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_url(self):
        """Test URL validation."""
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://example.com/path"))
        self.assertTrue(validate_url("https://example.com:8080/path?query=value"))
        
        self.assertFalse(validate_url("not_a_url"))
        self.assertFalse(validate_url("example.com"))
        self.assertFalse(validate_url(""))
    
    @patch('bookmark_manager.utils.requests.get')
    def test_fetch_title_from_url(self, mock_get):
        """Test fetching title from URL."""
        # Mock successful response
        mock_response = Mock()
        mock_response.content = '<html><head><title>Test Title</title></head><body></body></html>'
        mock_get.return_value = mock_response
        
        title = fetch_title_from_url("https://example.com")
        self.assertEqual(title, "Test Title")
        
        # Mock failed response
        mock_get.side_effect = Exception("Network error")
        title = fetch_title_from_url("https://example.com")
        self.assertIsNone(title)
    
    def test_export_import_json(self):
        """Test JSON export and import."""
        # Create test bookmarks
        bookmarks = [
            Bookmark(
                id=1,
                title="First",
                url="https://first.com",
                description="First bookmark",
                tags="test"
            ),
            Bookmark(
                id=2,
                title="Second",
                url="https://second.com",
                description="Second bookmark",
                tags="demo"
            )
        ]
        
        # Export to JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_file = f.name
        
        try:
            success = export_to_json(bookmarks, json_file)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(json_file))
            
            # Import from JSON
            imported = import_from_json(json_file)
            self.assertEqual(len(imported), 2)
            self.assertEqual(imported[0].title, "First")
            self.assertEqual(imported[1].title, "Second")
        finally:
            if os.path.exists(json_file):
                os.unlink(json_file)


class TestBookmarkManager(unittest.TestCase):
    """Test cases for BookmarkManager class."""
    
    def setUp(self):
        """Set up test bookmark manager."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.manager = BookmarkManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        os.unlink(self.temp_db.name)
    
    def test_add_bookmark(self):
        """Test adding a bookmark through the manager."""
        success = self.manager.add_bookmark(
            url="https://example.com",
            title="Test Bookmark"
        )
        self.assertTrue(success)
        
        # Verify it was added
        bookmarks = self.manager.db.get_all_bookmarks()
        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmarks[0].title, "Test Bookmark")
    
    def test_add_invalid_url(self):
        """Test adding bookmark with invalid URL."""
        success = self.manager.add_bookmark(
            url="not_a_url",
            title="Test"
        )
        self.assertFalse(success)
    
    def test_list_bookmarks(self):
        """Test listing bookmarks."""
        # Add test bookmarks
        self.manager.add_bookmark(url="https://first.com", title="First")
        self.manager.add_bookmark(url="https://second.com", title="Second")
        
        success = self.manager.list_bookmarks()
        self.assertTrue(success)
    
    def test_search_bookmarks(self):
        """Test searching bookmarks."""
        # Add test bookmarks
        self.manager.add_bookmark(url="https://python.org", title="Python Tutorial")
        self.manager.add_bookmark(url="https://javascript.com", title="JavaScript Guide")
        
        success = self.manager.search_bookmarks("python")
        self.assertTrue(success)
    
    def test_update_bookmark(self):
        """Test updating a bookmark."""
        # Add a bookmark first
        self.manager.add_bookmark(url="https://example.com", title="Original")
        
        # Update it
        success = self.manager.update_bookmark(
            identifier="1",
            title="Updated"
        )
        self.assertTrue(success)
        
        # Verify update
        bookmark = self.manager.db.get_bookmark_by_id(1)
        self.assertEqual(bookmark.title, "Updated")
    
    def test_delete_bookmark(self):
        """Test deleting a bookmark."""
        # Add a bookmark first
        self.manager.add_bookmark(url="https://example.com", title="To Delete")
        
        # Delete it
        success = self.manager.delete_bookmark("1")
        self.assertTrue(success)
        
        # Verify deletion
        bookmark = self.manager.db.get_bookmark_by_id(1)
        self.assertIsNone(bookmark)


if __name__ == '__main__':
    unittest.main()