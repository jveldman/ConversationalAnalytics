# dbt Transformation Layer 

**Transformation pipeline for conversational analytics**

## Overview

Transforms raw data, for now mainly CBS Statline API data, into analytics-ready models for the semantic layer. 

## Project Structure 

```
models/
├── staging/            # Raw data cleaning (stg_)
├── intermediate/       # Business logic (int_)
├── marts/              # Analytics-ready models (mrt_)
├── semantic_models/    # MetricFlow definitions
└── sources/            # Source definitions (src_.yml)
seeds/                  # Static data (dim_age_band.csv)
dbt_packages/       # Installed packages 
docs/               # Documentation on tables and columns
├── cbs                 # CBS documentation
├── dimensions/         # Dimension documentation per source
snapshots/
tests/

```

For information about the ingestion before staging, please read [this file](/ingestion/README.md). 

### Staging

In staging de datatypes are set for each column. Next to that, the columns are trimmed for white spaces and indicators of empty values, such as ".", are replaced by `NULL`. 

### Intermediate

Some values are standardised so that they fit with other columns. Totals are kept in, but are marked as totals by boolean columns. When certain categories belong to a larger category, then this is marked with boolean columns as well, for example `is_misdrijf`. Lastly the ages are standardised, so that tables with precise ages can be compared with tables that display age groups. 

### Mart 

These are the final reporting tables that are used for analytics. The rows containing totals are filtered out to prevent double counting. Larger categories (see intermediate) are added as a row split. 

## Data Sources 

- CBS Haltjongeren (85993NED) - Data on the Dutch youth diversion program
- CBS Verdachten (20366NED) - Data on suspects in the Netherlands

## Getting Started 

### Prerequisites

- Python 3.10+
- dbt-core (`pip install dbt-core dbt-duckdb`)
- DuckDB (included with `dbt-duckdb`)

### 1. Clone & Install 

```bash
git clone <repo-url>
cd ConversationalAnalytics/pocca

# Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate

# Install required packages
pip install -r ../requirements.txt
```

### 2. Configure Environment 

Create a `.env` file in the parent directory that looks as follows: 

```bash
# DuckDB (Development)
DUCKDB_PATH=path_to_local_db

# MotherDuck (Production)
MOTHERDUCK_TOKEN=your__motherduck_token
MOTHERDUCK_DB=your_db_name
```

### 3. Set Up Local DuckDB (dev)

Ensure that the local warehouse exists: 

```bash
duckdb data/duckdb/warehouse.duckdb
```

### 4. Run The Pipeline

```bash 
# Run all models to a local duckdb database
dbt run --target dev
# run all models to a cloud DuckDB database
dbt run --target prod

# Test all models 
dbt test

# Run and test all models 
dbt build

# Run and test a specific model
dbt build -s <model_name>
```

## 5. Generate Documentation 

```bash 
dbt docs generate
dbt docs serve
```

