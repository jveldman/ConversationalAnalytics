WITH source AS(
    SELECT * FROM {{ref('stg_ownership')}}
)

SELECT * FROM source