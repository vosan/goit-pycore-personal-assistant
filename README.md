# goit-pycore-personal-assistant 

Simple personal assistant within command line to manage contacts and notes.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Features

- Contacts: add, edit, delete, search, show upcoming birthdays in set ammount of days days
- Notes: add, edit, delete, search
- Data is stored in data files and is available on next launch

## Requirements

- Python 3.11+

## Available commands

```bash
Command List:
  ======================================================================
📞 Contact Management:
  add <name> <phone>........................... Add a new contact
  add-email <name> <email>..................... Add or update a contact's email
  add-birthday <name> <DD.MM.YYYY>............. Add birthday to a contact
  add-address <name> <address>................. Add or update a contact's address
  change-phone <name> <old_phone> <new_phone>.. Change contact's phone number
  birthdays [days]............................. Show upcoming birthdays (default: 7 days)
  birthday <name>.............................. Show birthday for a contact
  all.......................................... Show all contacts
  phone <name>................................. Show phone number(s) for a contact
  search <query>............................... Search contacts by name, phone, email, or address
  delete <name>................................ Delete a contact by name

  ======================================================================
  📝 Note Management:
  add-note <title> <content>................... Add a new note
  edit-note <title> <new_content>.............. Edit an existing note
  all-notes.................................... Show all notes
  search-note <keyword>........................ Search notes by keyword
  delete-note <title>.......................... Delete a note

   General:
  hello........................................ Greet the assistant
  help......................................... Show this help message
  close........................................ Close the assistant
  clear........................................ Clear the terminal screen
  ======================================================================
  Legend:
  <parameter>  Required parameter
  [parameter]  Optional parameter
  ======================================================================

```

## Hidden features
Assistant can give you a joke or few if you are "friendly" enough...
