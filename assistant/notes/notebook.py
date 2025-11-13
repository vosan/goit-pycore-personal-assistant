"""
Defines the Notebook class, which manages multiple Note objects.

Responsibilities:
- Store, retrieve, edit, and delete notes.
- Support search and filter operations (e.g., by keyword or tag).
"""

from typing import Optional, Dict, List
from assistant.notes.note import Note


class Notebook:
    """Manages a collection of notes."""
    
    def __init__(self):
        """Initialize an empty notebook."""
        self.notes: Dict[str, Note] = {}
    
    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> str:
        """
        Add a new note to the notebook.
        
        Args:
            title: The title of the note (used as unique identifier)
            content: The text content of the note
            tags: Optional list of tags
            
        Returns:
            Success or error message
        """
        if title in self.notes:
            return f"Note with title '{title}' already exists."
        
        self.notes[title] = Note(title, content, tags)
        return f"Note '{title}' added successfully."
    
    def get_note(self, title: str) -> Optional[Note]:
        """Get a note by title."""
        return self.notes.get(title)
    
    def edit_note(self, title: str, new_content: str) -> str:
        """
        Edit an existing note's content.
        
        Args:
            title: The title of the note to edit
            new_content: The new content for the note
            
        Returns:
            Success or error message
        """
        if title not in self.notes:
            return f"Note '{title}' not found."
        
        self.notes[title].update_content(new_content)
        return f"Note '{title}' updated successfully."
    
    def delete_note(self, title: str) -> str:
        """
        Delete a note from the notebook.
        
        Args:
            title: The title of the note to delete
            
        Returns:
            Success or error message
        """
        if title not in self.notes:
            return f"Note '{title}' not found."
        
        del self.notes[title]
        return f"Note '{title}' deleted successfully."
    
    def search_notes(self, keyword: str) -> List[Note]:
        """
        Search for notes containing a keyword in title or content.
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            List of matching notes
        """
        keyword_lower = keyword.lower()
        return [
            note for note in self.notes.values()
            if keyword_lower in note.title.lower() or keyword_lower in note.content.lower()
        ]
    
    def get_all_notes(self) -> List[Note]:
        """Get all notes in the notebook."""
        return list(self.notes.values())
    
    def to_dict(self) -> dict:
        """Convert notebook to dictionary for JSON serialization."""
        return {title: note.to_dict() for title, note in self.notes.items()}
    
    def from_dict(self, data: dict):
        """Load notebook from dictionary."""
        self.notes = {title: Note.from_dict(note_data) for title, note_data in data.items()}
    
    def __len__(self) -> int:
        """Return the number of notes."""
        return len(self.notes)
