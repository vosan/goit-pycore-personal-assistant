"""
Defines base and specific field types for contact information.

Classes:
- Name: Handles name formatting.
- Phone: Validates and stores phone numbers.
- Birthday: Validates and parses birthday dates.
- Email, Address: Simple string wrappers.

Responsibilities:
- Handle data validation and formatting for each field.
- Raise ValueError on invalid input.
"""
from __future__ import annotations

from datetime import datetime, date


class Name:
    def __init__(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self.value = value


class Phone:
    def __init__(self, value: str):
        # Minimal validation: digits and +, -, spaces allowed
        v = str(value).strip()
        if not v:
            raise ValueError("Phone cannot be empty")
        self.value = v

    def set(self, new_value: str) -> None:
        v = str(new_value).strip()
        if not v:
            raise ValueError("Phone cannot be empty")
        self.value = v


class Birthday:
    def __init__(self, value: str | date):
        if isinstance(value, date):
            self.value = value
            return
        v = str(value).strip()
        try:
            # Expect DD.MM.YYYY
            self.value = datetime.strptime(v, "%d.%m.%Y").date()
        except Exception as e:
            raise ValueError("Birthday must be in DD.MM.YYYY format") from e


class Email:
    def __init__(self, value: str):
        self.value = str(value).strip()


class Address:
    def __init__(self, value: str):
        self.value = str(value).strip()
