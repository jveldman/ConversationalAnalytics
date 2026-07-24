# Conversational Analytics

**Proof of Concept for AI-powered data analytics using natural language queries**

[![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)

[![Powered by Mistral](https://img.shields.io/badge/Powered_by-Mistral_AI-fa520f?style=flat-square)](https://mistral.ai/)
[![dbt Core](https://img.shields.io/badge/dbt-Core-orange?logo=dbt&logoColor=white)](https://github.com/dbt-labs/dbt-core)
[![Cube](https://img.shields.io/badge/Cube-Core-white?logo=cube&logoColor=white)](https://github.com/cube-js/cube)
[![DuckDB](https://img.shields.io/badge/DuckDB-000000?logo=duckdb&logoColor=white)](https://github.com/duckdb/duckdb)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://github.com/streamlit/streamlit)

## Overview 

This Conversational Analytics POC enables users to query CBS (Dutch Central Bureau of Statistics) data using natural language. Initially, the system ingests CBS tables into a database, transforms them and adds context using dbt and pushes the total into a Cube semantic layer. 

Once the data warehouse is set and the semantic layer is in place, the user has to describe what data they are looking for. Based on the description, an LLM looks for the batch matching data source in the data warehouse. For accuracy the user has to confirm the suggested database, after which they can ask questions about the data. 

Each data question is first handled by an LLM, which checks whether the question concerns data (e.g. *How many suspected crimes happened in 2024?"*) or metadata (e.g. *"What is a crime?"*). The question is pushed through to the data warehouse, respectively the semantic layer, from which an answer is obtained. The result is then returned including the request sent to cube-core in json format.

## Architecture

```mermaid
flowchart TB
  subgraph UserInterface["User Interface"]
    U[User] -->|Natural Language Query| S[Streamlit UI / Python Ingestion]
    S -->|Question| M[Mistral LLM]
    M -->|Semantic JSON| S
  end

  subgraph DataWarehouse["Data Warehouse"]
    direction TB
    DD[Local DuckDB warehouse.duckdb]
    MD[MotherDuck Cloud]
    DD -.->|Sync| MD
  end

  subgraph DbtCore["dbt-core (Pocca)"]
    direction TB
    SO[CBS Statline API] -->|Python| ST[Staging / Column Typing & Renaming]
    ST -->|SQL| IM[Intermediate / Filter & Transform]
    IM -->|SQL| RP[Reporting Layer]
    RP -->|dbt| MF[manifest.json]
    RP -->|SQL| MM[Measures & Metrics / Calculations]
  end

  subgraph Analytics["Analytics Layer"]
    direction TB
    CC[Cube-core / Semantic Layer / Analytics API] -->|Reads| CJ[cube_manifest.js]
  end

  subgraph Containerization["Containerization"]
    D[Docker / cube-core / docker-compose.yml]
  end

  S -->|Queries| DbtCore
  DbtCore -->|Transformed data| DD
  CJ -->|Reads| DD
  D -->|Runs| CC
  S -->|Visualization| CC
```

### Step by Step

1. Ingesting data based on `registry.py` using [ingestion](ingestion/)
2. Transforming data in SQL using dbt based on [dbt_reporting](dbt_reporting/). Here, an ingested data source passes three stages: 
    a. **Staging layer**: Raw data cleaning and standardisation
    b. **Intermediate layer**: Business logic and data enrichment
    c. **Mart layer**: Analytics ready reporting models
3. 


## Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Ingestion | Python, cbsodata | ETL from CBS API to data warehouse |
| Warehouse | DuckDB, MotherDuck | Analytical data storage |
| Transformation | dbt-core | Data modeling and transformation |
| Semantic Layer | Cube-core | Metrics and dimensions abstraction |
| Interface | Streamlit | Conversational UI with LLM integration |
| LLM | Mistral AI | Connecting data to natural language |

## Project Structure

```readme
POC_ConversationalAnalytics/
├── ingestion/           # Data ingestion pipeline
│   ├── cbs_ingestion/   # CBS-specific ETL logic
│   └── duckdb/          # Database connections
├── pocca/              # dbt project (transformation)
│   ├── models/         # SQL models (staging, intermediate, marts)
│   └── dbt_project.yml
├── cube-core/          # Cube.js semantic layer
│   ├── model/          # Cube definitions
│   └── docker-compose.yml
└── poc-chatbot/        # Streamlit UI with LLM
├── app.py          # Main application
└── *.py            # LLM, query, and data source handlers

```

## Configuration

### Environment Variables

Create .env file:

```env

# Motherduck (Production)
MOTHERDUCK_TOKEN=your_token_here
MOTHERDUCK_DB=pocca

##LLM
MISTRAL_API_KEY=your_key_here

#Cube.js
CUBEJS_API_SECRET=your_key_here

```

## Available Datasets

- Haltjongeren (CBS 85993NED) - Youth referred to  a diversion programme for first time offenders
- Verdachten (CBS 20366NED) - Suspects data