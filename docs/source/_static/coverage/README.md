# Offline coverage assets

Run `python tools/build_coverage.py` from the project environment. This reads runtime family size lists and the two regional source JSON files, PDF-transcription sources and Banagher source records. The optional India follow-up is merged by `(country_code, id)`, updating an existing source rather than counting it twice. It writes `coverage-data.json` and `index.html`; the HTML embeds both its complete table and data, so no fetch or CDN is required. `coverage-template.html` is the editable interface source.

`boundaries.json` caches country outlines from Natural Earth 1:50m Admin 0 countries, fetched on 2026-09-22 from the upstream Natural Earth vector repository:

https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson

The file retains its upstream SHA-256, retrieval date and attribution. It has 242 features, simplified with Shapely's topology-preserving 0.075-degree tolerance and cached in equirectangular SVG coordinates (three pixels per degree). `tools/build_coverage.py` inverts those coordinates to longitude/latitude and draws the map in the equal-area Equal Earth projection (Šavrič, Patterson & Jenny, 2018), 1080 units wide. Labels and jurisdiction IDs use Natural Earth `NAME_EN` and `ISO_A2_EH`; features without an ISO-A2 code retain `ADM0_A3`. Antarctica is omitted from the displayed map, but remains in the all-country table. Small countries can be selected through the table.

Natural Earth data is public domain: https://www.naturalearthdata.com/about/terms-of-use/

Source information: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/

Natural Earth shows de facto administrative control; displaying these shapes does not establish a position on sovereignty. Research jurisdictions and producer attribution are independent of polygon classification. Ireland (IE) and the United Kingdom (GB) are intentionally distinct.
