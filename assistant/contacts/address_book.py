"""
Defines the AddressBook class, which manages multiple contacts.

Responsibilities:
- Store and retrieve Record instances by name.
- Provide search, delete, and iteration methods.
- Include the `get_upcoming_birthdays()` function.
"""

from datetime import datetime

class AddressBook:

    def get_upcoming_birthdays(self, days: int | None = 7):
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

