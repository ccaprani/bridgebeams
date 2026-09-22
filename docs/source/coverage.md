# Country coverage

**Research coverage and implemented geometry are different counts.** This map colours countries by the number of fixed, source-backed profiles available in the library. The table also includes every jurisdiction in the research registries, including countries with no implemented geometry. Ireland and the United Kingdom are separate: Irish producer sections are counted under Ireland; the UK namespace currently has zero profiles.

[Open the map and complete table in a full window](_static/coverage/index.html).

```{raw} html
<iframe src="_static/coverage/index.html" title="Bridgebeams country coverage map and searchable complete country table" style="width:100%;height:1250px;border:1px solid #cbd7df;border-radius:8px" loading="lazy"></iframe>
```

The count includes documented gross reconstructions and distinct named source variants. It excludes namespace aliases, arbitrary continuous parameter choices, extrapolated Korean sizes, and incomplete Belgian/Greek templates requiring user-selected flange thicknesses. A profile count does not establish suitability for structural design. The map's **How the counts work** panel records specific counting choices.

The default table includes 117 catalogue jurisdictions: 114 with recent
research records plus Belgium, Greece and Poland, whose legacy
implementations/templates sit outside those recent registries. The all-country
view also displays jurisdictions with no catalogue record.

Research-record counts include partial transcriptions, inaccessible documents and rejected leads. Multiple records can refer to the same publication. These counts are neither unique-document counts nor implemented profiles. Legacy implementation sources are listed separately in [Sources](sources.md); the recent collection work is in the [Research catalogue](research.md).

The map, search, country details and source table work offline without external scripts or a map service. External source links need internet access. Small jurisdictions remain selectable in the complete table. Boundaries use [Natural Earth’s public-domain 1:50m country data](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/), simplified for display; they are a cartographic representation, not a catalogue claim about sovereignty.

Developers can regenerate the counts and page using `python tools/build_coverage.py` in the project environment. The generator reads current class size lists and the source registries; [download the generated coverage data](_static/coverage/coverage-data.json).
