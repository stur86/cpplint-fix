import pytest
from pathlib import Path
import xml.etree.ElementTree as ET
from cpplint_fix.parser import CPPLFailure, CPPLTestcase, CPPLTestsuite

def test_failure():
    failure_elem = ET.Element("failure")
    failure_elem.text = "42: Some error message [E123] [1]"
    
    failure = CPPLFailure(failure_elem)
    
    assert failure.lineno == 42
    assert failure.message == "Some error message"
    assert failure.code == "E123"
    assert repr(failure) == "CPPLFailure(lineno=42, message='Some error message', code='E123')"
    
    # Test invalid failure element
    invalid_elem = ET.Element("not_failure")
    with pytest.raises(AssertionError):
        CPPLFailure(invalid_elem)
        
    invalid_elem = ET.Element("failure")
    invalid_elem.text = None

    with pytest.raises(ValueError):
        CPPLFailure(invalid_elem)
        
    invalid_elem.text = "invalid format"
    with pytest.raises(ValueError):
        CPPLFailure(invalid_elem)
        
def test_testcase():
    testcase_elem = ET.Element("testcase", name="test_file.cpp")
    failure_elem = ET.Element("failure")
    failure_elem.text = "42: Some error message [E123] [1]"
    testcase_elem.append(failure_elem)
    
    testcase = CPPLTestcase(testcase_elem)
    
    assert testcase.fpath == Path("test_file.cpp")
    assert len(testcase.failures) == 1
    assert testcase.failures[0].lineno == 42
    assert testcase.failures[0].message == "Some error message"
    assert testcase.failures[0].code == "E123"
    
    # Test invalid testcase element
    invalid_elem = ET.Element("not_testcase")
    with pytest.raises(AssertionError):
        CPPLTestcase(invalid_elem)
        
    invalid_elem = ET.Element("testcase", name="")
    with pytest.raises(ValueError):
        CPPLTestcase(invalid_elem)
        
def test_testsuite():
    testsuite_elem = ET.Element("testsuite")
    testcase_elem = ET.Element("testcase", name="test_file.cpp")
    failure_elem = ET.Element("failure")
    failure_elem.text = "42: Some error message [E123] [1]"
    testcase_elem.append(failure_elem)
    testsuite_elem.append(testcase_elem)
    
    testsuite = CPPLTestsuite(testsuite_elem)
    
    assert len(testsuite.testcases) == 1
    assert testsuite.testcases_dict[Path("test_file.cpp")].fpath == Path("test_file.cpp")
    assert len(testsuite.testcases_dict[Path("test_file.cpp")].failures) == 1

    # Test empty testsuite
    empty_suite = CPPLTestsuite(ET.Element("testsuite"))
    assert len(empty_suite.testcases) == 0
    
def test_example_xml(examples_path: Path):
    example_file = examples_path / "example.xml"
    assert example_file.exists(), f"Example file {example_file} does not exist"
    
    tree = ET.parse(example_file)
    root = tree.getroot()
    
    testsuite = CPPLTestsuite(root)
    
    assert len(testsuite.testcases) > 0, "No test cases found in example XML"
    for testcase in testsuite.testcases:
        assert isinstance(testcase, CPPLTestcase), "Testcase is not of type CPPLTestcase"
        assert len(testcase.failures) >= 0, "Testcase has negative number of failures"
        for failure in testcase.failures:
            assert isinstance(failure, CPPLFailure), "Failure is not of type CPPLFailure"
            assert failure.lineno > 0, "Failure line number is not positive"
            assert failure.message, "Failure message is empty"
            assert failure.code, "Failure code is empty"