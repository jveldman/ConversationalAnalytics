{% docs tbl_stg_ownership%}
Geeft weer waar bepaalde data vandaan komt, welke organisatie de eigenaar van een bepaald model is. In deze tabel staat ook informatie over de data steward en hoe deze steward gecontacteerd kan worden. 
{% enddocs %}

{% docs dim_model_name %}
De naam van het model waarnaar gerefereerd wordt. 
{% enddocs %}

{% docs dim_model_type %}
Het type model. Kan ' staging' , 'intermediate', 'mart' of 'semantic' zijn. 
{% enddocs %}

{% docs dim_data_owner %}
De eigenaar van het model, ookwel de leverancier van de data. Dit zijn vaak organisaties zoals het CBS, DJI, of CJIB. Er zijn GEEN contactgegevens toegevoegd, omdat contact over datavragen dient te verlopen via de data steward. 
{% enddocs %}

{% docs dim_data_steward %}
De naam van de persoon die het eerst in lijn staat voor datavragen van gebruikers. De data steward staat tussen de gebruiker en de data owner in, en kan zo zorgen voor efficiënte communicatie tussen juridische en analytische specialisten. 
{% enddocs %}

{% docs dim_data_steward_email %}
Het email adres waarop de data steward gecontacteerd kan worden. 
{%enddocs %}