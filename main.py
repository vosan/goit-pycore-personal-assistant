"""
Entry point for the Personal Assistant application.

Responsibilities:
- Display the welcome message and main input loop.
- Parse user input using `parse_input()` from `assistant.core`.
- Route commands to the appropriate functions (contacts or notes modules).
- Manage application lifecycle (start, exit, etc.).
"""
import atexit
import signal
from pathlib import Path
import sys
from assistant.contacts.address_book import AddressBook
from prompt_toolkit import PromptSession
from assistant.typeahead import Typeahead
from assistant.core import parse_input
from assistant.contacts.commands import register_contact_commands
from assistant.notes.commands import register_note_commands
from assistant.commands_enum import Command, COMMAND_HELP
from assistant.notes.notebook import Notebook
from assistant.storage_manager import load_data, save_data

# Command registry (populated by register_* functions)
COMMANDS = {}


def show_help():
    """Display help with all commands, parameters, and descriptions."""
    print("\n" + "=" * 70)
    print("📚 Personal Assistant - Available Commands")
    print("=" * 70)

    print("\n📞 Contact Management:")
    for cmd in Command.Contacts:
        help_info = COMMAND_HELP[cmd]
        print(help_info.format(cmd.value, width=45))

    print("\n📝 Note Management:")
    for cmd in Command.Notes:
        help_info = COMMAND_HELP[cmd]
        print(help_info.format(cmd.value, width=45))

    print("\n⚙️ General:")
    for cmd in Command.General:
        help_info = COMMAND_HELP[cmd]
        print(help_info.format(cmd.value, width=45))

    print("\n" + "=" * 70)
    print("Legend:")
    print("  <parameter>  Required parameter")
    print("  [parameter]  Optional parameter")
    print("=" * 70 + "\n")


def main():
    print("Welcome to the Personal Assistant!")

    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"
    contacts_path = data_dir / "contacts.json"
    notes_path = data_dir / "notes.json"

    # Load persisted data (create files with defaults if missing)
    contacts_data = load_data(contacts_path, default={})
    notes_data = load_data(notes_path, default={})

    contacts = AddressBook()
    notes = Notebook()
    # Use prompt_toolkit only for interactive terminals to avoid warnings like
    # "Warning: Input is not a terminal (fd=0)."
    is_tty = sys.stdin.isatty() and sys.stdout.isatty()
    session = PromptSession() if is_tty else None

    # Initialize in-memory data from persisted storage
    if isinstance(contacts_data, dict):
        contacts.from_dict(contacts_data)
    elif isinstance(contacts_data, list):
        # Backward-compatible shape
        contacts.from_list(contacts_data)

    if isinstance(notes_data, dict):
        notes.from_dict(notes_data)

    def persist():
        # Persist in-memory/runtime data to files
        save_data(contacts_path, contacts.to_dict())
        save_data(notes_path, notes.to_dict())

    def handle_signal(signum, frame):
        try:
            persist()
        finally:
            raise SystemExit(0)

    # Ensure data is saved on normal and signal-based termination
    atexit.register(persist)
    try:
        signal.signal(signal.SIGINT, handle_signal)
    except Exception:
        pass
    try:
        signal.signal(signal.SIGTERM, handle_signal)
    except Exception:
        pass

    register_contact_commands(COMMANDS)
    register_note_commands(COMMANDS)

    # Map raw command strings to their Enum counterparts for reliable dispatch
    value_to_enum = {}
    for group in (Command.Contacts, Command.Notes, Command.General):
        for cmd in group:
            value_to_enum[cmd.value] = cmd

    # Initialize completer after registration using all known command names
    if is_tty:
        all_hints = [
            *[cmd.value for cmd in Command.Contacts],
            *[cmd.value for cmd in Command.Notes],
            *[cmd.value for cmd in Command.General],
            # helper/testing commands
            "test-set",
            "test-get",
        ]
        completer = Typeahead(hints=all_hints)
    else:
        completer = None

    try:
        while True:
            if is_tty:
                user_input = session.prompt('Enter a command: ', completer=completer)
            else:
                try:
                    user_input = input('> ')
                except EOFError:
                    break

            # Skip empty or whitespace-only inputs without error
            if not user_input or not user_input.strip():
                continue

            command, *args = parse_input(user_input)
            cmd_enum = value_to_enum.get(command)

            if cmd_enum == Command.General.CLOSE:
                print("Good bye!")
                persist()
                break

            elif command == "test-set":
                sample_contacts = [
                    {"name": "Alice", "phones": ["0123456789"], "birthday": "12.11.1990"},
                    {"name": "Bob", "phones": ["0987654321"], "birthday": None},
                ]
                sample_notes = [
                    {"title": "Welcome", "content": "First note", "tags": ["intro", "test"]}
                ]
                contacts.from_list(sample_contacts)
                # Convert notes list into dict shape keyed by title
                notes.from_dict({item["title"]: item for item in sample_notes})
                persist()
                print("Test data written to data/contacts.json and data/notes.json.")
                continue

            elif command == "test-get":
                print("Contacts Data:", contacts.to_dict())
                print("Notes Data:", notes.to_dict())
                continue

            elif cmd_enum == Command.General.HELLO:
                print("How can I help you?")
                continue

            elif cmd_enum == Command.General.HELP:
                show_help()
                continue

            if cmd_enum in COMMANDS:
                handler = COMMANDS[cmd_enum]
                if handler is None:
                    print("⚠️ Command not implemented yet.")
                else:
                    if isinstance(cmd_enum, Command.Contacts):
                        result = handler(args, contacts)
                    elif isinstance(cmd_enum, Command.Notes):
                        result = handler(args, notes)
                    else:
                        result = None

                    if result is not None:
                        print(str(result).rstrip())
            else:
                # Only report invalid for non-empty commands
                print("Unknown command. Type 'help' to see available commands.")
    finally:
        # Fallback persistence in case of unexpected exceptions
        persist()


if __name__ == '__main__':
    main()
