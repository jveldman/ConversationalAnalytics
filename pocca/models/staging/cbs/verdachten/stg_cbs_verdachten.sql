WITH verdachten AS (
    SELECT 
        *
    FROM {{ source('raw_cbs', 'cbs_data_verdachten')    }}
)

SELECT 
    ID::INTEGER AS id, 
    Geslacht::VARCHAR AS geslacht, 
    Leeftijd::VARCHAR As leeftijd,
    Geboorteland::VARCHAR AS geboorteland,
    Herkomstland::VARCHAR AS herkomstland,
    Perioden::INTEGER AS jaar,
    TotaalVerdachtenVanMisdrijven_1::INTEGER AS totaal_verdachten_van_misdrijven, 
    VerdachtenVanVermogensmisdrijven_2::INTEGER AS verdachten_van_vermogensmisdrijven,
    VerdachtenVanVernielingEnOpenbOrde_3::INTEGER AS Verdachten_van_vernieling_opb_orde,
    VerdachtenVanGeweldsmisdrijven_4::INTEGER AS verdachten_van_geweldsmisdrijven,
    VerdachtenVanVerkeersmisdrijven_5::INTEGER AS verdachten_van_verkeersmisdrijven,
    VerdachtenVanDrugsmisdrijven_6::INTEGER AS verdachten_van_drugsmisdrijven, 
    VerdachtenVanVuurWapenmisdrijven_7::INTEGER AS verdachten_van_vuurwapenmisdrijven,
    TotaalVerdachtenVanMisdrijven_8::INTEGER AS totaal_verdachten_van_misdrijven_p10k, 
    VerdachtenVanVermogensmisdrijven_9::INTEGER AS verdachten_van_vermogensmisdrijven_p10k,
    VerdachtenVanVernielingEnOpenbOrde_10::INTEGER AS Verdachten_van_vernieling_opb_orde_p10k,
    VerdachtenVanGeweldsmisdrijven_11::INTEGER AS verdachten_van_geweldsmisdrijven_p10k,
    VerdachtenVanVerkeersmisdrijven_12::INTEGER AS verdachten_van_verkeersmisdrijven_p10k,
    VerdachtenVanDrugsmisdrijven_13::INTEGER AS verdachten_van_drugsmisdrijven_p10k, 
    VerdachtenVanVuurWapenmisdrijven_14::INTEGER AS verdachten_van_vuurwapenmisdrijven_p10k, 
    CURRENT_DATE() AS refresh_date
FROM verdachten
    