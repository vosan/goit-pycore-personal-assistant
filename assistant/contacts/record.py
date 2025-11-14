"""
Defines the Record class, representing a single contact.

Responsibilities:
- Store a contact’s name, phones, and birthday.
- Provide methods to add/edit/remove/find phone numbers.
- Handle adding and storing a birthday (using the Birthday field).
"""
from .fields import Name, Phone, Birthday, Email, Address
from datetime import datetime
from typing import Any, Dict, List

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            phone_obj.set(new_phone)
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        birthday_date = self.birthday.value
        try:
            next_birthday = birthday_date.replace(year=today.year)
        except ValueError:
            next_birthday = datetime(today.year, 2, 28).date()
        if next_birthday < today:
            next_year = today.year + 1
            try:
                next_birthday = birthday_date.replace(year=next_year)
            except ValueError:
                # Again: Feb 29 fallback for non-leap years
                next_birthday = datetime(next_year, 2, 28).date()

        return (next_birthday - today).days
    
    def add_email(self, email: str):
        """Add or update email."""
        self.email = Email(email)

    def add_address(self, address: str):
        """Add or update address."""
        self.address = Address(address)


    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones) if self.phones else "no phone numbers"
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "not specified"
        email_str = self.email.value if self.email else "not specified"
        address_str = self.address.value if self.address else "not specified"
        return (
            f"Name: {self.name.value}, "
            f"Phones: {phones_str}, "
            f"Birthday: {birthday_str}, "
            f"Email: {email_str}, "
            f"Address: {address_str}"
        )

    # ---- Serialization helpers ----
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "birthday": self.birthday.value.strftime("%d.%m.%Y") if self.birthday else None,
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":
        # Support both dicts keyed and possibly minimal items
        name = data.get("name") or data.get("Name")
        rec = cls(name)
        for ph in data.get("phones", []) or []:
            rec.add_phone(ph)
        bday = data.get("birthday")
        if bday:
            rec.add_birthday(bday)
        email = data.get("email")
        if email:
            rec.add_email(email)
        address = data.get("address")
        if address:
            rec.add_address(address)
        return rec
