"""
Implements all command functions related to contact management.

Functions:
- add_contact()
- change_contact()
- show_phone()
- show_all()
- add_birthday()
- show_birthday()
- birthdays()
- delete_contact()
- etc.

Responsibilities:
- Parse and validate command arguments.
- Interact with the AddressBook and Record classes.
- Return text messages to be printed by main.py.
"""

from assistant.commands_enum import Command
from assistant.core import input_error
from assistant.contacts.record import Record
from assistant.contacts.utils import format_contact


@input_error
def add_contact(args, book):
    """Add a new contact or phone number."""
    if len(args) < 2 or len(args[1])!= 10 or not args[1].isdigit():
        return "Usage: add [name] [phone number] with 10 digits"
    name, phone = args[0], args[1]
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} created."
    else:
        message = f"Contact {name} updated."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    """Edit an existing contact's phone number."""
    if len(args) != 3:
        return "Usage: change [name] [old phone] [new phone]"
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone number for {name} has been changed."


@input_error
def show_phone(args, book):
    """Show all phone numbers for a contact."""
    if len(args) != 1:
        return "Usage: phone <name> <phone>"
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    # Always show in formatted block; show only the requested field
    return format_contact(record, include_fields=["phones"])


@input_error
def show_all(args, book):
    """Display all contacts in the address book."""
    if not book.data:
        return "The contact list is empty."
    blocks = [format_contact(record) for record in book.data.values()]
    return "\n\n".join(blocks)


@input_error
def add_birthday(args, book):
    """Add a birthday to a contact."""
    if len(args) != 2:
        return "Usage: add-birthday [name] [date in DD.MM.YYYY format]"
    name, bday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(bday)
    return f"Birthday for {name} has been added."


@input_error
def show_birthday(args, book):
    """Show the birthday of a contact."""
    if len(args) != 1:
        return "Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    # Show formatted block with only birthday; if absent, shows "not specified"
    return format_contact(record, include_fields=["birthday"])


@input_error
def birthdays(args, book):
    """Show contacts with upcoming birthdays."""
    days = int(args[0]) if args else 7
    # Ensure non-negative day window
    window = max(days, 0)
    result = book.get_upcoming_birthdays(window)
    if not result:
        suffix = "day" if window == 1 else "days"
        return f"No birthdays within the next {window} {suffix}."
    blocks = []
    for name, date in result.items():
        rec = book.find(name)
        if rec:
            blocks.append(format_contact(rec, include_fields=["birthday"], birthday_override=date))
        else:
            # Fallback in case of mismatch
            blocks.append(f"{name}: {date}")
    return "\n\n".join(blocks)


@input_error
def add_email(args, book):
    """Add an email to a contact."""
    if len(args) != 2:
        return "Usage: add-email [name] [email]"
    name, email = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_email(email)
    return f"Email for {name} has been added."


@input_error
def add_address(args, book):
    """Add a physical address to a contact."""
    if len(args) < 2:
        return "Usage: add-address [name] [address]"
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_address(address)
    return f"Address for {name} has been added."


@input_error
def delete_contact(args, book):
    """Delete a contact by name.

    Usage: delete-contact [name]
    """
    if len(args) != 1:
        return "Usage: delete-contact [name]"
    name = args[0]
    deleted = book.delete(name)
    if deleted:
        return f"Contact {name} deleted."
    return "Contact not found."

@input_error
def search_contacts(args, book):
    """Search contacts by name, phone, email, or address.

    Usage: search-contacts <query>
    """
    if not args:
        return "Usage: search-contacts <query>"
    query = " ".join(args).strip()
    ql = query.lower()
    matches = []

    for contact in book.data.values():
        if ql in contact.name.value.lower():
            matches.append(contact)
            continue
        if any(ql in p.value.lower() for p in contact.phones):
            matches.append(contact)
            continue
        if contact.email and ql in contact.email.value.lower():
            matches.append(contact)
            continue
        if contact.address and ql in contact.address.value.lower():
            matches.append(contact)

    if not matches:
        return f"No contacts matched '{query}'."
    blocks = [format_contact(c) for c in matches]
    return "\n\n".join(blocks)


def register_contact_commands(commands):
    """Register commands in the main command dispatcher."""
    commands[Command.Contacts.ADD] = add_contact
    commands[Command.Contacts.CHANGE] = change_contact
    commands[Command.Contacts.PHONE] = show_phone
    commands[Command.Contacts.ALL] = show_all
    commands[Command.Contacts.ADD_BIRTHDAY] = add_birthday
    commands[Command.Contacts.SHOW_BIRTHDAY] = show_birthday
    commands[Command.Contacts.BIRTHDAYS] = birthdays
    commands[Command.Contacts.SEARCH] = search_contacts
    commands[Command.Contacts.ADD_EMAIL] = add_email
    commands[Command.Contacts.ADD_ADDRESS] = add_address
    commands[Command.Contacts.DELETE] = delete_contact
