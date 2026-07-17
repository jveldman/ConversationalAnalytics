# Takes the tables from registry.py and sends them to the suitable loaders

from ingestion.cbs_ingestion.loaders import cbs_data_loader, cbs_info_loader, cbs_meta_loader
from ingestion.cbs_ingestion.registry import CBS_DATASETS,CbsDataset
from typing import Literal

# Specify loaders
LOADER_BY_KIND = {
    "data": cbs_data_loader, 
    "info": cbs_info_loader, 
    "meta": cbs_meta_loader
}

# Skip disabled datasets
def load_dataset(dataset: CbsDataset, env: Literal["dev", "prod"]) -> None:
    if not dataset.enabled: 
        print(f"Skipping disabled dataset: {dataset.key}")
        return
    
    if dataset.kind is None: 
        raise ValueError(f"Dataset '{dataset.key}' has no kind configured." )
    if dataset.kind not in ("data", "info", "meta"): 
        raise ValueError(f"Unsupported kind '{dataset.kind}' for dataset '{dataset.key}'.")

    # Select the suitable loader based on kind
    loader = LOADER_BY_KIND[dataset.kind]

    # Show log of progression
    print(
        f"Loading dataset={dataset.key}, "
        f"kind={dataset.kind}, "
        f"table_id={dataset.table_id}, "
        f"target={dataset.target_schema or 'raw'}.{dataset.table_name}"        
    )

    # Execute the selected loader function
    loader(
        table_id = dataset.table_id, 
        schema = dataset.target_schema, 
        table_name = dataset.table_name, 
        cat_url = dataset.cat_url, 
        env = env
    )

    print(f"Finished dataset: {dataset.key}")

def load_all_enabled(env: Literal["dev", "prod"]) -> None: 
    # Loop through entire registry and load every available dataset.
    for dataset in CBS_DATASETS.values():
        if dataset.enabled:
            load_dataset(dataset, env)

def list_datasets() -> list[str]:
    # Function to show all availbale keys.
    return sorted(CBS_DATASETS.keys())