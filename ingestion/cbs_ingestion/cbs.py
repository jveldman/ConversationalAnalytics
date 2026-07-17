"""Import functions for CBS tables"""
import cbsodata
from ingestion.duckdb.connection import get_connection
import pandas as pd
from typing import Literal 

def catalog_data(table_id: str, cat_url = None):
    """Imports the data of a certain table. Cat_url for external CBS data"""
    if cat_url is None: 
        return cbsodata.get_data(table_id)
    return cbsodata.get_data(table_id, catalog_url = cat_url)

def catalog_info(table_id: str, cat_url = None):
    """Imports information on a certain table. Cat_url for external CBS data"""
    if cat_url is None: 
        return cbsodata.get_info(table_id)
    return cbsodata.get_info(table_id, catalog_url = cat_url)

def catalog_meta(table_id: str, cat_url = None):
    """Imports metadata on a certain table. Cat_url for external CBS data"""
    if cat_url is None: 
        return cbsodata.get_meta(table_id, "DataProperties")
    return cbsodata.get_meta(table_id,"DataProperties", catalog_url = cat_url)

def load_to_db(env: Literal["dev", "prod"], table_id: str, schema: str, table_name: str, df: pd.DataFrame):
    """Loads data into the database. Creates schema if not available"""
    con = get_connection(env)
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    con.execute(f"""
    CREATE OR REPLACE TABLE {schema}.{table_name} AS 
    SELECT * FROM df
    """)

    print(f"✓ Loaded {table_id} into {schema}.{table_name}")
    
    con.close()
    return