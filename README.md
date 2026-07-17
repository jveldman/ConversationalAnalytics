```mermaid
flowchart TB
    subgraph UserInterface["🎯 User Interface"]
        U[User] -->|Natural Language Query| S[Streamlit UI <br> Python Ingestion]
        S -->|Question| M[ Mistral LLM]
        M -->|Semantic JSON| S
    end

    subgraph DataWarehouse["🗃️ Data Warehouse"]
        direction TB
        DD[Local DuckDB warehouse.duckdb]
        MD[MotherDuck Cloud]
        DD -.->|Sync| MD
    end

    subgraph DbtCore["⚙️ dbt-core (Pocca)"]
        direction TB
        SO[CBS Statline API] -->|Python| ST[Staging <br> Column Typing & Renaming]
        ST -->|SQL| IM[Intermediate <br> Filter & Transform]
        IM -->|SQL| RP[Reporting Layer]
        RP -->|dbt| MF[manifest.json]
        RP -->|SQL| MM[Measures & Metrics <br> Calculations]

    end

    subgraph Analytics["📊 Analytics Layer"]
        direction TB
        CC[Cube-core <br> Semantic Layer <br>Analytics API] -->|Reads| CJ[cube_manifest.js]
    end

    subgraph Containerization["🐳 Containerization"]
        D[Docker <br> cube-core <br> docker-compose.yml]
    end

    

    S -->|Queries| DbtCore
    DbtCore -->|Transformed data| DD
    CJ -->|Reads| DD
    D -->|Runs| CC
    S -->|Visualization| CC
    
    
    %% style UserInterface fill:#f9f,stroke:#333
    %% style DataWarehouse fill:#bbf,stroke:#333
    %% style DbtCore fill:#9f9,stroke:#333
    %% style Analytics fill:#ff9,stroke:#333
    %% style Containerization fill:#99f,stroke:#333
````
