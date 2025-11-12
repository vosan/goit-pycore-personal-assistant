"""
Provides shared utilities for the command-line interface:
- The `input_error` decorator for unified exception handling.
- The `parse_input()` function for splitting user input into command and arguments.
- Optionally, a central command dispatcher function (if needed later).

Responsibilities:
- Contain only CLI parsing and error handling logic.
"""
import re

def validate_phone(phone: str) -> bool:
    """Перевіряє правильність номера телефону українського формату."""
    if not phone or not isinstance(phone, str):
        return False
        
    cleaned_phone = re.sub(r'\D', '', phone)
    pattern = r'^(\+?38)?0\d{9}$'
    return bool(re.match(pattern, cleaned_phone))

def validate_email(email: str) -> bool:
    """Перевіряє правильність email адреси."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def normalize_phone(phone: str) -> str:
    """Нормалізує номер телефону до стандартного формату +380XXXXXXXXX."""
    if not validate_phone(phone):
        raise ValueError("Некоректний номер телефону")
        
    cleaned_phone = re.sub(r'\D', '', phone)
    if cleaned_phone.startswith('38') and len(cleaned_phone) == 12:
        return '+' + cleaned_phone
    elif cleaned_phone.startswith('0') and len(cleaned_phone) == 10:
        return '+38' + cleaned_phone
    else:
        raise ValueError("Неможливо нормалізувати номер телефону")

def input_error(func):
    """Decorator to handle input errors."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format. Please provide all required arguments."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return inner

def parse_input(user_input):
    """Parse user input into command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args