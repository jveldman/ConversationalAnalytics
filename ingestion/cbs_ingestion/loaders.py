"""Loads CBS data to the database based on their type (data, info, meta)"""
import pandas as pd
from datetime import datetime, timezone
from ingestion.cbs_ingestion.cbs import catalog_data, catalog_info, catalog_meta, load_to_db
from typing import Literal

def cbs_data_loader(env: Literal["dev", "prod"], table_id: str, schema: str = "raw", table_name: str = None, cat_url = None):
    """Loads the data to the database and adds a refresh date (vernieuwd_op)"""
    
    # Fetch data and convert to Pandas DataFrame
    df = pd.DataFrame(catalog_data(table_id, cat_url))
    df["vernieuwd_op"] = datetime.now(timezone.utc) 

    #Create table name if not provided
    if table_name is None: 
        table_name = table_id.lower()

    # Load data into database 
    load_to_db(env, table_id, schema, table_name, df)
    
    return

def cbs_info_loader(env: Literal["dev", "prod"],table_id: str, schema: str = "raw", table_name: str = None, cat_url = None):
    """Loads a datasource's information to the database and adds a refresh date (vernieuwd_op)"""

    # Fetch info and convert to Pandas Dataframe 
    df = pd.DataFrame([catalog_info(table_id, cat_url)])   
    df["vernieuwd_op"] = datetime.now(timezone.utc) 

    # Create table name if not provided 
    if table_name is None: 
        table_name = table_id.lower()

    # load data into database
    load_to_db(env, table_id, schema, table_name, df)

    return

def cbs_meta_loader(env: Literal["dev", "prod"], table_id: str, schema: str = "raw", table_name: str = None, cat_url = None):
    """Loads a datasource's metadata to the database and adds a refresh date (vernieuwd_op)"""

    # Fetch info and convert to Pandas Dataframe 
    df = pd.DataFrame(catalog_meta(table_id, cat_url))  
    df["vernieuwd_op"] = datetime.now(timezone.utc)  

    # Create table name if not provided 
    if table_name is None: 
        table_name = table_id.lower()

    # load data into database
    load_to_db(env, table_id, schema, table_name, df)

    return