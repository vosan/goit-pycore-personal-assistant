"""
CLI parsing and error handling utilities.

Functions:
- input_error: Decorator for unified exception handling.
- parse_input: Parse user input into command and arguments.
"""
from functools import wraps
from typing import Callable, Any, Tuple, List
import shlex
import logging

logger = logging.getLogger(__name__)


def input_error(func: Callable) -> Callable:
    """Decorator for handling command errors."""
    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
        except Exception as e:
            logger.exception("Unexpected error")
            return f"Error: {e}"
    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse input into command and arguments."""
    if not user_input or not user_input.strip():
        return "", []
    
    try:
        parts = shlex.split(user_input.strip())
    except ValueError:
        parts = user_input.strip().split()
    
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args
