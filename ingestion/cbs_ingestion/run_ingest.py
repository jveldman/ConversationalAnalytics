# Parser to run all ingestion at once
import argparse
from ingestion.cbs_ingestion.writer import load_all_enabled, list_datasets

def build_parser() -> argparse.ArgumentParser:

    # Create Command Line Interface (CLI)
    parser = argparse.ArgumentParser(
        description="Run data ingestion to local / cloud warehouse."
    )

    parser.add_argument(
        "--list", 
        action = "store_true",
        help = "List available dataset keys",
    )

    parser.add_argument(
        "--db", 
        choices = ["dev", "prod"],
        default = "dev",
        help = "Select the environment. Dev runs in a local warehouse.duckdb, prod runs on Motherduck in cloud.",
    )

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # If list is passed, print all available datasets in the called list_datasets function. 
    if args.list:
        print("Available datasets:")
        for key in list_datasets():
            print(f" - {key}")
        return
    
    # If no arguments are passed, it loads all the datasets available. 
    load_all_enabled(env = args.db)


if __name__ == "__main__":
    main()
    


