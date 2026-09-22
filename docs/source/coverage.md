# Country coverage

**Research coverage and implemented geometry are different counts.** This map colours countries by the number of fixed, source-backed profiles available in the library. The table also includes every jurisdiction in the research registries, including countries with no implemented geometry. Ireland and the United Kingdom are separate jurisdictions. Banagher profiles with documented availability in both appear in both country rows, with stable profile IDs; the global distinct-profile total counts each once.

The legend uses grey for places with no research record and no fixed section,
light blue for researched places with zero implemented sections, then deeper
colours for 1–5, 6–15, 16–40 and 41 or more sections. A few legacy families
have implemented sections without an entry in the recent research registries;
their section count determines their map colour.

[Open the map and complete table in a full window](_static/coverage/index.html).

```{raw} html
<iframe src="_static/coverage/index.html" title="Bridgebeams country coverage map and searchable complete country table" style="width:100%;height:1250px;border:1px solid #d1d5da;border-radius:8px" loading="lazy"></iframe>
```

Country counts include documented gross reconstructions and distinct named source variants available in each jurisdiction. Shared Banagher profiles count in both the UK and Ireland; the distinct global total deduplicates their profile IDs. Arbitrary continuous parameter choices, extrapolated Korean sizes, and incomplete Belgian/Greek templates requiring user-selected flange thicknesses are excluded. A profile count does not establish suitability for structural design. The map's **How the counts work** panel records specific counting choices.

The default table includes 123 catalogue jurisdictions: 122 with recent
research records plus Belgium, whose legacy template sits outside those
recent registries. Greece and Poland now have both geometry/templates and
new project or manufacturer research. The all-country
view also displays jurisdictions with no catalogue record.

Research-record counts include partial transcriptions, inaccessible documents and rejected leads. Multiple records can refer to the same publication. These counts are neither unique-document counts nor implemented profiles. Legacy implementation sources are listed separately in [Sources](sources.md); the recent collection work is in the [Research catalogue](research.md).

The September multilingual discovery search now includes Pakistan NHA Types A–H, the PCI AASHTO I–VI reference, and AASHTO-named leads in the Philippines, Honduras, Nicaragua, Guatemala, El Salvador and Peru. Honduras newly enters the recent research registry. The NHAI NH 45-A drawing supplies India's first fully dimensioned project midspan profile; its feasibility-report status is shown in the family documentation. Country details on the map show original source links, local-language titles, drawing locators and section names where available. A blocked lead's indexed terms are explicitly unverified.

The map, search, country details and source table work offline without external scripts or a map service. External source links need internet access. Small jurisdictions remain selectable in the complete table. Boundaries use [Natural Earth’s public-domain 1:50m country data](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/), simplified for display; they are a cartographic representation, not a catalogue claim about sovereignty.

Developers can regenerate the counts and page using `python tools/build_coverage.py` in the project environment. The generator reads current class size lists and the source registries; [download the generated coverage data](_static/coverage/coverage-data.json).
