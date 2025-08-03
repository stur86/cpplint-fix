from pathlib import Path
import subprocess as sp
import logging
from cpplint_fix.parser import CPPLTestsuite
from cpplint_fix.source import SourceFile
from cpplint_fix.edits import Edits, FailedEditError

logger = logging.getLogger(__name__)

def run_cpplint(root: Path) -> CPPLTestsuite:
    """Run cpplint on the given root directory and return the parsed results."""
    cmd = ["cpplint", "--output=junit", "--recursive", "./"]
    proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, cwd=root)
    _, stderr = proc.communicate()
    
    return CPPLTestsuite.from_string(stderr.decode("utf-8"))

def fix_folder(input: Path, output: Path | None, dry_run: bool = False) -> None:
    """Run cpplint on the input folder and apply fixes to the output folder."""

    cppl_testsuite = run_cpplint(input)
    
    if not cppl_testsuite.testcases:
        logger.info("No test cases found in cpplint output.")
        return
    
    for testcase in cppl_testsuite.testcases:
        # All paths are relative to the input directory
        fpath = input / testcase.fpath
        logger.info(f"Processing file: {fpath}")
        src = SourceFile.from_file(fpath)
        for failure in testcase.failures:
            edit_class = Edits.get(failure.code)
            if edit_class is None:
                logger.warning(f"No edits found for error code: {failure.code}")
                continue

            edit = edit_class(failure)
            if dry_run:
                logger.info(f"Dry run: would apply edit {edit} to {fpath}")
                continue
            try:
                edit.apply(src)
            except FailedEditError as e:
                logger.error(f"Failed to apply edit {edit} to {fpath}: {e}")
                continue
        
        if dry_run:
            continue

        if output is not None:
            dest_path = output / fpath.name
            src.to_file(dest_path)
            logger.info(f"Fixed file written to: {dest_path}")
        else:
            logger.info(f"Applying edits to source file: {fpath}")
            src.apply_edits()