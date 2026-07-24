WITH veelplegers AS(
    SELECT 
        *
    FROM {{ source('raw_cbs', 'cbs_data_veelplegers')   }}
)

SELECT 
    ID::INTEGER AS id, 
    Geslacht::VARCHAR AS geslacht, 
    Leeftijd::VARCHAR AS leeftijd, 
    Recidive::VARCHAR AS recidive, 
    Perioden::INTEGER AS jaar, 
    VerdachtenVanMisdrijven_1::INTEGER AS verdachten_van_misdrijven, 
    CURRENT_DATE() AS refresh_date
FROM veelplegers