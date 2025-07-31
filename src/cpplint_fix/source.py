from pathlib import Path
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceLine:
    number: int
    line: str
    insert_before: list[str] = field(default_factory=list)
    insert_after: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.number <= 0:
            raise ValueError("Line number must be positive")
        if not isinstance(self.line, str):
            raise TypeError("Line must be a string")
        # Strip any newline characters from the line
        object.__setattr__(self, 'line', self.line.strip('\n'))
        print(self)
    
    @property
    def edited_lines(self) -> list[str]:
        """Returns the lines to be inserted before and after the source line."""
        return self.insert_before + [self.line] + self.insert_after
    
    def __repr__(self) -> str:
        return f"{self.number}: {self.line} (+{len(self.insert_before)} before, {len(self.insert_after)} after)"

class SourceFile:
    """Represents a source file with its lines."""
    
    def __init__(self, path: Path):
        self._path = path.absolute()
        self._lines: list[SourceLine] = []
        for i, line in enumerate(path.read_text().splitlines(), start=1):
            self._lines.append(SourceLine(number=i, line=line))
        
    @property
    def path(self) -> Path:
        return self._path
    
    def insert_before(self, line_number: int, text: str):
        """Insert a line before the specified line number."""
        if line_number < 1 or line_number > len(self._lines):
            raise IndexError("Line number out of range")
        self._lines[line_number - 1].insert_before.append(text)
        
    def insert_after(self, line_number: int, text: str):
        """Insert a line after the specified line number."""
        if line_number < 1 or line_number > len(self._lines):
            raise IndexError("Line number out of range")
        self._lines[line_number - 1].insert_after.append(text)
    
    def __getitem__(self, index: int) -> SourceLine:
        """Get a specific line by its index (1-based)."""
        if index < 1 or index > len(self._lines):
            raise IndexError("Line index out of range")
        return self._lines[index - 1]
    
    def __repr__(self) -> str:
        return f"SourceFile(path={self._path}, lines_count={len(self._lines)})"