from cpplint_fix.edits.base import BaseEdit, EditOperation, EditOperationType
from cpplint_fix.source import SourceFile

class MissingEndingNL(BaseEdit):
    """Edit to add a missing newline at the end of a file."""

    _error_code = "whitespace/ending_newline"

    def _operations(self, source_file: SourceFile) -> list[EditOperation]:
        """Returns an edit operation to add a newline at the end of the file."""
        if not source_file.lines or source_file.lines[-1].final_line == '':
            return []  # No operation needed if the last line already ends with a newline

        return [EditOperation(
            line_number=len(source_file.lines),
            operation_type=EditOperationType.INSERT_AFTER,
            text=''
        )]