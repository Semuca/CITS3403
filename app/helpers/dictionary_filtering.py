"""Helper functions for filtering dictionaries"""

from typing import Any

def remove_none_from_dictionary(dictionary: dict[Any, Any]) -> dict[Any, Any]:
    """Return a copy of the dictionary with all None values removed"""
    return {key: value for key, value in dictionary.items() if value is not None}
