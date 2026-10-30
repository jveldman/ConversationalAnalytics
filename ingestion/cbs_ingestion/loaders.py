"""Loads CBS data to the database based on their type (data, info, meta).

This module provides three loader functions that fetch data from the CBS API
and load it into the warehouse with appropriate metadata.
"""

from datetime import datetime, timezone
from typing import Literal, Optional

import pandas as pd
from ingestion.cbs_ingestion.cbs import (
    catalog_data,
    catalog_info,
    catalog_meta,
    load_to_db
)


def cbs_data_loader(
    env: Literal["dev", "prod"],
    table_id: str,
    schema: str = "raw",
    table_name: Optional[str] = None,
    cat_url: Optional[str] = None
) -> None:
    """Loads the data to the database and adds a refresh date (vernieuwd_op).
    
    Args:
        env: Environment ('dev' for local DuckDB, 'prod' for MotherDuck)
        table_id: CBS Statline table identifier
        schema: Target schema name (default: 'raw')
        table_name: Target table name (default: table_id lowercase)
        cat_url: Optional catalog URL for external CBS data
    """
    # Fetch data and convert to Pandas DataFrame
    df = pd.DataFrame(catalog_data(table_id, cat_url))
    df["vernieuwd_op"] = datetime.now(timezone.utc)

    # Create table name if not provided
    if table_name is None:
        table_name = table_id.lower()

    # Load data into database
    load_to_db(env, table_id, schema, table_name, df)


def cbs_info_loader(
    env: Literal["dev", "prod"],
    table_id: str,
    schema: str = "raw",
    table_name: Optional[str] = None,
    cat_url: Optional[str] = None
) -> None:
    """Loads a datasource's information to the database and adds a refresh date.
    
    Args:
        env: Environment ('dev' for local DuckDB, 'prod' for MotherDuck)
        table_id: CBS Statline table identifier
        schema: Target schema name (default: 'raw')
        table_name: Target table name (default: table_id lowercase)
        cat_url: Optional catalog URL for external CBS data
    """
    # Fetch info and convert to Pandas DataFrame
    df = pd.DataFrame([catalog_info(table_id, cat_url)])
    df["vernieuwd_op"] = datetime.now(timezone.utc)

    # Create table name if not provided
    if table_name is None:
        table_name = table_id.lower()

    # load data into database
    load_to_db(env, table_id, schema, table_name, df)


def cbs_meta_loader(
    env: Literal["dev", "prod"],
    table_id: str,
    schema: str = "raw",
    table_name: Optional[str] = None,
    cat_url: Optional[str] = None
) -> None:
    """Loads a datasource's metadata to the database and adds a refresh date.
    
    Args:
        env: Environment ('dev' for local DuckDB, 'prod' for MotherDuck)
        table_id: CBS Statline table identifier
        schema: Target schema name (default: 'raw')
        table_name: Target table name (default: table_id lowercase)
        cat_url: Optional catalog URL for external CBS data
    """
    # Fetch meta and convert to Pandas DataFrame
    df = pd.DataFrame(catalog_meta(table_id, cat_url))
    df["vernieuwd_op"] = datetime.now(timezone.utc)

    # Create table name if not provided
    if table_name is None:
        table_name = table_id.lower()

    # load data into database
    load_to_db(env, table_id, schema, table_name, df)