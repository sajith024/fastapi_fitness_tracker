from datetime import datetime, timedelta
import re

from pydantic_core import PydanticCustomError

from app.utils import date_tz

length_regex = r"^.{8,}$"  # At least 8 characters
uppercase_regex = r"(?=.*[A-Z])"  # At least one uppercase letter
lowercase_regex = r"(?=.*[a-z])"  # At least one lowercase letter
digit_regex = r"(?=.*\d)"  # At least one digit
special_char_regex = r"(?=.*[@$!%*?&])"  # At least one special character
only_char_regex = r"^[a-zA-Z_]*$"


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


def validate_goal_deadline(deadline: datetime):
    today_date = date_tz.now().date()
    deadline_date = deadline.date()
    years_in_future_limit = today_date + timedelta(days=365)

    if deadline_date < today_date:
        raise PydanticCustomError(
            "date_error", "The input date must be today or a future date"
        )
    elif deadline_date > years_in_future_limit:
        raise PydanticCustomError(
            "date_error", "The input date must be within a year in the future"
        )

    return deadline


def validate_exercise(exercise: str):
    if not re.match(only_char_regex, exercise):
        raise PydanticCustomError(
            "exercise_error",
            "Exercise must be valid string with alphabets, '_'.",
        )
