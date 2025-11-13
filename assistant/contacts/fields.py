"""
Defines base and specific field types for contact information.

Classes:
- Field: Base class for all fields.
- Name: Handles name formatting.
- Phone: Validates and stores phone numbers.
- Birthday: Validates and parses birthday dates.

Responsibilities:
- Handle data validation and formatting for each field.
- Raise ValueError on invalid input.
"""
class Name:
    def __init__(self, value):
        self.value = value

class Phone:
    def __init__(self, value):
        self.value = value

class Birthday:
    def __init__(self, value):
        self.value = value

class Email:
    def __init__(self, value):
        self.value = value

class Address:
    def __init__(self, value):
        self.value = value
