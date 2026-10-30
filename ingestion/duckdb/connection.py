"""Set up connection with local or cloud database.

Provides connection utilities for DuckDB (local) and MotherDuck (cloud).
"""

import os
from typing import Literal

import duckdb
from dotenv import load_dotenv

load_dotenv()


def get_connection(env: Literal["dev", "prod"]):
    """Connect to database depending on input environment.
    
    Args:
        env: Environment identifier ('dev' for local DuckDB, 'prod' for MotherDuck)
        
    Returns:
        DuckDB connection object
        
    Raises:
        ValueError: If env is not 'dev' or 'prod'
        RuntimeError: If required environment variables are missing for prod
    """
    if env == "dev":
        db_path = os.environ.get("DUCKDB_PATH", "data/duckdb/warehouse.duckdb")
        print("Accessing local DuckDB database...")
        return duckdb.connect(db_path)
    elif env == "prod":
        token = os.environ.get("MOTHERDUCK_TOKEN")
        if not token:
            raise RuntimeError(
                "MOTHERDUCK_TOKEN environment variable is required for prod environment. "
                "Please set it in your .env file or environment."
            )
        db = os.environ.get("MOTHERDUCK_DB", "pocca")
        print("Accessing MotherDuck database...")
        return duckdb.connect(f"md:{db}?motherduck_token={token}")
    
    raise ValueError('env must be "dev" or "prod".')
