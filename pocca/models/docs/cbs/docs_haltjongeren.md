{% docs tbl_stg_haltjongeren %}

The table almost directly based on the ingestion model. Only changes made are that data types are set and that empty spaces are cleaned. Includes rows with total values, therefore it is not suitable for calculations without further transformations. 

{% enddocs %}


{% docs tbl_int_haltjongeren %}

De tabel bevat gegevens over het absolute aantal jongeren per bevolkingsgroep en het aantal jongeren per 10 000 inwoners uit de geselecteerde bevolkingsgroep dat naar Halt verwezen is voor een Halt-traject (de zogenoemde Halt-jongeren) en dit traject in het publicatiejaar heeft afgerond. Er wordt onderscheid gemaakt naar delictgroep, geslacht, leeftijd en opleiding. De tabel bevat ook gegevens over het type delict (absoluut en relatief) per bevolkingsgroep.

De tabel geeft aan hoeveel jongeren in het publicatiejaar een Halt-traject hebben afgerond per soort delict. Een jongere die binnen een jaar meer dan één keer naar Halt is verwezen, wordt in de tabel maar één keer meegeteld. Het soort delict wordt dan bepaald aan de hand van het eerste delict waarvoor de jongere naar Halt is verwezen.

Van personen die niet voorkomen in de Basis Registratie Personen (BRP) ontbreken vaak persoonsgegevens. Deze personen zijn wel meegeteld in de absolute cijfers, maar niet in de relatieve. 

Sinds juni 2024 zijn de voorwaarden om jongeren een Halt-afdoening aan te bieden gewijzigd (zie link naar Halt-besluit in paragraaf 3). Door deze gewijzigde voorwaarden is de verwachting dat er jaarlijks meer Halt-afdoeningen aangeboden zullen worden. 

Vuurwerkmisdrijven zijn vanaf verslagjaar 2020 opgenomen als aparte delictgroep. Voorheen viel deze categorie onder de delictgroep vuurwerkovertredingen.


Status van de cijfers:
Gegevens zijn beschikbaar vanaf 2005 tot en met 2025. De cijfers zijn definitief.
Gegevens over het onderwijsniveau zijn beschikbaar vanaf verslagjaar 2013 en nog niet beschikbaar voor het laatste verslagjaar.

Wijzigingen per 29 mei 2026:
Cijfers over 2025 en over het hoogst gevolgde onderwijsniveau voor 2024 zijn toegevoegd. 

Wanneer komen er nieuwe cijfers beschikbaar:
Nieuwe cijfers komen doorgaans vier maanden na afloop van het verslagjaar beschikbaar.

{% enddocs %}


{% docs tbl_mrt_haltjongeren %}
Reporting model voor conversational en exploratory analytics op CBS Halt data. 
Dit model bevat alleen observaties die geen totalen zijn en is bedoeld als de betrouwbare laag 
om te filteren op jaar, delictgroep, geslacht, leeftijd en opleidingsniveau. 
Dit is het primaire model dat wordt geconsumeerd door de semantische laag. 
{% enddocs %}


{% docs dim_delictgroep %}
Categoraal veld: het type delict zoals geregistreerd door de politie en geclassificeerd volgens CBS-standaard. hoofdgroepen: geweldsmisdrijven (mishandeling, bedreiging, seksuele misdrijven), vermogensmisdrijven (diefstal, inbraak, winkeldiefstal), vernieling en openbare orde (vernieling, brandstichting, openlijke geweldpleging), verkeersmisdrijven, drugsmisdrijven, vuurwapenmisdrijven, en overtredingen (baldadigheid, leerplichtwet). Bron: CBS StatLine 81947NED [web:21].
{% enddocs %}

{% docs tpc_haltjongeren %}
Het totaal aantal Halt-jongeren dat is verwezen naar Halt voor het plegen van een strafbaar feit. Het betreft hier zowel overtredingen als misdrijven.
Cijfers worden afgerond op tientallen, hierdoor komt het totaal soms niet overeen met de som der delen.
{% enddocs %}

{% docs tpc_haltjongeren_relatief %}
Het aantal Halt-jongeren per 10 000 inwoners uit de geselecteerde bevolkingsgroep dat is verwezen naar Halt voor het plegen van een strafbaar feit. Het betreft hier zowel overtredingen als misdrijven. 
{% enddocs %}

{% docs dim_is_misdrijf %}
Boolean indicator: true als de delictgroep een misdrijf is (geweldsmisdrijven, vernieling en openbare orde, vermogensmisdrijven, vuurwerkmisdrijven, of overige misdrijven), false anders.
{% enddocs %}

{% docs dim_is_overtreding %}
Boolean indicator: true als de delictgroep een overtreding is (baldadigheid, overtreding leerplichtwet, vuurwerkovertredingen, of overige overtredingen), false anders.
{% enddocs %}

{% docs dim_is_totaal_halt %}
Boolean indicator: true als de rij het totaal voor alle HALT-jongeren representeert (delictgroep = 'totaal aantal halt-jongeren'), false voor individuele delictgroepen.
{% enddocs %}

{% docs dim_is_totaal_misdrijf %}
Boolean indicator: true als de rij het totaal voor alle misdrijven representeert (delictgroep = 'totaal misdrijven'), false voor individuele misdrijf-categorieën.
{% enddocs %}

{% docs dim_is_totaal_overtreding %}
Boolean indicator: true als de rij het totaal voor alle overtredingen representeert (delictgroep = 'totaal overtredingen'), false voor individuele overtreding-categorieën.
{% enddocs %}

{% docs dim_type_delict %}
Categorieveld voor de juridische classificatie van een delict. De waarde geeft aan of een registratie hoort bij een misdrijf, een overtreding of een overige categorie. Dit veld is bedoeld voor analyse, filtering en aggregatie in conversaties met data.
{% enddocs %}