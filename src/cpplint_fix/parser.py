import re
from pathlib import Path
import xml.etree.ElementTree as XMLET


class CPPLFailure:
    _lineno: int
    _message: str
    _code: str
    
    _failre = re.compile(r"^(?P<lineno>\d+):\s*(?P<message>.*)\s*\[(?P<code>.*)\] \[\d+\]$")
    
    def __init__(self, elem: XMLET.Element) -> None:
        assert elem.tag == "failure", f"Expected 'failure' tag, got {elem.tag}"
        if elem.text is None:
            raise ValueError("Failure element text cannot be None")
        _failm = self._failre.match(elem.text.strip())
        if not _failm:
            raise ValueError(f"Invalid failure message: {elem.text.strip()}")
        self._lineno = int(_failm.group("lineno"))
        self._message = _failm.group("message").strip()
        self._code = _failm.group("code")
        
    @property
    def lineno(self) -> int:
        return self._lineno
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def code(self) -> str:
        return self._code
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lineno={self._lineno}, message='{self._message}', code='{self._code}')"
    
class CPPLTestcase:
    _fpath: Path
    _failures: list[CPPLFailure]
    
    def __init__(self, elem: XMLET.Element) -> None:
        assert elem.tag == "testcase", f"Expected 'testcase' tag, got {elem.tag}"
        fpath = elem.attrib.get("name", "")
        if not fpath:
            raise ValueError("Testcase name cannot be empty")
        self._fpath = Path(fpath)
        self._failures = []
        
        for child in elem:
            self._failures.append(CPPLFailure(child))
            
    @property
    def fpath(self) -> Path:
        return self._fpath
    
    @property
    def failures(self) -> list[CPPLFailure]:
        return self._failures
    
    @property
    def failures_dict(self) -> dict[int, list[CPPLFailure]]:
        """Returns a dictionary grouping failures by line number."""
        if not self._failures:
            return {}

        # Group the failures by line number
        fdict = {}
        for fail in self._failures:
            flist: list[CPPLFailure] = fdict.setdefault(fail.lineno, [])
            flist.append(fail)

        return fdict
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(fpath={self._fpath}, failures_count={len(self._failures)})"
    
class CPPLTestsuite:
    _testcases: list[CPPLTestcase]
    
    def __init__(self, elem: XMLET.Element) -> None:
        assert elem.tag == "testsuite", f"Expected 'testsuite' tag, got {elem.tag}"
        self._testcases = []
        
        for child in elem:
            self._testcases.append(CPPLTestcase(child))
                
    @property
    def testcases(self) -> list[CPPLTestcase]:
        return self._testcases
    
    @property
    def testcases_dict(self) -> dict[Path, CPPLTestcase]:
        """Returns a dictionary mapping file paths to Testcase objects."""
        return {tc.fpath: tc for tc in self._testcases}
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(testcases_count={len(self._testcases)})"
    
    @classmethod
    def from_file(cls, file_path: Path) -> "CPPLTestsuite":
        """Creates a CPPLTestsuite from an XML file."""
        tree = XMLET.parse(file_path)
        root = tree.getroot()
        return cls(root)