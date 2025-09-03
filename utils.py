import json
import csv
import os
import re
import webbrowser
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore, Style, init
from models import Bookmark

# Initialize colorama
init(autoreset=True)


def validate_url(url: str) -> bool:
    """Validate if the given string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def fetch_title_from_url(url: str) -> Optional[str]:
    """Fetch the title of a webpage from its URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        return title.text.strip() if title else None
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not fetch title from URL: {e}")
        return None


def open_url_in_browser(url: str) -> bool:
    """Open URL in the default browser."""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error: Could not open URL in browser: {e}")
        return False


def export_to_json(bookmarks: List[Bookmark], filename: str) -> bool:
    """Export bookmarks to JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            data = [bookmark.to_dict() for bookmark in bookmarks]
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error exporting to JSON: {e}")
        return False


def export_to_csv(bookmarks: List[Bookmark], filename: str) -> bool:
    """Export bookmarks to CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'URL', 'Description', 'Tags', 'Created At', 'Updated At', 'Visit Count'])
            
            for bookmark in bookmarks:
                writer.writerow([
                    bookmark.id,
                    bookmark.title,
                    bookmark.url,
                    bookmark.description or '',
                    bookmark.tags or '',
                    bookmark.created_at.isoformat(),
                    bookmark.updated_at.isoformat(),
                    bookmark.visit_count
                ])
        return True
    except Exception as e:
        print(f"{Fore.RED}Error exporting to CSV: {e}")
        return False


def import_from_json(filename: str) -> List[Bookmark]:
    """Import bookmarks from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        bookmarks = []
        for item in data:
            bookmark = Bookmark.from_dict(item)
            bookmarks.append(bookmark)
        
        return bookmarks
    except Exception as e:
        print(f"{Fore.RED}Error importing from JSON: {e}")
        return []


def import_from_csv(filename: str) -> List[Bookmark]:
    """Import bookmarks from CSV file."""
    try:
        bookmarks = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bookmark = Bookmark(
                    id=int(row['ID']) if row['ID'] else None,
                    title=row['Title'],
                    url=row['URL'],
                    description=row['Description'] if row['Description'] else None,
                    tags=row['Tags'] if row['Tags'] else None,
                    created_at=datetime.fromisoformat(row['Created At']) if row['Created At'] else datetime.now(),
                    updated_at=datetime.fromisoformat(row['Updated At']) if row['Updated At'] else datetime.now(),
                    visit_count=int(row['Visit Count']) if row['Visit Count'] else 0
                )
                bookmarks.append(bookmark)
        
        return bookmarks
    except Exception as e:
        print(f"{Fore.RED}Error importing from CSV: {e}")
        return []


def format_bookmark_display(bookmark: Bookmark, show_id: bool = True) -> str:
    """Format a bookmark for display with colors."""
    parts = []
    
    if show_id and bookmark.id:
        parts.append(f"{Fore.CYAN}#{bookmark.id}")
    
    parts.append(f"{Fore.GREEN}{bookmark.title}")
    
    if bookmark.tags:
        parts.append(f"{Fore.YELLOW}[{bookmark.tags}]")
    
    parts.append(f"{Fore.BLUE}{bookmark.url}")
    
    if bookmark.description:
        parts.append(f"{Fore.WHITE}{bookmark.description}")
    
    parts.append(f"{Fore.MAGENTA}Visits: {bookmark.visit_count}")
    
    return ' - '.join(str(part) for part in parts)


def display_bookmarks(bookmarks: List[Bookmark], show_stats: bool = True):
    """Display a list of bookmarks with formatting."""
    if not bookmarks:
        print(f"{Fore.YELLOW}No bookmarks found.")
        return
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Bookmarks ({len(bookmarks)} items)")
    print(f"{Fore.CYAN}{'='*60}")
    
    for bookmark in bookmarks:
        print(format_bookmark_display(bookmark))
        print()
    
    if show_stats:
        total_visits = sum(b.visit_count for b in bookmarks)
        print(f"{Fore.MAGENTA}Total visits: {total_visits}")


def display_stats(stats: Dict[str, Any]):
    """Display bookmark statistics."""
    print(f"\n{Fore.CYAN}{'='*40}")
    print(f"{Fore.CYAN}Bookmark Statistics")
    print(f"{Fore.CYAN}{'='*40}")
    print(f"{Fore.GREEN}Total bookmarks: {stats['total']}")
    print(f"{Fore.GREEN}Bookmarks visited: {stats['visited']}")
    print(f"{Fore.GREEN}Max visits: {stats['max_visits']}")
    
    if stats['most_visited']:
        title, url, visits = stats['most_visited']
        print(f"{Fore.YELLOW}Most visited: {title} ({visits} visits)")
        print(f"{Fore.BLUE}  {url}")
    
    if stats['recent']:
        title, url, created = stats['recent']
        print(f"{Fore.YELLOW}Most recent: {title}")
        print(f"{Fore.BLUE}  {url}")


def display_tags(tags: List[str]):
    """Display list of tags."""
    if not tags:
        print(f"{Fore.YELLOW}No tags found.")
        return
    
    print(f"\n{Fore.CYAN}{'='*40}")
    print(f"{Fore.CYAN}Available Tags ({len(tags)})")
    print(f"{Fore.CYAN}{'='*40}")
    
    for i, tag in enumerate(tags, 1):
        print(f"{Fore.GREEN}{i:3d}. {tag}")


def confirm_action(message: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{Fore.YELLOW}{message} (y/N): ").strip().lower()
    return response in ['y', 'yes']


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def get_default_export_filename(format_type: str) -> str:
    """Get default export filename based on format and timestamp."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"bookmarks_export_{timestamp}.{format_type}"


def print_success(message: str):
    """Print success message."""
    print(f"{Fore.GREEN}✓ {message}")


def print_error(message: str):
    """Print error message."""
    print(f"{Fore.RED}✗ {message}")


def print_warning(message: str):
    """Print warning message."""
    print(f"{Fore.YELLOW}⚠ {message}")


def print_info(message: str):
    """Print info message."""
    print(f"{Fore.BLUE}ℹ {message}")


def paginate_list(items: List[Any], page: int, items_per_page: int = 10) -> List[Any]:
    """Paginate a list of items."""
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end]


def get_pagination_info(total_items: int, page: int, items_per_page: int = 10) -> Dict[str, int]:
    """Get pagination information."""
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start = (page - 1) * items_per_page + 1
    end = min(start + items_per_page - 1, total_items)
    
    return {
        'total_items': total_items,
        'total_pages': total_pages,
        'current_page': page,
        'start': start,
        'end': end,
        'items_per_page': items_per_page
    }