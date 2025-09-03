import sqlite3
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import Bookmark


class DatabaseManager:
    """Handles all database operations for the bookmark manager."""
    
    def __init__(self, db_path: str = "bookmarks.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the required schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    description TEXT,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    visit_count INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
    
    def add_bookmark(self, bookmark: Bookmark) -> int:
        """Add a new bookmark to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookmarks (title, url, description, tags, created_at, updated_at, visit_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                bookmark.title,
                bookmark.url,
                bookmark.description,
                bookmark.tags,
                bookmark.created_at,
                bookmark.updated_at,
                bookmark.visit_count
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_bookmark_by_id(self, bookmark_id: int) -> Optional[Bookmark]:
        """Retrieve a bookmark by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bookmarks WHERE id = ?', (bookmark_id,))
            row = cursor.fetchone()
            if row:
                return Bookmark(
                    id=row['id'],
                    title=row['title'],
                    url=row['url'],
                    description=row['description'],
                    tags=row['tags'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    visit_count=row['visit_count']
                )
            return None
    
    def get_bookmark_by_url(self, url: str) -> Optional[Bookmark]:
        """Retrieve a bookmark by its URL."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bookmarks WHERE url = ?', (url,))
            row = cursor.fetchone()
            if row:
                return Bookmark(
                    id=row['id'],
                    title=row['title'],
                    url=row['url'],
                    description=row['description'],
                    tags=row['tags'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    visit_count=row['visit_count']
                )
            return None
    
    def get_all_bookmarks(self, limit: Optional[int] = None, offset: int = 0) -> List[Bookmark]:
        """Retrieve all bookmarks with optional pagination."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM bookmarks ORDER BY created_at DESC'
            params = []
            
            if limit is not None:
                query += ' LIMIT ? OFFSET ?'
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            bookmarks = []
            for row in rows:
                bookmarks.append(Bookmark(
                    id=row['id'],
                    title=row['title'],
                    url=row['url'],
                    description=row['description'],
                    tags=row['tags'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    visit_count=row['visit_count']
                ))
            return bookmarks
    
    def search_bookmarks(self, query: str, search_in: str = 'all') -> List[Bookmark]:
        """Search bookmarks by query in specified fields."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            search_conditions = []
            params = [f'%{query}%']
            
            if search_in == 'all':
                search_conditions = [
                    'title LIKE ?',
                    'url LIKE ?',
                    'description LIKE ?',
                    'tags LIKE ?'
                ]
                params = [f'%{query}%'] * 4
            elif search_in == 'title':
                search_conditions = ['title LIKE ?']
            elif search_in == 'url':
                search_conditions = ['url LIKE ?']
            elif search_in == 'description':
                search_conditions = ['description LIKE ?']
            elif search_in == 'tags':
                search_conditions = ['tags LIKE ?']
            
            where_clause = ' OR '.join(search_conditions)
            sql = f'SELECT * FROM bookmarks WHERE {where_clause} ORDER BY created_at DESC'
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            bookmarks = []
            for row in rows:
                bookmarks.append(Bookmark(
                    id=row['id'],
                    title=row['title'],
                    url=row['url'],
                    description=row['description'],
                    tags=row['tags'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at']),
                    visit_count=row['visit_count']
                ))
            return bookmarks
    
    def update_bookmark(self, bookmark_id: int, updates: Dict[str, Any]) -> bool:
        """Update a bookmark with new values."""
        if not updates:
            return False
        
        set_clauses = []
        params = []
        
        for key, value in updates.items():
            if hasattr(Bookmark, key):
                set_clauses.append(f'{key} = ?')
                params.append(value)
        
        if not set_clauses:
            return False
        
        set_clauses.append('updated_at = ?')
        params.append(datetime.now().isoformat())
        params.append(bookmark_id)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE bookmarks SET {", ".join(set_clauses)} WHERE id = ?', params)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """Delete a bookmark by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_bookmark_by_url(self, url: str) -> bool:
        """Delete a bookmark by URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookmarks WHERE url = ?', (url,))
            conn.commit()
            return cursor.rowcount > 0
    
    def increment_visit_count(self, bookmark_id: int) -> bool:
        """Increment the visit count for a bookmark."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE bookmarks SET visit_count = visit_count + 1 WHERE id = ?', (bookmark_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_bookmark_stats(self) -> Dict[str, Any]:
        """Get statistics about bookmarks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM bookmarks')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) as total FROM bookmarks WHERE visit_count > 0')
            visited = cursor.fetchone()[0]
            
            cursor.execute('SELECT MAX(visit_count) as max_visits FROM bookmarks')
            max_visits = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT title, url, visit_count FROM bookmarks ORDER BY visit_count DESC LIMIT 1')
            most_visited = cursor.fetchone()
            
            cursor.execute('SELECT title, url, created_at FROM bookmarks ORDER BY created_at DESC LIMIT 1')
            recent = cursor.fetchone()
            
            return {
                'total': total,
                'visited': visited,
                'max_visits': max_visits,
                'most_visited': most_visited,
                'recent': recent
            }
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags from bookmarks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT tags FROM bookmarks WHERE tags IS NOT NULL')
            rows = cursor.fetchall()
            
            tags = set()
            for row in rows:
                if row[0]:
                    tags.update(tag.strip() for tag in row[0].split(','))
            
            return sorted(list(tags))
    
    def get_total_count(self) -> int:
        """Get total number of bookmarks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM bookmarks')
            return cursor.fetchone()[0]