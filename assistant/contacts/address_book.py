"""
Defines the AddressBook class, which manages multiple contacts.

Responsibilities:
- Store and retrieve Record instances by name.
- Provide search, delete, and iteration methods.
- Include the `get_upcoming_birthdays()` function.
 - Handle serialization to/from JSON-compatible structures.
"""

from datetime import datetime
from typing import Dict, Any

from .record import Record

class AddressBook:
    def __init__(self) -> None:
        # Internal storage: name -> Record
        self.data: Dict[str, Record] = {}

    def add_record(self, record: Record) -> None:
        """Add or replace a record by its name."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Find a record by exact name."""
        return self.data.get(name)

    # ---- Serialization helpers ----
    def to_dict(self) -> Dict[str, Any]:
        return {name: rec.to_dict() for name, rec in self.data.items()}

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.data = {name: Record.from_dict(rec) for name, rec in data.items()}

    def from_list(self, items: list[dict]) -> None:
        """Backward compatibility for list-shaped storage."""
        self.data = {}
        for item in items:
            rec = Record.from_dict(item)
            self.add_record(rec)

    def get_upcoming_birthdays(self, days: int | None = 7):
        """Return a dict of name -> next birthday date (DD.MM.YYYY) within the next `days`.

        - If `days` is None, defaults to 7.
        - Negative values are treated as 0 (today only).
        """
        if days is None:
            days = 7
        if days < 0:
            days = 0
        today = datetime.today().date()
        upcoming = {}

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value

            try:
                next_bday = birthday_date.replace(year=today.year)
            except ValueError:
                next_bday = datetime(today.year, 2, 28).date()

            if next_bday < today:
                next_year = today.year + 1
                try:
                    next_bday = birthday_date.replace(year=next_year)
                except ValueError:
                    next_bday = datetime(next_year, 2, 28).date()

            delta = (next_bday - today).days
            if 0 <= delta <= days:
                upcoming[record.name.value] = next_bday.strftime("%d.%m.%Y")

        return upcoming

