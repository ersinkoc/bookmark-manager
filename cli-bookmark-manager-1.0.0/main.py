#!/usr/bin/env python3

import argparse
import sys
import os
from typing import Optional, List
from datetime import datetime
from colorama import Fore

# Handle Windows path issues
if os.name == 'nt':  # Windows
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules directly for Windows compatibility
from database import DatabaseManager
from models import Bookmark
from utils import (
    validate_url, fetch_title_from_url, open_url_in_browser,
    export_to_json, export_to_csv, import_from_json, import_from_csv,
    display_bookmarks, display_stats, display_tags,
    print_success, print_error, print_warning, print_info,
    paginate_list, get_pagination_info, confirm_action
)


class BookmarkManager:
    """Main bookmark manager CLI application."""
    
    def __init__(self, db_path: str = "bookmarks.db"):
        # Handle Windows path
        if os.name == 'nt' and not os.path.isabs(db_path):
            # Use user's home directory on Windows
            home_dir = os.path.expanduser("~")
            db_path = os.path.join(home_dir, db_path)
        
        self.db = DatabaseManager(db_path)
    
    def add_bookmark(self, url: str, title: Optional[str] = None, 
                    description: Optional[str] = None, tags: Optional[str] = None,
                    fetch_title: bool = False) -> bool:
        """Add a new bookmark."""
        if not validate_url(url):
            print_error(f"Invalid URL: {url}")
            return False
        
        # Check if URL already exists
        existing = self.db.get_bookmark_by_url(url)
        if existing:
            print_error(f"Bookmark with this URL already exists (ID: {existing.id})")
            return False
        
        # Fetch title if requested and not provided
        if fetch_title and not title:
            print_info("Fetching title from webpage...")
            title = fetch_title_from_url(url)
        
        if not title:
            title = url
        
        bookmark = Bookmark(
            title=title,
            url=url,
            description=description,
            tags=tags,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        bookmark_id = self.db.add_bookmark(bookmark)
        if bookmark_id:
            print_success(f"Bookmark added successfully (ID: {bookmark_id})")
            return True
        else:
            print_error("Failed to add bookmark")
            return False
    
    def list_bookmarks(self, limit: Optional[int] = None, page: int = 1) -> bool:
        """List bookmarks with pagination."""
        offset = (page - 1) * (limit or 10) if limit else 0
        bookmarks = self.db.get_all_bookmarks(limit=limit, offset=offset)
        
        if not bookmarks:
            print_warning("No bookmarks found")
            return False
        
        display_bookmarks(bookmarks, show_stats=False)
        
        # Show pagination info
        total_count = self.db.get_total_count()
        if limit and total_count > limit:
            pagination_info = get_pagination_info(total_count, page, limit or 10)
            print(f"\n{Fore.BLUE}Page {pagination_info['current_page']} of {pagination_info['total_pages']}")
            print(f"Showing bookmarks {pagination_info['start']}-{pagination_info['end']} of {pagination_info['total_items']}")
        
        return True
    
    def search_bookmarks(self, query: str, search_in: str = 'all') -> bool:
        """Search bookmarks."""
        if not query.strip():
            print_error("Search query cannot be empty")
            return False
        
        bookmarks = self.db.search_bookmarks(query, search_in)
        
        if not bookmarks:
            print_warning(f"No bookmarks found matching '{query}'")
            return False
        
        print_info(f"Found {len(bookmarks)} bookmarks matching '{query}'")
        display_bookmarks(bookmarks, show_stats=False)
        return True
    
    def update_bookmark(self, identifier: str, title: Optional[str] = None,
                       url: Optional[str] = None, description: Optional[str] = None,
                       tags: Optional[str] = None) -> bool:
        """Update a bookmark."""
        # Find bookmark by ID or URL
        bookmark = None
        if identifier.isdigit():
            bookmark = self.db.get_bookmark_by_id(int(identifier))
        else:
            bookmark = self.db.get_bookmark_by_url(identifier)
        
        if not bookmark:
            print_error(f"Bookmark not found: {identifier}")
            return False
        
        # Validate new URL if provided
        if url and url != bookmark.url:
            if not validate_url(url):
                print_error(f"Invalid URL: {url}")
                return False
            
            # Check if new URL already exists
            existing = self.db.get_bookmark_by_url(url)
            if existing and existing.id != bookmark.id:
                print_error(f"Bookmark with this URL already exists (ID: {existing.id})")
                return False
        
        # Build updates dict
        updates = {}
        if title is not None:
            updates['title'] = title
        if url is not None:
            updates['url'] = url
        if description is not None:
            updates['description'] = description
        if tags is not None:
            updates['tags'] = tags
        
        if not updates:
            print_warning("No updates specified")
            return False
        
        if self.db.update_bookmark(bookmark.id, updates):
            print_success(f"Bookmark updated successfully (ID: {bookmark.id})")
            return True
        else:
            print_error("Failed to update bookmark")
            return False
    
    def delete_bookmark(self, identifier: str) -> bool:
        """Delete a bookmark."""
        # Find bookmark by ID or URL
        bookmark = None
        if identifier.isdigit():
            bookmark = self.db.get_bookmark_by_id(int(identifier))
        else:
            bookmark = self.db.get_bookmark_by_url(identifier)
        
        if not bookmark:
            print_error(f"Bookmark not found: {identifier}")
            return False
        
        # Show bookmark details
        print_info("Bookmark to delete:")
        print(f"  {bookmark}")
        
        if not confirm_action("Are you sure you want to delete this bookmark?"):
            print_info("Deletion cancelled")
            return False
        
        # Delete by ID or URL
        if identifier.isdigit():
            success = self.db.delete_bookmark(int(identifier))
        else:
            success = self.db.delete_bookmark_by_url(identifier)
        
        if success:
            print_success("Bookmark deleted successfully")
            return True
        else:
            print_error("Failed to delete bookmark")
            return False
    
    def open_bookmark(self, identifier: str) -> bool:
        """Open bookmark in browser."""
        # Find bookmark by ID or URL
        bookmark = None
        if identifier.isdigit():
            bookmark = self.db.get_bookmark_by_id(int(identifier))
        else:
            bookmark = self.db.get_bookmark_by_url(identifier)
        
        if not bookmark:
            print_error(f"Bookmark not found: {identifier}")
            return False
        
        print_info(f"Opening: {bookmark.title}")
        
        if open_url_in_browser(bookmark.url):
            self.db.increment_visit_count(bookmark.id)
            print_success("Bookmark opened in browser")
            return True
        else:
            print_error("Failed to open bookmark")
            return False
    
    def export_bookmarks(self, format_type: str, filename: Optional[str] = None) -> bool:
        """Export bookmarks to file."""
        bookmarks = self.db.get_all_bookmarks()
        
        if not bookmarks:
            print_warning("No bookmarks to export")
            return False
        
        if not filename:
            filename = get_default_export_filename(format_type)
        
        # Handle Windows path
        if os.name == 'nt' and not os.path.isabs(filename):
            # Use current directory
            filename = os.path.join(os.getcwd(), filename)
        
        if format_type.lower() == 'json':
            success = export_to_json(bookmarks, filename)
        elif format_type.lower() == 'csv':
            success = export_to_csv(bookmarks, filename)
        else:
            print_error(f"Unsupported export format: {format_type}")
            return False
        
        if success:
            print_success(f"Exported {len(bookmarks)} bookmarks to {filename}")
            return True
        else:
            return False
    
    def import_bookmarks(self, filename: str) -> bool:
        """Import bookmarks from file."""
        # Handle Windows path
        if os.name == 'nt' and not os.path.isabs(filename):
            filename = os.path.join(os.getcwd(), filename)
        
        if not os.path.exists(filename):
            print_error(f"File not found: {filename}")
            return False
        
        if filename.endswith('.json'):
            bookmarks = import_from_json(filename)
        elif filename.endswith('.csv'):
            bookmarks = import_from_csv(filename)
        else:
            print_error(f"Unsupported file format: {filename}")
            return False
        
        if not bookmarks:
            print_error("No bookmarks found in file")
            return False
        
        imported_count = 0
        skipped_count = 0
        
        for bookmark in bookmarks:
            # Check if URL already exists
            existing = self.db.get_bookmark_by_url(bookmark.url)
            if existing:
                print_warning(f"Skipping duplicate: {bookmark.url}")
                skipped_count += 1
                continue
            
            # Reset ID for new insertion
            bookmark.id = None
            bookmark.created_at = datetime.now()
            bookmark.updated_at = datetime.now()
            
            if self.db.add_bookmark(bookmark):
                imported_count += 1
        
        print_success(f"Imported {imported_count} bookmarks, skipped {skipped_count} duplicates")
        return imported_count > 0
    
    def show_stats(self) -> bool:
        """Show bookmark statistics."""
        stats = self.db.get_bookmark_stats()
        display_stats(stats)
        return True
    
    def show_tags(self) -> bool:
        """Show all unique tags."""
        tags = self.db.get_all_tags()
        display_tags(tags)
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CLI Bookmark Manager - Save, organize, and manage your bookmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add --url "https://github.com" --title "GitHub" --tags "dev,git"
  %(prog)s search "python" --in all
  %(prog)s list --limit 10 --page 1
  %(prog)s update 1 --title "New Title"
  %(prog)s delete 1
  %(prog)s open 1
  %(prog)s export --format json --file bookmarks.json
  %(prog)s import --file bookmarks.json
  %(prog)s stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new bookmark')
    add_parser.add_argument('--url', required=True, help='URL of the bookmark')
    add_parser.add_argument('--title', help='Title of the bookmark')
    add_parser.add_argument('--description', help='Description of the bookmark')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--fetch-title', action='store_true', 
                           help='Fetch title from webpage if not provided')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List bookmarks')
    list_parser.add_argument('--limit', type=int, help='Number of bookmarks to show')
    list_parser.add_argument('--page', type=int, default=1, help='Page number for pagination')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search bookmarks')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--in', choices=['title', 'url', 'description', 'tags', 'all'],
                             default='all', help='Field to search in')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a bookmark')
    update_parser.add_argument('identifier', help='Bookmark ID or URL')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--url', help='New URL')
    update_parser.add_argument('--description', help='New description')
    update_parser.add_argument('--tags', help='New tags')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a bookmark')
    delete_parser.add_argument('identifier', help='Bookmark ID or URL')
    
    # Open command
    open_parser = subparsers.add_parser('open', help='Open bookmark in browser')
    open_parser.add_argument('identifier', help='Bookmark ID or URL')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export bookmarks')
    export_parser.add_argument('--format', choices=['json', 'csv'], required=True,
                               help='Export format')
    export_parser.add_argument('--file', help='Output filename')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import bookmarks')
    import_parser.add_argument('--file', required=True, help='Input filename')
    
    # Stats command
    subparsers.add_parser('stats', help='Show bookmark statistics')
    
    # Tags command
    subparsers.add_parser('tags', help='List all unique tags')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        manager = BookmarkManager()
        
        if args.command == 'add':
            success = manager.add_bookmark(
                url=args.url,
                title=args.title,
                description=args.description,
                tags=args.tags,
                fetch_title=args.fetch_title
            )
        
        elif args.command == 'list':
            success = manager.list_bookmarks(limit=args.limit, page=args.page)
        
        elif args.command == 'search':
            success = manager.search_bookmarks(args.query, getattr(args, 'in'))
        
        elif args.command == 'update':
            success = manager.update_bookmark(
                identifier=args.identifier,
                title=args.title,
                url=args.url,
                description=args.description,
                tags=args.tags
            )
        
        elif args.command == 'delete':
            success = manager.delete_bookmark(args.identifier)
        
        elif args.command == 'open':
            success = manager.open_bookmark(args.identifier)
        
        elif args.command == 'export':
            success = manager.export_bookmarks(args.format, args.file)
        
        elif args.command == 'import':
            success = manager.import_bookmarks(args.file)
        
        elif args.command == 'stats':
            success = manager.show_stats()
        
        elif args.command == 'tags':
            success = manager.show_tags()
        
        else:
            print_error(f"Unknown command: {args.command}")
            return 1
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print_info("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print_error(f"An error occurred: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())