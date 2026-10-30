"""Type definitions for CBS dataset ingestion."""

from typing import Literal

# Dataset kinds supported by the ingestion pipeline
DatasetKind = Literal["data", "info", "meta"]

# Write modes for loading data into the warehouse
WriteMode = Literal["append", "replace", "fail"]