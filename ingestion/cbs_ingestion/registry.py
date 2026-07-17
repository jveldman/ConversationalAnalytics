## All the sources that should be loaded to the data warehouse

from dataclasses import dataclass
from typing import Optional
from ingestion.cbs_ingestion.dataset_types import DatasetKind, WriteMode

@dataclass(frozen = True)
class CbsDataset: 
    key: str
    table_id: str
    table_name: str

    cat_url: Optional[str] = None           # Specific url for external data, e.g. "dataderden.cbs.nl"
    kind: Optional[DatasetKind] = None      # data, info, or meta
    target_schema: Optional[str] = None     # schema to write to
    write_mode: WriteMode = "append"        # append, replace, fail
    enabled: bool = True                    # Should it run in default batch mode?
    description: Optional[str] = None       # Documentation for humans and logs

CBS_DATASETS = {
    "haltjongeren_data" : CbsDataset(
        key = "haltjongeren_data", 
        table_id = "85993NED", 
        table_name = "cbs_data_haltjongeren", 
        kind = "data", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "haltjongeren_info" : CbsDataset(
        key = "haltjongeren_info", 
        table_id = "85993NED", 
        table_name = "cbs_info_haltjongeren", 
        kind = "info", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "haltjongeren_meta" : CbsDataset(
        key = "haltjongeren_meta", 
        table_id = "85993NED", 
        table_name = "cbs_meta_haltjongeren", 
        kind = "meta", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "veelplegers_data" : CbsDataset(
        key = "veelplegers_data", 
        table_id = "85657NED", 
        table_name = "cbs_data_veelplegers", 
        kind = "data", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "veelplegers_info" : CbsDataset(
        key = "veelplegers_info", 
        table_id = "85657NED", 
        table_name = "cbs_info_veelplegers", 
        kind = "info", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    
    "veelplegers_meta" : CbsDataset(
        key = "veelplegers_meta", 
        table_id = "85657NED", 
        table_name = "cbs_meta_veelplegers", 
        kind = "meta", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "verdachten_data" : CbsDataset(
        key = "verdachten_data", 
        table_id = "20366NED", 
        table_name = "cbs_data_verdachten", 
        cat_url = "dataderden.cbs.nl",
        kind = "data", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "verdachten_info" : CbsDataset(
        key = "verdachten_info", 
        table_id = "20366NED", 
        table_name = "cbs_info_verdachten", 
        cat_url = "dataderden.cbs.nl",
        kind = "info", 
        target_schema = "raw", 
        write_mode = "replace", 
    ), 

    "verdachten_meta" : CbsDataset(
        key = "verdachten_meta", 
        table_id = "20366NED", 
        table_name = "cbs_meta_verdachten", 
        cat_url = "dataderden.cbs.nl",
        kind = "meta", 
        target_schema = "raw", 
        write_mode = "replace", 
    )
}
