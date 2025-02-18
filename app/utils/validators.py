import re

from pydantic_core import PydanticCustomError

length_regex = r"^.{8,}$"  # At least 8 characters
uppercase_regex = r"(?=.*[A-Z])"  # At least one uppercase letter
lowercase_regex = r"(?=.*[a-z])"  # At least one lowercase letter
digit_regex = r"(?=.*\d)"  # At least one digit
special_char_regex = r"(?=.*[@$!%*?&])"  # At least one special character


def validate_password(password: str):
    if not re.match(length_regex, password):
        raise PydanticCustomError(
            "password_error",
            "Password must be at least 8 characters long",
        )

    if not re.search(uppercase_regex, password):
        raise PydanticCustomError(
            "password_error",
            "Password must contain at least one uppercase letter",
        )

    if not re.search(lowercase_regex, password):
        raise PydanticCustomError(
            "password_error",
            "Password must contain at least one lowercase letter",
        )

    if not re.search(digit_regex, password):
        raise PydanticCustomError(
            "password_error",
            "Password must contain at least one digit",
        )

    if not re.search(special_char_regex, password):
        raise PydanticCustomError(
            "password_error",
            "Password must contain at least one special character (@, $, !, %, *, ?, &, etc.)",
        )

    return password
