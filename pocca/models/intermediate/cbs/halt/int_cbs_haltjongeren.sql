{{
  config(materialized = 'table')
}}

WITH  src AS(
    SELECT * FROM {{ ref('stg_cbs_haltjongeren') }}
), 

age_band AS(
    SELECT * FROM {{ ref('dim_age_band') }}
),

-- Create booleans for totals, crimes, offenses, total crimes and total offenses. 
parsed AS (
    SELECT 
        *,
        CASE 
            WHEN leeftijd ~ '^[0-9]+ ?jaar$'
                THEN cast(split_part(leeftijd, ' ', 1) AS INTEGER)
            ELSE NULL
        END AS leeftijd_int, 
        CASE WHEN lower(geslacht) = 'totaal' THEN TRUE ELSE FALSE END AS is_totaal_geslacht, 
        CASE WHEN lower(leeftijd) = 'totaal' THEN TRUE ELSE FALSE END AS is_totaal_leeftijd,
        CASE 
            WHEN lower(leeftijd) ILIKE '%overig%' 
            OR lower(leeftijd) ILIKE '%onbekend%'
        THEN TRUE ELSE FALSE END AS is_leeftijd_onbekend,
        CASE 
            WHEN lower(delictgroep) IN ('geweldsmisdrijven', 'vernieling en openbare orde', 'vermogensmisdrijven', 'vuurwerkmisdrijven', 'overige misdrijven')
            THEN TRUE ELSE FALSE 
        END AS is_misdrijf,
        CASE 
            WHEN lower(delictgroep) in ('baldadigheid', 'overtreding leerplichtwet', 'vuurwerkovertredingen', 'overige overtredingen')
            THEN TRUE ELSE FALSE
        END AS is_overtreding, 
        CASE WHEN lower(delictgroep) = 'totaal aantal halt-jongeren' THEN TRUE ELSE FALSE END AS is_totaal_halt, 
        CASE WHEN lower(delictgroep) = 'totaal misdrijven' THEN TRUE ELSE FALSE END AS is_totaal_misdrijf,
        CASE WHEN lower(delictgroep) = 'totaal overtredingen' THEN TRUE ELSE FALSE END AS is_totaal_overtreding,
        CASE WHEN lower(opleiding) ILIKE '%totaal%' THEN TRUE ELSE FALSE END AS is_totaal_opleiding, 
        CURRENT_DATE() AS refresh_date
        FROM src
), 

-- merge with age category table for scalability
parsed_ages AS(
    SELECT 
        p.*, 
        ab.age_band_label as leeftijd_groep
    FROM parsed AS p
    LEFT JOIN age_band as ab
    ON (
        p.leeftijd_int IS NOT NULL 
        AND p.leeftijd_int >= ab.age_min 
        AND (
            p.leeftijd_int <= ab.age_max
            OR ab.age_max IS NULL
        )
    )
    OR (
        ab.age_band_label = 'Totaal'
        AND p.is_totaal_leeftijd IS TRUE
        AND ab.age_min IS NULL 
        AND ab.age_max IS NULL
    )
    OR (
        ab.age_band_label = 'Onbekend'
        AND p.is_leeftijd_onbekend IS TRUE
        AND ab.age_min IS NULL 
        AND ab.age_max IS NULL
    )
)

SELECT 
    id,
    jaar,  
    delictgroep, 
    geslacht, 
    leeftijd,
    leeftijd_int, 
    leeftijd_groep,  
    opleiding, 
    haltjongeren, 
    haltjongeren_relatief, 
    is_misdrijf, 
    is_overtreding, 
    is_totaal_misdrijf, 
    is_totaal_overtreding, 
    is_totaal_halt,
    is_totaal_geslacht, 
    is_totaal_leeftijd, 
    is_leeftijd_onbekend, 
    is_totaal_opleiding, 
    refresh_date
FROM parsed_ages



