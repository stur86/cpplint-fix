import os
from pathlib import Path
from tempfile import NamedTemporaryFile
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
        object.__setattr__(self, "line", self.line.strip("\n"))

    @property
    def edited_lines(self) -> list[str]:
        """Returns the lines to be inserted before and after the source line."""
        return self.insert_before + [self.line] + self.insert_after

    def __repr__(self) -> str:
        return f"{self.number}: {self.line} (+{len(self.insert_before)} before, {len(self.insert_after)} after)"


@dataclass(frozen=True)
class SourceFile:
    """Represents a source file with its lines."""

    path: Path
    lines: list[SourceLine] = field(repr=False)

    def insert_before(self, line_number: int, text: str):
        """Insert a line before the specified line number."""
        if line_number < 1 or line_number > len(self.lines):
            raise IndexError("Line number out of range")
        self.lines[line_number - 1].insert_before.append(text)

    def insert_after(self, line_number: int, text: str):
        """Insert a line after the specified line number."""
        if line_number < 1 or line_number > len(self.lines):
            raise IndexError("Line number out of range")
        self.lines[line_number - 1].insert_after.append(text)

    def __getitem__(self, index: int) -> SourceLine:
        """Get a specific line by its index (1-based)."""
        if index < 1 or index > len(self.lines):
            raise IndexError("Line index out of range")
        return self.lines[index - 1]

    def __len__(self) -> int:
        """Returns the number of lines in the source file."""
        return len(self.lines)

    def __repr__(self) -> str:
        return f"SourceFile(path={self.path}, lines_count={len(self.lines)})"
    
    def to_file(self, file_path: Path) -> None:
        """Writes the source file to the specified path."""
        all_lines = sum([line.edited_lines for line in self.lines], [])
        with file_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(all_lines))
        
    def apply(self) -> None:
        """Applies all edits to the source file."""
        # First, create a temporary file with all edits applied
        temp_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.to_file(Path(temp_file.name))
        # Now, replace the original file with the temporary file
        temp_file.close()
        os.replace(temp_file.name, self.path)

    @classmethod
    def from_file(cls, file_path: Path) -> "SourceFile":
        """Creates a SourceFile from a given file path."""
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist")

        file_lines = file_path.read_text(encoding="utf-8").splitlines()
        lines = [
            SourceLine(number=i + 1, line=line)
            for i, line in enumerate(file_lines)
        ]   
        return cls(path=file_path, lines=lines)
