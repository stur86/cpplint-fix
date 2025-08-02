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
        
class TrailingWhitespace(BaseEdit):
    """Edit to remove trailing whitespace from lines."""

    _error_code = "whitespace/end_of_line"

    def _operations(self, source_file: SourceFile) -> list[EditOperation]:
        """Returns edit operations to remove trailing whitespace from lines."""
        line_no = self.failure.lineno
        line_text = source_file[line_no].final_line
        if line_text is None:
            return []
        return [
            EditOperation(line_no, EditOperationType.EDIT, line_text.rstrip())
        ]