from typing import Type
from .base import BaseEdit
from .whitespace import MissingEndingNL

__all__ = [
    "BaseEdit",
    "Edits",
    "MissingEndingNL"
]

class Edits():
    """Categorizes and returns all the edits defined within this module."""
    __edits: dict[str, Type[BaseEdit]] = {
        v._error_code: v for v in globals().values()
        if isinstance(v, type) and issubclass(v, BaseEdit) and v is not BaseEdit
    }
    
    @classmethod
    def get(cls, edit_code: str) -> Type[BaseEdit] | None:
        """Returns the edit class for the given error code."""
        if edit_code not in cls.__edits:
            return None
        return cls.__edits[edit_code]
