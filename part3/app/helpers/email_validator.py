"""Simplitic email validator."""

import re


def validate_email(email: str) -> bool:
    """Check if an email is valid.

    Returns:
        true if email is valid else false

    """
    regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    return True if re.fullmatch(regex, email) else False
