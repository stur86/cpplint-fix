from pathlib import Path
import argparse as ap
from cpplint_fix.wrapper import fix_folder
import logging


def main():
    parser = ap.ArgumentParser(description="Run cpplint and apply fixes to source files.")
    parser.add_argument("input", type=Path, help="Input directory containing source files")
    parser.add_argument("--output", type=Path, default=None, 
                        help="Output directory for fixed files (optional)")
    parser.add_argument("--dry-run", action="store_true",
                        help="If set, only print the changes without applying them")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    logging.basicConfig(level=logging.INFO)
    
    fix_folder(input_path, output_path, dry_run=args.dry_run)
    
if __name__ == "__main__":
    main()