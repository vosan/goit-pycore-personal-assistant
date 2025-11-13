"""
Defines the Record class, representing a single contact.

Responsibilities:
- Store a contact’s name, phones, and birthday.
- Provide methods to add/edit/remove/find phone numbers.
- Handle adding and storing a birthday (using the Birthday field).
"""
from .fields import Name, Phone, Birthday, Email, Address
from datetime import datetime, timedelta

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
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
