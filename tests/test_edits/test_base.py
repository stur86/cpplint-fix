import pytest
from pathlib import Path
from cpplint_fix.edits.base import BaseEdit
from cpplint_fix.parser import CPPLFailure
from cpplint_fix.source import SourceFile, SourceLine

def test_base_edit():
    class TestEdit(BaseEdit):
        _error_code = "TEST_EDIT"

        def apply(self, source_file: SourceFile) -> None:
            source_file.insert_after(self.failure.lineno, "// Test edit applied")
    
    source = "const int x = 42;"
    source_file = SourceFile(path=Path("test.cpp"), lines=[SourceLine(number=1, line=source)])
    
    edit = TestEdit(CPPLFailure(lineno=1, message="Test failure", code="TEST_EDIT"))
    assert edit.error_code == "TEST_EDIT"
    assert edit.failure.lineno == 1
    assert edit.failure.message == "Test failure"
    
    edit.apply(source_file)
    assert len(source_file.lines) == 1
    assert source_file[1].line == source
    assert source_file[1].insert_after == ["// Test edit applied"]
    
def test_base_edit_invalid_failure():
    class InvalidEdit(BaseEdit):
        _error_code = "INVALID_EDIT"

        def apply(self, source_file: SourceFile) -> None:
            pass

    with pytest.raises(AssertionError):
        InvalidEdit(CPPLFailure(lineno=1, message="Invalid failure", code="WRONG_CODE"))
    
            
    
