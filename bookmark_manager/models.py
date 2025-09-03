from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Bookmark:
    """Represents a bookmark with all its properties."""
    id: Optional[int] = None
    title: str = ""
    url: str = ""
    description: Optional[str] = None
    tags: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    visit_count: int = 0
    
    def get_tags_list(self) -> List[str]:
        """Get tags as a list of strings."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list: List[str]):
        """Set tags from a list of strings."""
        self.tags = ','.join(tag.strip() for tag in tags_list if tag.strip())
    
    def to_dict(self) -> dict:
        """Convert bookmark to dictionary for export."""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'tags': self.get_tags_list(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'visit_count': self.visit_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Bookmark':
        """Create bookmark from dictionary."""
        tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        
        return cls(
            id=data.get('id'),
            title=data['title'],
            url=data['url'],
            description=data.get('description'),
            tags=tags,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now(),
            visit_count=data.get('visit_count', 0)
        )
    
    def __str__(self) -> str:
        """String representation of bookmark."""
        tags_str = f" [{self.tags}]" if self.tags else ""
        return f"#{self.id}: {self.title}{tags_str} - {self.url}"
    
    def __repr__(self) -> str:
        """Debug representation of bookmark."""
        return f"Bookmark(id={self.id}, title='{self.title}', url='{self.url}')"