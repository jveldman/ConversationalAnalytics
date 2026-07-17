"""Set up connection with local or cloud database"""
import os
import duckdb
from dotenv import load_dotenv 
from typing import Literal 

load_dotenv()

def get_connection(env: Literal["dev", "prod"]):
    """Connect to database depending on input with run"""
    if env == "dev":
        db_path = os.environ.get("DUCKDB_PATH", "data/duckdb/warehouse.duckdb")
        print("Accessing local DuckDB database...")
        return duckdb.connect(db_path)
    elif env == "prod":
        token = os.environ["MOTHERDUCK_TOKEN"]
        db = os.environ.get("MOTHERDUCK_DB", "pocca")
        print('Accessing MotherDuck database...')
        return duckdb.connect(f"md:{db}?motherduck_token={token}")
    
    else: 
        raise ValueError('env must be "dev" or "prod".')
        

