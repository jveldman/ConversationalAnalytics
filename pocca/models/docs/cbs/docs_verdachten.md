{% docs tbl_int_cbs_verdachten %}

The intermediate table for suspects. In this table, booleans are created for totals, such as the total of all ages or all genders. 
The age band table is added to be able to link age groups to ages per year. 

{% enddocs %}

{% docs tbl_mrt_cbs_verdachten %}
This table is the version suitable for analytics and is used by Cube-core's semantic layer. It includes the same dimensions as the intermediate model, only then with all the total rows filtered out to prevent double counting. 

{% enddocs %}

{% docs tbl_stg_verdachten %}

The staging table for data on suspects. THis table is almost identical to the table in ingestion. 
No further transformations have been done, besides setting the datatype. 

{% enddocs %}

{% docs tpc_totaal_verdachten_van_misdrijven %}
The total number of people suspected of committing a crime. 
{% enddocs %}

{% docs tpc_verdachten_van_vermogensmisdrijven %}
The number people suspected of property crime.
{% enddocs %}

{% docs tpc_verdachten_van_vernieling_opb_orde %}
The number of people suspected of desctruction of public order. 
{% enddocs %}

{% docs tpc_verdachten_van_geweldsmisdrijven %}
The number of people suspected of violent crimes. 
{% enddocs %}

{% docs tpc_verdachten_van_verkeersmisdrijven %}
The number of people suspected of traffic offenses. 
{% enddocs %}

{% docs tpc_verdachten_van_drugsmisdrijven %}
The number of people suspected of drug offenses.
{% enddocs %}

{% docs tpc_verdachten_van_vuurwapenmisdrijven %}
The number of people suspected of firearm related crimes. 
{% enddocs %}

{% docs tpc_totaal_verdachten_van_misdrijven_p10k %}
The average number of people suspected of committing a crime per 10.000 inhabitants. 
{% enddocs %}

{% docs tpc_verdachten_van_vermogensmisdrijven_p10k %}
The average number people suspected of property crime per 10.000 inhabitants.
{% enddocs %}

{% docs tpc_verdachten_van_vernieling_opb_orde_p10k %}
The average number of people suspected of desctruction of public order per 10.000 inhabitants. 
{% enddocs %}

{% docs tpc_verdachten_van_geweldsmisdrijven_p10k %}
The average number of people suspected of violent crimes per 10.000 inhabitants. 
{% enddocs %}

{% docs tpc_verdachten_van_verkeersmisdrijven_p10k %}
The average number of people suspected of traffic offenses per 10.000 inhabitants. 
{% enddocs %}

{% docs tpc_verdachten_van_drugsmisdrijven_p10k %}
The average number of people suspected of drug offenses per 10.000 inhabitants.
{% enddocs %}

{% docs tpc_verdachten_van_vuurwapenmisdrijven_p10k %}
The average number of people suspected of firearm related crimes per 10.000 inhabitants. 
{% enddocs %}