WITH source AS (
    SELECT * FROM {{ ref('ownership') }}
)

SELECT 
    model_name, 
    model_type, 
    data_owner, 
    data_steward, 
    data_steward_email,
    current_date AS last_updated
FROM source
