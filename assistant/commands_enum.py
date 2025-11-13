"""
Command enumeration for the Personal Assistant application.

Centralizes all CLI command definitions to ensure consistency
across the codebase and provide type safety.
"""

from enum import Enum
from dataclasses import dataclass


class Command:
    """
    Namespace for all CLI commands organized by category.
    
    Usage:
        Command.Contacts.ADD
        Command.Notes.EDIT_NOTE
        Command.General.EXIT
    """
    
    class Contacts(str, Enum):
        """Contact management commands."""
        ADD = "add"
        CHANGE = "change"
        PHONE = "phone"
        ALL = "all"
        ADD_BIRTHDAY = "add-birthday"
        SHOW_BIRTHDAY = "show-birthday"
        BIRTHDAYS = "birthdays"
        ADD_EMAIL = "add-email"
        ADD_ADDRESS = "add-address"
    
    class Notes(str, Enum):
        """Note management commands."""
        ADD_NOTE = "add-note"
        EDIT_NOTE = "edit-note"
        DELETE_NOTE = "delete-note"
        SEARCH_NOTE = "search-note"
        SHOW_NOTES = "show-notes"
    
    class General(str, Enum):
        """General commands."""
        HELLO = "hello"
        HELP = "help"
        CLOSE = "close"


@dataclass
class CommandHelp:
    """Command help information including parameters and description."""
    params: str
    description: str
    
    def format(self, command_name: str, width: int = 40) -> str:
        """Format command help for display."""
        cmd_with_params = f"{command_name} {self.params}".strip()
        return f"  {cmd_with_params:.<{width}} {self.description}"


# Command help information
COMMAND_HELP = {
    # Contact commands
    Command.Contacts.ADD: CommandHelp(
        params="<name> <phone>",
        description="Add a new contact"
    ),
    Command.Contacts.CHANGE: CommandHelp(
        params="<name> <old_phone> <new_phone>",
        description="Change contact's phone number"
    ),
    Command.Contacts.PHONE: CommandHelp(
        params="<name>",
        description="Show phone number(s) for a contact"
    ),
    Command.Contacts.ALL: CommandHelp(
        params="",
        description="Show all contacts"
    ),
    Command.Contacts.ADD_BIRTHDAY: CommandHelp(
        params="<name> <DD.MM.YYYY>",
        description="Add birthday to a contact"
    ),
    Command.Contacts.SHOW_BIRTHDAY: CommandHelp(
        params="<name>",
        description="Show birthday for a contact"
    ),
    Command.Contacts.BIRTHDAYS: CommandHelp(
        params="[days]",
        description="Show upcoming birthdays (default: 7 days)"
    ),
    Command.Contacts.ADD_EMAIL: CommandHelp(
        params="<name> <email>",
        description="Add or update a contact's email"
    ),
    Command.Contacts.ADD_ADDRESS: CommandHelp(
        params="<name> <address>",
        description="Add or update a contact's address"
    ),
    
    # Note commands
    Command.Notes.ADD_NOTE: CommandHelp(
        params="<title> <content>",
        description="Add a new note"
    ),
    Command.Notes.EDIT_NOTE: CommandHelp(
        params="<title> <new_content>",
        description="Edit an existing note"
    ),
    Command.Notes.DELETE_NOTE: CommandHelp(
        params="<title>",
        description="Delete a note"
    ),
    Command.Notes.SEARCH_NOTE: CommandHelp(
        params="<keyword>",
        description="Search notes by keyword"
    ),
    Command.Notes.SHOW_NOTES: CommandHelp(
        params="",
        description="Show all notes"
    ),
    
    # General commands
    Command.General.HELLO: CommandHelp(
        params="",
        description="Greet the assistant"
    ),
    Command.General.HELP: CommandHelp(
        params="",
        description="Show this help message"
    ),
    Command.General.CLOSE: CommandHelp(
        params="",
        description="Close the assistant"
    ),
}


def get_command_help(command: str | Enum) -> CommandHelp | None:
    """Get help information for a command."""
    return COMMAND_HELP.get(command)
