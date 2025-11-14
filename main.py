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
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import CompleteStyle
import os

# Command registry (populated by register_* functions)
COMMANDS = {}

# Rotating phrases for the `hello` command
GREETINGS = [
    "Hello! How can I help you?",
    "Hi there! What can I do for you today?",
    "Greetings! Ready when you are."
]

GREETING_JOKES = [
    "Why did the computer show up at work late? It had a hard drive.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people: those who understand binary and those who don’t.",
    "I tried to catch some fog earlier. I mist."
]


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
    show_help()
    print("\033[1;36mWelcome to the Personal Assistant!\033[0m")  # bold cyan

    def clear_screen():
        """Clear the terminal screen and scrollback buffer."""
        # ANSI escape sequences to clear scrollback (3J), move cursor home (H), and clear screen (2J)
        sys.stdout.write("\033[3J\033[H\033[2J")
        sys.stdout.flush()

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
    # Reserve some lines for the completion menu so there's always space at the
    # bottom for hints. Make it configurable via PA_MENU_RESERVE. Default: 6.
    reserve_env = os.environ.get("PA_MENU_RESERVE", "6")
    try:
        reserve_lines = int(reserve_env)
    except ValueError:
        reserve_lines = 6
    if reserve_lines < 0:
        reserve_lines = 0
    if reserve_lines > 20:
        reserve_lines = 20

    session = (
        PromptSession(
            reserve_space_for_menu=reserve_lines,
            complete_while_typing=True,
            mouse_support=False,
            enable_history_search=False,
            # Use a menu style that adapts to space; in TTY it'll render nicely.
            complete_style=CompleteStyle.MULTI_COLUMN if is_tty else CompleteStyle.READLINE_LIKE,
        )
        if is_tty
        else None
    )

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
        ]
        completer = Typeahead(hints=all_hints)
    else:
        completer = None

    # State for tracking consecutive `hello` commands
    last_command_was_hello = False
    hello_streak = 0
    greet_index = 0
    joke_index = 0

    try:
        while True:
            if is_tty:
                with patch_stdout(raw=True):
                    user_input = session.prompt('> ', completer=completer)
            else:
                try:
                    user_input = input()
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

            elif cmd_enum == Command.General.HELLO:
                # Maintain a streak counter for consecutive `hello` calls
                if last_command_was_hello:
                    hello_streak += 1
                else:
                    hello_streak = 1

                # First 3 consecutive hellos → rotate through greetings; afterwards → jokes
                if hello_streak <= 3:
                    phrase = GREETINGS[greet_index % len(GREETINGS)] if GREETINGS else "Hello!"
                    greet_index = (greet_index + 1) % max(1, len(GREETINGS))
                else:
                    phrase = GREETING_JOKES[joke_index % len(GREETING_JOKES)] if GREETING_JOKES else "Hello again!"
                    joke_index = (joke_index + 1) % max(1, len(GREETING_JOKES))

                print(phrase)
                last_command_was_hello = True
                continue

            elif cmd_enum == Command.General.HELP:
                # Reset the streak on a different valid command
                last_command_was_hello = False
                hello_streak = 0
                greet_index = 0
                joke_index = 0
                show_help()
                continue

            elif cmd_enum == Command.General.CLEAR:
                # Reset hello streak and clear the screen
                last_command_was_hello = False
                hello_streak = 0
                greet_index = 0
                joke_index = 0
                clear_screen()
                continue

            if cmd_enum in COMMANDS:
                handler = COMMANDS[cmd_enum]
                if handler is None:
                    print("⚠️ Command not implemented yet.")
                else:
                    # Any valid non-hello command resets the streak
                    last_command_was_hello = False
                    hello_streak = 0
                    greet_index = 0
                    joke_index = 0
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
                # Reset the hello streak on any different (even unknown) command
                last_command_was_hello = False
                hello_streak = 0
                greet_index = 0
                joke_index = 0
                print("Unknown command. Type 'help' to see available commands.")
    finally:
        # Fallback persistence in case of unexpected exceptions
        persist()


if __name__ == '__main__':
    main()
