"""
Defines the AddressBook class, which manages multiple contacts.

Responsibilities:
- Store and retrieve Record instances by name.
- Provide search, delete, and iteration methods.
- Include the `get_upcoming_birthdays()` function.
"""

from datetime import datetime, timedelta

class AddressBook:
    pass








def get_upcoming_birthdays(self, days: None):
        if days == None :
            user_input = input("Enter the number of days (or press Enter to leave 7): ")
            if user_input.strip():
                try: 
                    days = int(user_input)
                except ValueError:
                    print("Please enter an integer")
                
        today = datetime.today().date()
        upcoming = {}
        for record in self.data.values():
            if record.birthday:
                next_bday = record.birthday.value.replace(year=today.year)
                if next_bday < today:
                    next_bday = next_bday.replace(year=today.year + 1)
                delta = (next_bday - today).days
                if 0 <= delta <= days:
                    upcoming[record.name.value] = next_bday.strftime("%d.%m.%Y")
        return upcoming