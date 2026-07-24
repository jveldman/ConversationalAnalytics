{% docs dim_id%}
Unieke primary key voor elke rij in een tabel.
{% enddocs %}

{% docs dim_jaar %}
Het kalenderjaar van waarneming (bijvoorbeeld 2023). 
{% enddocs %}

{% docs dim_geslacht %}
Het geslacht van de persoon: man, vrouw, onbekend of totaal. 
{% enddocs %}

{% docs dim_leeftijd %}
De leeftijd zoals gespecificeerd door het CBS (bijvoorbeeld "12 jaar" of "12 tot 17 jaar"). 
{% enddocs %}

{% docs dim_leeftijd_int %}
De leeftijd als geheel getal (integer) voor rekenoperaties. 
{% enddocs %}

{% docs dim_leeftijd_groep %}
De leeftijd ingedeeld in groepen (bijvoorbeeld "12-17", "65+")
{% enddocs %}

{% docs dim_geboorteland %}
The country where a person was born. In case the person was born in a country that doesn't exist anymore, for example Zaïre, the country of birth gets adjusted to the name of the current country (Dem. Rep. Congo). Sometimes countries are grouped due to the impossibility of splitting out each country, for example people born in Aruba before 1986 get assigned Dutch Antilles. 
{% enddocs %}

{% docs dim_herkomstland %}
Depends on the country of birth of the person in question. For people born in the Netherlands, the country of origin is determined by the country of birth of their parents. When both parents are born outside the Netherlands, the country of birth of the mother determines the country of origin. If the mother is born in the Netherlands, and the father abroad, the country of birth of the father is used. 
{% enddocs %}

{% docs dim_opleiding %}
Het betreft hier de hoogst gevolgde opleiding van de persoon in het desbetreffende jaar. Ze hoeven deze opleiding niet met een diploma of overgangsbewijs te hebben afgerond.
{% enddocs %}

{% docs dim_is_totaal_geslacht %}
Boolean veld: true als deze rij het totaal voor alle geslachten bevat, anders false. 
{% enddocs %}

{% docs dim_is_totaal_leeftijd %}
Boolean veld: true als deze rij het totaal voor alle leeftijd bevat, anders false. 
{% enddocs %}

{% docs dim_is_leeftijd_onbekend %}
Boolean veld: true als in deze rij de leeftijd onbekend is, anders false. 
{% enddocs %}

{% docs dim_is_totaal_opleiding %}
Boolean veld: true als deze rij het totaal voor alle niveaus in opleiding bevat, anders false. 
{% enddocs %}

{% docs dim_is_totaal_geboorteland %}
Boolean value: indicates whether the row displays the total of all birth countries. 
{% enddocs %}

{% docs dim_is_totaal_herkomstland %}
Boolean value: indicates whether the row displays the total of all countries of origin. 
{% enddocs %}

{% docs refresh_date %}
The date on which the table was last refreshed. This does not mean that the newest data was ingested.
{% enddocs %}

{% docs dim_min_leeftijd %}
The minimum age of the group with a specific age range. 
{% enddocs %}

{% docs dim_max_leeftijd %}
The maximum age of the group with a specific age range. 
{% enddocs %}