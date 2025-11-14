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
- etc.

Responsibilities:
- Parse and validate command arguments.
- Interact with the AddressBook and Record classes.
- Return text messages to be printed by main.py.
"""

from assistant.commands_enum import Command
from assistant.core import input_error
from assistant.contacts.record import Record


@input_error
def add_contact(args, book):
    """Add a new contact or phone number."""
    if len(args) < 2:
        return "Usage: add [name] [phone number]"
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
        return "Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    phones = "; ".join(p.value for p in record.phones)
    return f"{name}: {phones}"


@input_error
def show_all(args, book):
    """Display all contacts in the address book."""
    if not book.data:
        return "The contact list is empty."
    return "\n".join(str(record) for record in book.data.values())


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
    if not record or not record.birthday:
        return "Birthday not found."
    return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book):
    """Show contacts with upcoming birthdays."""
    days = int(args[0]) if args else 7
    result = book.get_upcoming_birthdays(days)
    if not result:
        return "No birthdays within the next week."
    return "\n".join(f"{name}: {date}" for name, date in result.items())


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
    return "\n".join(str(c) for c in matches)


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
