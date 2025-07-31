import types
from typing import Type
from .base import BaseEdit


class _EditsMeta(type):
    """Metaclass to automatically register edits."""

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if not hasattr(cls, "_edits"):
            cls._edits = {}
        import cpplint_fix.edits as edits_module

        # Look for all the modules inside
        for k, v in edits_module.__dict__.items():
            if isinstance(v, types.ModuleType):
                # Iterate through all classes in the module
                for sub_v in v.__dict__.values():
                    if (
                        isinstance(sub_v, type)
                        and issubclass(sub_v, BaseEdit)
                        and sub_v is not BaseEdit
                    ):
                        cls._edits[sub_v._error_code] = sub_v

        return new_class


class Edits(metaclass=_EditsMeta):
    """Categorizes and returns all the edits defined within this module."""
    _edits: dict[str, Type[BaseEdit]] = {}
    
    @classmethod
    def get(cls, edit_code: str) -> Type[BaseEdit]:
        """Returns the edit class for the given error code."""
        if edit_code not in cls._edits:
            raise KeyError(f"Edit with error code '{edit_code}' not found")
        return cls._edits[edit_code]
