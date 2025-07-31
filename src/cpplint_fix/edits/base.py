from abc import ABC, abstractmethod
from cpplint_fix.source import SourceFile
from cpplint_fix.parser import CPPLFailure


class BaseEdit(ABC):
    _error_code: str = "BASE_EDIT"
    _failure: CPPLFailure

    def __init__(self, failure: CPPLFailure):
        self._failure = failure
        assert (
            failure.code == self._error_code
        ), f"Expected error code {self._error_code}, got {failure.code}"

    @property
    def error_code(self) -> str:
        """Returns the error code associated with this edit."""
        return self._error_code

    @property
    def failure(self) -> CPPLFailure:
        """Returns the CPPLFailure associated with this edit."""
        return self._failure

    @abstractmethod
    def apply(self, source_file: SourceFile) -> None:
        """Apply the edit to the given source file."""
        pass
