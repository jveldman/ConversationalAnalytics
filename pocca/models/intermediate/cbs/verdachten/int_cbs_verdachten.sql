
with src AS(
    SELECT * FROM {{ ref('stg_cbs_verdachten') }}
), 

age_band AS(
    SELECT * FROM {{ ref('dim_age_band') }}
), 

-- Standardise age and set totals apart
parsed AS(
    SELECT 
        *, 
        CAST(LIST_EXTRACT(regexp_extract_all(leeftijd, '\d+'), 1) AS INTEGER) AS min_leeftijd, 
        CASE 
            WHEN array_length(regexp_extract_all(leeftijd, '\d+')) > 1
            THEN CAST(LIST_EXTRACT(regexp_extract_all(leeftijd, '\d+'), 2) AS INTEGER) - 1
            ELSE NULL
        END AS max_leeftijd,
        CASE WHEN lower(geslacht) ILIKE '%totaal%' THEN TRUE ELSE FALSE END AS is_totaal_geslacht, 
        CASE WHEN lower(leeftijd) = 'totaal' THEN TRUE ELSE FALSE END AS is_totaal_leeftijd, 
        CASE WHEN lower(geboorteland) = 'totaal' THEN TRUE ELSE FALSE END AS is_totaal_geboorteland, 
        CASE WHEN lower(geboorteland) = 'totaal' THEN TRUE ELSE FALSE END AS is_totaal_herkomstland, 
        CURRENT_DATE() AS refresh_date
    FROM src
), 

-- Add age_band tables to allow comparisons
parsed_ages AS(
    SELECT 
        p.*, 
        ab.age_band_label AS leeftijd_groep
    FROM parsed as p 
    LEFT JOIN age_band AS ab
    ON (
        p.min_leeftijd = ab.age_min
        AND p.max_leeftijd = ab.age_max)
    OR (p.min_leeftijd = ab.age_min
        AND p.max_leeftijd IS NULL)
    OR (
        ab.age_band_label = 'Totaal'
        AND p.is_totaal_leeftijd IS TRUE 
        AND ab.age_min IS NULL
        AND ab.age_max IS NULL
    )
)

SELECT 
    id,
    jaar,  
    geslacht, 
    min_leeftijd,
    max_leeftijd, 
    leeftijd_groep,  
    geboorteland, 
    herkomstland, 
    totaal_verdachten_van_misdrijven, 
    verdachten_van_vermogensmisdrijven,
    verdachten_van_vernieling_opb_orde, 
    verdachten_van_verkeersmisdrijven, 
    verdachten_van_drugsmisdrijven, 
    verdachten_van_vuurwapenmisdrijven, 
    totaal_verdachten_van_misdrijven_p10k, 
    verdachten_van_vermogensmisdrijven_p10k, 
    verdachten_van_vernieling_opb_orde_p10k, 
    verdachten_van_verkeersmisdrijven_p10k, 
    verdachten_van_drugsmisdrijven_p10k, 
    verdachten_van_vuurwapenmisdrijven_p10k, 
    is_totaal_geslacht, 
    is_totaal_leeftijd, 
    is_totaal_geboorteland, 
    is_totaal_herkomstland,
    CURRENT_DATE() AS refresh_date
FROM parsed_ages
