from datetime import datetime


def to_datetime(date_str: str) -> datetime:
    """Converts a string to a datetime object, supporting multiple formats."""
    formats = [
        "%Y-%m-%dT%H:%M:%S",  # ISO format without 'Z'
        "%Y-%m-%dT%H:%M:%S.%f",  # ISO with microseconds
        "%Y-%m-%d",  # Date only
        "%Y/%m/%d",  # Date with slashes
    ]

    # Remove 'Z' for UTC if present
    if date_str.endswith("Z"):
        date_str = date_str[:-1]

    # Try parsing with different formats
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Date string '{date_str}' is not in a recognized format."
    )
