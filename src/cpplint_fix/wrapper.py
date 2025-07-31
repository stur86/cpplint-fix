from pathlib import Path
import subprocess as sp
from cpplint_fix.parser import CPPLTestsuite

def run_cpplint(root: Path) -> CPPLTestsuite:
    """Run cpplint on the given root directory and return the parsed results."""
    cmd = ["cpplint", "--output=junit", "--recursive", str(root.absolute())]
    proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    _, stderr = proc.communicate()
    
    return CPPLTestsuite.from_string(stderr.decode("utf-8"))

