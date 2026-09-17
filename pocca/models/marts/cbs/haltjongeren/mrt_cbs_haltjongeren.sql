 -- Remove totals for calculation errors

WITH src AS (
    SELECT 
        *
    FROM {{ ref('int_cbs_haltjongeren') }}
)

SELECT 
    id,
    MAKE_DATE(jaar, 1, 1) AS jaar, 
    delictgroep, 
    geslacht, 
    leeftijd,
    leeftijd_int, 
    leeftijd_groep, 
    opleiding, 
    CASE 
        WHEN is_overtreding = TRUE THEN 'overtreding'
        WHEN is_misdrijf = TRUE THEN 'misdrijf'
        ELSE 'overig'
    END AS type_delict,
    haltjongeren, 
    haltjongeren_relatief, 
    refresh_date
FROM src 
WHERE 
    is_totaal_misdrijf = FALSE
    AND is_totaal_halt = FALSE
    AND is_totaal_geslacht = FALSE
    AND is_totaal_leeftijd = FALSE
    AND is_totaal_opleiding = FALSE
    