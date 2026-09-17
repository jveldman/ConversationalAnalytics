
-- Trim and clean data

WITH source AS (
    SELECT * FROM {{ source('raw_cbs', 'cbs_data_haltjongeren') }}
)

SELECT
    ID::INTEGER AS id,
    LOWER(TRIM(Delictgroep))::VARCHAR AS delictgroep,
    LOWER(TRIM(Geslacht))::VARCHAR AS geslacht,
    LOWER(TRIM(Leeftijd))::VARCHAR AS leeftijd,
    LOWER(TRIM(Opleiding))::VARCHAR AS opleiding,
    Perioden::INTEGER AS jaar,
    CASE 
        WHEN TRIM(HaltJongeren_1) IN ('', '.') THEN NULL 
        ELSE CAST(TRIM(HaltJongeren_1) AS INTEGER) 
    END AS haltjongeren,
    CASE 
        WHEN TRIM(HaltJongerenRelatief_2) IN ('', '.') THEN NULL 
        ELSE CAST(TRIM(HaltJongerenRelatief_2) AS INTEGER) 
    END AS haltjongeren_relatief, 
    CURRENT_DATE() AS refresh_date
FROM source