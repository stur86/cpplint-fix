import pytest
from dataclasses import FrozenInstanceError
from cpplint_fix.source import SourceLine



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
