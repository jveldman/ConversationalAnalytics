"""Import functions for CBS tables.

This module provides functions to fetch data from the CBS Statline API
and load it into the data warehouse.
"""

from typing import Literal, Optional

import pandas as pd
import cbsodata
from ingestion.duckdb.connection import get_connection


def catalog_data(table_id: str, cat_url: Optional[str] = None) -> list:
    """Imports the data of a certain table.
    
    Args:
        table_id: CBS Statline table identifier
        cat_url: Optional catalog URL for external CBS data
        
    Returns:
        List of data rows from the CBS API
    """
    if cat_url is None:
        return cbsodata.get_data(table_id)
    return cbsodata.get_data(table_id, catalog_url=cat_url)


def catalog_info(table_id: str, cat_url: Optional[str] = None) -> dict:
    """Imports information on a certain table.
    
    Args:
        table_id: CBS Statline table identifier
        cat_url: Optional catalog URL for external CBS data
        
    Returns:
        Dictionary containing table information
    """
    if cat_url is None:
        return cbsodata.get_info(table_id)
    return cbsodata.get_info(table_id, catalog_url=cat_url)


def catalog_meta(table_id: str, cat_url: Optional[str] = None) -> list:
    """Imports metadata on a certain table.
    
    Args:
        table_id: CBS Statline table identifier
        cat_url: Optional catalog URL for external CBS data
        
    Returns:
        List of metadata dictionaries
    """
    if cat_url is None:
        return cbsodata.get_meta(table_id, "DataProperties")
    return cbsodata.get_meta(table_id, "DataProperties", catalog_url=cat_url)


def load_to_db(
    env: Literal["dev", "prod"],
    table_id: str,
    schema: str,
    table_name: str,
    df: pd.DataFrame
) -> None:
    """Loads data into the database. Creates schema if not available.
    
    Args:
        env: Environment ('dev' for local DuckDB, 'prod' for MotherDuck)
        table_id: CBS Statline table identifier
        schema: Target schema name
        table_name: Target table name
        df: Pandas DataFrame containing the data to load
    """
    con = get_connection(env)
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    con.execute(f"""
    CREATE OR REPLACE TABLE {schema}.{table_name} AS 
    SELECT * FROM df
    """)

    print(f"Loaded {table_id} into {schema}.{table_name}")
    
    con.close()