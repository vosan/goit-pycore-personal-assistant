"""
Defines the Note class representing a single text note.

Responsibilities:
- Store note content, creation time, and optional tags.
- Provide methods for text updates and tag management.
"""

from datetime import datetime
from typing import List, Optional


class Note:
    """Represents a single note with title, content, and metadata."""
    
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None):
        """
        Initialize a new note.
        
        Args:
            title: The title of the note
            content: The text content of the note
            tags: Optional list of tags for categorization
        """
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def update_content(self, new_content: str):
        """Update the note's content and timestamp."""
        self.content = new_content
        self.updated_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str):
        """Add a tag to the note if it doesn't already exist."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().isoformat()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the note."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert note to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        """Create a Note instance from a dictionary."""
        note = cls(data["title"], data["content"], data.get("tags", []))
        note.created_at = data.get("created_at", note.created_at)
        note.updated_at = data.get("updated_at", note.updated_at)
        return note
    
    def __str__(self) -> str:
        """String representation of the note."""
        tags_str = f" [Tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"📝 {self.title}{tags_str}\n{self.content}\n📅 Created: {self.created_at[:10]}"
