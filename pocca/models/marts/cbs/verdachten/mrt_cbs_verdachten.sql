-- Remove totals for calculation errors

WITH src AS (
    SELECT 
        *
    FROM {{ ref('int_cbs_verdachten') }}
)

SELECT 
    id,
    MAKE_DATE(jaar, 1, 1) AS jaar, 
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
    refresh_date
FROM src 
WHERE 
    is_totaal_geslacht = FALSE
    AND is_totaal_leeftijd = FALSE
    AND is_totaal_geboorteland = FALSE
    AND is_totaal_herkomstland = FALSE
    