from pathlib import Path
import pytest
from .conftest import EditExample
from cpplint_fix.wrapper import run_cpplint
from cpplint_fix.edits import Edits
from cpplint_fix.source import SourceFile

@pytest.mark.usefixtures("edit_example")
@pytest.mark.parametrize("error_code", ["whitespace/ending_newline"])
def test_edit(edit_example: EditExample, tmp_path: Path):
    assert edit_example is not None
    
    # Run cpplint on the input folder
    cppl_testsuite = run_cpplint(edit_example.input)
    assert cppl_testsuite is not None
    assert cppl_testsuite.total_failures > 0, "No failures found in cpplint output"
    
    fixed_path = tmp_path / "fixed"
    fixed_path.mkdir(parents=True, exist_ok=True)
    
    # Now for each file, find the edits
    for testcase in cppl_testsuite.testcases:
        assert testcase.fpath.exists(), f"Testcase file {testcase.fpath} does not exist"
        src = SourceFile.from_file(testcase.fpath)
        assert src is not None, f"Failed to parse source file {testcase.fpath}"
        
        for failure in testcase.failures:
            edit_class = Edits.get(failure.code)
            assert edit_class is not None
            edit_instance = edit_class(failure)
            assert edit_instance is not None
            edit_instance.apply(src)
            
        dest_path = fixed_path / testcase.fpath.name
        src.to_file(dest_path)
        
        # Check that it's the same as the expected output
        expected_output = edit_example.output / testcase.fpath.name
        assert expected_output.exists(), f"Expected output file {expected_output} does not exist"
        assert dest_path.read_text() == expected_output.read_text(), f"Output file {dest_path} does not match expected output {expected_output}"