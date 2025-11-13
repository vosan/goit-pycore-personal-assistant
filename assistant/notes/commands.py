"""
Implements all command functions for managing notes.

Functions might include:
- add_note()
- edit_note()
- delete_note()
- search_notes()
- show_all_notes()
- etc.

Responsibilities:
- Parse user arguments and call appropriate methods on Notebook.
- Return text responses for CLI output.
"""

from typing import List
from assistant.commands_enum import Command
from assistant.notes.notebook import Notebook
from assistant.core import input_error


@input_error
def add_note(args: List[str], notebook: Notebook) -> str:
    """
    Add a new note.
    
    Args:
        args: [title, content, ...]
        notebook: The notebook instance
        
    Returns:
        Success or error message
    """
    if len(args) < 2:
        return "Error: Please provide both title and content.\nUsage: add-note <title> <content>"
    
    title = args[0]
    content = " ".join(args[1:])
    
    return notebook.add_note(title, content)


@input_error
def edit_note(args: List[str], notebook: Notebook) -> str:
    """
    Edit an existing note's content.
    
    Args:
        args: [title, new_content, ...]
        notebook: The notebook instance
        
    Returns:
        Success or error message
    """
    if len(args) < 2:
        return "Error: Please provide both title and new content.\nUsage: edit-note <title> <new_content>"
    
    title = args[0]
    new_content = " ".join(args[1:])
    
    return notebook.edit_note(title, new_content)


@input_error
def delete_note(args: List[str], notebook: Notebook) -> str:
    """
    Delete a note.
    
    Args:
        args: [title]
        notebook: The notebook instance
        
    Returns:
        Success or error message
    """
    if len(args) < 1:
        return "Error: Please provide the note title.\nUsage: delete-note <title>"
    
    title = args[0]
    return notebook.delete_note(title)


@input_error
def search_notes(args: List[str], notebook: Notebook) -> str:
    """
    Search notes by keyword.
    
    Args:
        args: [keyword]
        notebook: The notebook instance
        
    Returns:
        List of matching notes or error message
    """
    if len(args) < 1:
        return "Error: Please provide a search keyword.\nUsage: search-note <keyword>"
    
    keyword = args[0]
    matching_notes = notebook.search_notes(keyword)
    
    if not matching_notes:
        return f"No notes found containing '{keyword}'."
    
    result = [f"Found {len(matching_notes)} note(s) containing '{keyword}':\n"]
    result.append("=" * 70)
    
    for note in matching_notes:
        result.append(f"\n{note}")
        result.append("-" * 70)
    
    return "\n".join(result)


@input_error
def show_all_notes(args: List[str], notebook: Notebook) -> str:
    """
    Display all notes.
    
    Args:
        args: Not used
        notebook: The notebook instance
        
    Returns:
        List of all notes or message if empty
    """
    notes = notebook.get_all_notes()
    
    if not notes:
        return "No notes found. Add your first note with: add-note <title> <content>"
    
    result = [f"All Notes ({len(notes)} total):\n"]
    result.append("=" * 70)
    
    for note in notes:
        result.append(f"\n{note}")
        result.append("-" * 70)
    
    return "\n".join(result)


def register_note_commands(commands):
    """Register commands in the main command dispatcher."""
    commands[Command.Notes.ADD_NOTE] = add_note
    commands[Command.Notes.EDIT_NOTE] = edit_note
    commands[Command.Notes.DELETE_NOTE] = delete_note
    commands[Command.Notes.SEARCH_NOTE] = search_notes
    commands[Command.Notes.SHOW_NOTES] = show_all_notes