#!/bin/bash

# Run dbt-cube-sync to convert dbt models to Cube.js schema
dbt-cube-sync dbt-to-cube \
  --manifest ../pocca/target/manifest.json \
  --catalog ../pocca/target/catalog.json \
  --output ./model/cubes

python3 add_governance.py
