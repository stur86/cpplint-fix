import pytest
from pathlib import Path
from dataclasses import FrozenInstanceError
from cpplint_fix.source import SourceLine, SourceFile



def test_source_line():
    line = SourceLine(number=42, line="int main() { return 0; };\n")
    
    assert line.number == 42
    assert line.line == "int main() { return 0; };"
    assert line.insert_before == []
    assert line.insert_after == []

    with pytest.raises(FrozenInstanceError):
        line.number = 40 # type: ignore
        
    with pytest.raises(FrozenInstanceError):
        line.line = "int main() { return 1; };" # type: ignore
        
    # Try inserting lines before and after
    line.insert_before.append("// This is a comment")
    line.insert_after.append("// End of main function")
    
    assert line.edited_lines == [
        "// This is a comment",
        "int main() { return 0; };",
        "// End of main function"
    ]
    
    with pytest.raises(ValueError):
        SourceLine(number=0, line="Invalid line")
    with pytest.raises(TypeError):
        SourceLine(number=1, line=123) # type: ignore

def test_source_file(tmp_path: Path):
    source_content = """
int main() {
    return 0;
}
"""

    source_file_path = tmp_path / "test_source.cpp"
    source_file_path.write_text(source_content)
    
    source_file = SourceFile.from_file(source_file_path)
    assert source_file.path == source_file_path
    assert len(source_file.lines) == 4  # 3 lines + 1 empty line
    assert len(source_file) == 4
    source_lines = source_content.splitlines(keepends=False)

    for (i, line) in enumerate(source_file.lines, start=1):
        assert line.number == i
        assert isinstance(line.line, str)
        assert line.line == source_lines[i - 1]
        
    # Try inserting lines
    source_file.insert_before(2, "// This is a comment before line 2")
    source_file.insert_after(3, "// This is a comment after line 3")
    
    assert source_file[2].insert_before == ["// This is a comment before line 2"]
    assert source_file[3].insert_after == ["// This is a comment after line 3"]