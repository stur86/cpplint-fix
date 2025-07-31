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
    
    @property
    def edited_lines(self) -> list[str]:
        """Returns the lines to be inserted before and after the source line."""
        return self.insert_before + [self.line] + self.insert_after
    
    