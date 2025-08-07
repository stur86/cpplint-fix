from pathlib import Path
import argparse as ap
from cpplint_fix.wrapper import fix_folder
from cpplint_fix.config import CPPLFixConfig
import logging


def main():
    parser = ap.ArgumentParser(description="Run cpplint and apply fixes to source files.")
    parser.add_argument("input", type=Path, help="Input directory containing source files")
    parser.add_argument("--output", "-o", type=Path, default=None, 
                        help="Output directory for fixed files (optional)")
    parser.add_argument("--config", "-c", type=Path, default=None,
                        help="Path to the configuration file (optional)")
    parser.add_argument("--dry-run", action="store_true",
                        help="If set, only print the changes without applying them")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    logging.basicConfig(level=logging.INFO)
    
    config: CPPLFixConfig | None = None    
    if args.config:
        config_path: Path = args.config
        if not config_path.exists():
            logging.error(f"Configuration file {config_path} does not exist.")
            return
        
        with config_path.open('r') as f:
            config_content = f.read()
        
        try:
            config = CPPLFixConfig.model_validate_yaml(config_content)
            logging.info("Configuration loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            return

    fix_folder(input_path, output_path, dry_run=args.dry_run, config=config)

if __name__ == "__main__":
    main()