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
from assistant.contacts.address_book import AddressBook
from prompt_toolkit import PromptSession
from assistant.typeahead import Typeahead
from assistant.core import parse_input
from assistant.contacts.commands import register_contact_commands
from assistant.notes.commands import register_note_commands
from assistant.commands_enum import Command, COMMAND_HELP
from assistant.notes.notebook import Notebook
from assistant.storage_manager import load_data, save_data

COMMANDS = {
    Command.Contacts.ADD: None,
    Command.Contacts.CHANGE: None,
    Command.Contacts.PHONE: None,
    Command.Contacts.ALL: None,
    Command.Contacts.ADD_BIRTHDAY: None,
    Command.Contacts.SHOW_BIRTHDAY: None,
    Command.Contacts.BIRTHDAYS: None,
    Command.Notes.ADD_NOTE: None,
    Command.Notes.EDIT_NOTE: None,
    Command.Notes.DELETE_NOTE: None,
    Command.Notes.SEARCH_NOTE: None,
    Command.Notes.SHOW_NOTES: None,
}


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
    contacts_data = load_data(contacts_path, default=[])
    notes_data = load_data(notes_path, default=[])

    contacts = AddressBook()
    notes = Notebook()
    session = PromptSession()
    completer = Typeahead(hints=COMMANDS.keys())

    # Attach runtime data containers
    setattr(contacts, "data", contacts_data)
    setattr(notes, "data", notes_data)

    def persist():
        # Persist in-memory/runtime data to files
        save_data(contacts_path, getattr(contacts, "data", []))
        save_data(notes_path, getattr(notes, "data", []))

    def handle_signal(signum, frame):
        try:
            persist()
        finally:
            raise SystemExit(0)

    # Ensure data is saved on normal and signal-based termination
    atexit.register(persist)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    register_contact_commands(COMMANDS)
    register_note_commands(COMMANDS)

    try:
        while True:
            user_input = session.prompt('Enter a command: ', completer=completer)
            command, *args = parse_input(user_input)

            if command == Command.General.CLOSE:
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
                setattr(contacts, "data", sample_contacts)
                setattr(notes, "data", sample_notes)
                persist()
                print("Test data written to data/contacts.json and data/notes.json.")
                continue

            elif command == "test-get":
                print("Contacts Data:", getattr(contacts, "data", []))
                print("Notes Data:", getattr(notes, "data", []))
                continue

            elif command == Command.General.HELLO:
                print("How can I help you?")
                continue

            elif command == Command.General.HELP:
                show_help()
                continue

            if command in COMMANDS:
                handler = COMMANDS[command]
                if handler is None:
                    print("⚠️ Command not implemented yet.")
                else:
                    if isinstance(command, Command.Contacts):
                        print(handler(args, contacts))
                    elif isinstance(command, Command.Notes):
                        print(handler(args, notes))
            else:
                print("Invalid command.")
    finally:
        # Fallback persistence in case of unexpected exceptions
        persist()


if __name__ == '__main__':
    main()
