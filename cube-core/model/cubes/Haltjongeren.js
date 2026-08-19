cube(`Haltjongeren`, {
  sql: `SELECT * FROM pocca.mrt_cbs_haltjongeren`,
  
  dimensions: {
    haltjongeren_record: {
      sql: `haltjongeren_record`,
      type: `string`,
      title: `Haltjongeren Record`,
      description: `Unieke primary key voor elke rij in een tabel.`
    },

    jaar: {
      sql: `jaar`,
      type: `time`,
      title: `Jaar`,
      description: `Het kalenderjaar van waarneming (bijvoorbeeld 2023).`
    },

    delictgroep: {
      sql: `delictgroep`,
      type: `string`,
      title: `Delictgroep`,
      description: `Categoraal veld: het type delict zoals geregistreerd door de politie en geclassificeerd volgens CBS-standaard. hoofdgroepen: geweldsmisdrijven (mishandeling, bedreiging, seksuele misdrijven), vermogensmisdrijven (diefstal, inbraak, winkeldiefstal), vernieling en openbare orde (vernieling, brandstichting, openlijke geweldpleging), verkeersmisdrijven, drugsmisdrijven, vuurwapenmisdrijven, en overtredingen (baldadigheid, leerplichtwet). Bron: CBS StatLine 81947NED [web:21].`
    },

    geslacht: {
      sql: `geslacht`,
      type: `string`,
      title: `Geslacht`,
      description: `Het geslacht van de persoon: man, vrouw, onbekend of totaal.`
    },

    leeftijd: {
      sql: `leeftijd`,
      type: `string`,
      title: `Leeftijd`,
      description: `De leeftijd zoals gespecificeerd door het CBS (bijvoorbeeld "12 jaar" of "12 tot 17 jaar").`
    },

    leeftijd_int: {
      sql: `leeftijd_int`,
      type: `string`,
      title: `Leeftijd Int`,
      description: `De leeftijd als geheel getal (integer) voor rekenoperaties.`
    },

    leeftijd_groep: {
      sql: `leeftijd_groep`,
      type: `string`,
      title: `Leeftijd Groep`,
      description: `De leeftijd ingedeeld in groepen (bijvoorbeeld "12-17", "65+")`
    },

    opleiding: {
      sql: `opleiding`,
      type: `string`,
      title: `Opleiding`,
      description: `Het betreft hier de hoogst gevolgde opleiding van de persoon in het desbetreffende jaar. Ze hoeven deze opleiding niet met een diploma of overgangsbewijs te hebben afgerond.`
    },

    type_delict: {
      sql: `type_delict`,
      type: `string`,
      title: `Type Delict`,
      description: `Categorieveld voor de juridische classificatie van een delict. De waarde geeft aan of een registratie hoort bij een misdrijf, een overtreding of een overige categorie. Dit veld is bedoeld voor analyse, filtering en aggregatie in conversaties met data.`
    }
  },
  
  measures: {
    haltjongeren_sum: {
      type: `sum`,
      sql: `haltjongeren`,
      title: `Haltjongeren Sum`,
      description: `Het totaal aantal Halt-jongeren dat is verwezen naar Halt voor het plegen van een strafbaar feit. Het betreft hier zowel overtredingen als misdrijven.
Cijfers worden afgerond op tientallen, hierdoor komt het totaal soms niet overeen met de som der delen.`
    },

    haltjongeren_relatief_sum: {
      type: `sum`,
      sql: `haltjongeren_relatief`,
      title: `Haltjongeren Relatief Sum`,
      description: `Het aantal Halt-jongeren per 10 000 inwoners uit de geselecteerde bevolkingsgroep dat is verwezen naar Halt voor het plegen van een strafbaar feit. Het betreft hier zowel overtredingen als misdrijven.`
    },

    misdrijf_vs_overtreding_ratio: {
      type: `number`,
      sql: `${totaal_misdrijf} / NULLIF(${totaal_overtreding}, 0)`,
      title: `Misdrijf/Overtreding Ratio`,
      description: `De ratio van het aantal misdrijven over het aantal overtredingen. `
    },

    totaal_overtreding: {
      type: `sum`,
      sql: `haltjongeren`,
      title: `Totaal overtreding`,
      description: `Het totaal aantal jongeren dat naar Halt is gestuurd vanwege het begaan van een overtreding.`
    },

    totaal_misdrijf: {
      type: `sum`,
      sql: `haltjongeren`,
      title: `Totaal misdrijf`,
      description: `Het totaal aantal jongeren dat naar Halt is gestuurd vanwege het plegen van een misdrijf.`
    },

    totaal_haltjongeren: {
      type: `sum`,
      sql: `haltjongeren`,
      title: `Totaal Halt-jongeren`,
      description: `Het totaal aantal jongeren dat is doorverwezen naar Halt.`
    }
  }
});
