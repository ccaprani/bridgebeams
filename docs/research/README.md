# Global precast bridge beam source collection

The [visual-review follow-up](visual-review-followup-2026-09.md) records the
received readings, recovered CAD and 46 additional implemented profiles.
The [India follow-up](india-followup.md) adds primary sources and updates
the RDSO access result. The Sphinx [coverage page](../source/coverage.md) provides the complete
country list and map, separating source counts from implemented profiles.
The [Ontario follow-up](canada-followup.md) records current MTO solid-slab drawings
and three profiles. The [US state follow-up](us-states-followup.md) records ten
state DOT source leads and three Minnesota profiles; Washington W-series
profiles are also implemented from official drawings.

This directory is the versioned research record for expanding `bridgebeams`.
The regional reports preserve original source titles alongside English
translations, links, dimension transcriptions, and remaining uncertainties.
The accompanying JSON files retain structured source records. Downloaded
publications and rendered page images remain in the ignored `sources/`
directory; their availability does not determine whether the research itself
is retained in Git.

See the [country index](#country-index) and the
[verification record](verification-2026-09.md) for coverage, implemented
profiles and completed checks.

## Research batches

| Coverage | Report | Structured evidence |
|---|---|---|
| Europe and the Americas | [Sources and translations](europe-americas-2026-09.md) | [Source records](data/europe-americas-sources.json) |
| Asia, Middle East and Africa | [Sources and translations](asia-africa-2026-09.md) | [Source records](data/asia-africa-sources.json) |
| Central Europe: manufacturers and technical catalogues | [Named-section deep search](deep-search-central-europe-2026-09.md) | [12 source leads](data/deep-search-central-europe-2026-09.json) |
| Romance-language regions: producers, guides and theses | [Named-section deep search](deep-search-romance-2026-09.md) | [10 source leads](data/deep-search-romance-2026-09.json) |
| Asia, Africa and Middle East: standard drawings and academic work | [Named-section deep search](deep-search-asia-africa-2026-09.md) | [9 source leads](data/deep-search-asia-africa-2026-09.json) |
| Greece: two dimensioned project proposals | [Project-girder search](deep-search-new-europe-2026-09.md) | [2 source leads](data/deep-search-new-europe-2026-09.json) |
| Puerto Rico, Bhutan, Jamaica, Hong Kong and Mauritius | [Project and jurisdiction search](deep-search-new-regions-2026-09.md) | [5 source leads](data/deep-search-new-regions-2026-09.json) |
| Existing PDF backlog: Qatar, New Zealand, Norway and Japan | [Visual transcription and corrections](pdf-transcription-2026-09.md) | [Transcriptions](data/pdf-transcriptions.json) |
| Existing Banagher manual: Solid Box and W families | [Tables and geometry audit](banagher-pending-families-2026-09.md) | [Transcriptions](data/banagher-pending-families.json) |
| Canada: Ontario MTO current drawings | [Source and geometry follow-up](canada-followup.md) | [Drawing record](data/canada-followup.json) |
| United States: ten state DOTs | [State source follow-up](us-states-followup.md) | [State records](data/us-states-followup.json) |
| Washington W-series | [Drawing and property audit](us-washington-followup.md) | [Source hashes and checks](data/us-washington-followup.json) |
| United States: PCI AASHTO I-beam Types I–VI | [Dimensioned reference and property checks](pci-aashto-reference-2026-09.md) | [Source record](data/deep-search-us-aashto-2026-09.json) |
| Pakistan: NHA PSC I-girder Types A–H | [Design-code and geometry follow-up](pakistan-us-section-followup-2026-09.md) | [Three source leads](data/deep-search-pakistan-2026-09.json) |
| AASHTO-named beams outside the US | [Cross-jurisdiction follow-up](aashto-cross-jurisdiction-followup-2026-09.md) | [Seven source leads](data/deep-search-aashto-global-2026-09.json) |

## Reading the evidence

A source can establish that a manufacturer supplies bridge beams without
specifying the cross-section. A table of overall depths and widths is useful
catalogue data, but it is not enough to construct an exact polygon. A
dimensioned section drawing, with all necessary thicknesses and haunches,
provides stronger evidence. Independently published area, centroid and second
moment of area allow the resulting geometry to be checked.

Keep these distinctions when reusing the records:

- **Verified source:** the linked page or document was inspected; its
  statements are limited to what was actually visible.
- **Transcribed dimensions:** numeric facts read from a specified drawing or
  table, with the original units and page locator retained.
- **Lead or access blocker:** a potentially useful source requiring further
  retrieval or checking. A search result is not a substitute for its drawing.
- **Implemented geometry:** a separate package feature, with tests and stated
  approximation limits. Source discovery alone does not establish this status.

Search coverage is dated and bounded. An unsuccessful search does not show
that a national catalogue does not exist. National standards, highway-agency
drawings, regional practices and producer ranges are all useful; they should
not be described as interchangeable.

## Translation and units

The reports translate technical titles, labels and factual tables rather
than reproducing entire publications. Original beam designations are kept:
similar names in different countries do not establish identical geometry.
In particular, *prestressed* alone does not mean *pretensioned*;
post-tensioned and conventionally reinforced precast beams are distinguished
where the source does so.

Source units are retained in the research data. Implementations use
millimetres, square millimetres and fourth powers of millimetres. A centroid
measured down from the top must be converted before comparing with the
new families' soffit-based coordinates; legacy Australian classes retain
their earlier coordinate convention. Published centroidal inertia must not be
compared with inertia about the soffit.

## Reproducibility and copyright

Use the original URL, publication/drawing identifier, page locator and file
hash recorded in each batch to recover the evidence. Download paths are local
working references and need not exist in a fresh clone. Source publications
retain their own copyright; inclusion of their factual dimensions or a link
does not relicense their drawings under this repository's MIT licence.

## Checking and refreshing the regional index

Run `python3 tools/check_source_catalogue.py` from the repository to validate
the two regional registries. `--verify-downloads` additionally checks local
PDF and HTML hashes and uses `pdfinfo` to check PDF page counts; it requires
the ignored downloads to be present. `--write-index` refreshes the generated
country table below. The separate PDF-backlog and Banagher transcriptions
retain their own source manifests and are not included in these regional
row counts.

Run `python3 tools/check_discovery_sources.py` to validate the eight newer
discovery queues. Their 49 records are searchable on the coverage map;
the historical country index below remains the original regional-batch index,
so its 149-record total should not be mistaken for the complete map total.

<!-- country-index:start -->
## Country index

149 source records across 111 country/jurisdiction codes. Counts include access blockers and rejected leads; they are not counts of implemented or verified beam families. Dimension rows include partial dimension and property tables.

| Country / jurisdiction | Source records | Dimension / property rows | Report |
|---|---:|---:|---|
| Algeria (DZ) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Angola (AO) | 2 | 2 | [asia-africa](asia-africa-2026-09.md) |
| Argentina (AR) | 1 | 2 | [europe-americas](europe-americas-2026-09.md) |
| Armenia (AM) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Australia (AU) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Austria (AT) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Bahrain (BH) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Bangladesh (BD) | 1 | 5 | [asia-africa](asia-africa-2026-09.md) |
| Belarus (BY) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Belize (BZ) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Bosnia and Herzegovina (BA) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Botswana (BW) | 1 | 1 | [asia-africa](asia-africa-2026-09.md) |
| Brazil (BR) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Brunei (BN) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Bulgaria (BG) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Cambodia (KH) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Cameroon (CM) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Canada (CA) | 2 | 8 | [europe-americas](europe-americas-2026-09.md) |
| Chile (CL) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| China (CN) | 2 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Colombia (CO) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Costa Rica (CR) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Croatia (HR) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Czechia (CZ) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Côte d’Ivoire (CI) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Denmark (DK) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Dominican Republic (DO) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Ecuador (EC) | 2 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Egypt (EG) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| El Salvador (SV) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Estonia (EE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Ethiopia (ET) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Fiji (FJ) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Finland (FI) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| France (FR) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Georgia (GE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Germany (DE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Ghana (GH) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Guatemala (GT) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Guinea (GN) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Guyana (GY) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Haiti (HT) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Hungary (HU) | 4 | 12 | [europe-americas](europe-americas-2026-09.md) |
| India (IN) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Indonesia (ID) | 3 | 27 | [asia-africa](asia-africa-2026-09.md) |
| Iran (IR) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Iraq (IQ) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Ireland (IE) | 2 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Israel (IL) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Italy (IT) | 4 | 34 | [europe-americas](europe-americas-2026-09.md) |
| Japan (JP) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Jordan (JO) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Kazakhstan (KZ) | 2 | 9 | [europe-americas](europe-americas-2026-09.md) |
| Kenya (KE) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Kuwait (KW) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Kyrgyzstan (KG) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Laos (LA) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Latvia (LV) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Lebanon (LB) | 1 | 1 | [asia-africa](asia-africa-2026-09.md) |
| Malaysia (MY) | 2 | 3 | [asia-africa](asia-africa-2026-09.md) |
| Maldives (MV) | 1 | 1 | [asia-africa](asia-africa-2026-09.md) |
| Mexico (MX) | 2 | 123 | [europe-americas](europe-americas-2026-09.md) |
| Moldova (MD) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Mongolia (MN) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Montenegro (ME) | 1 | 1 | [europe-americas](europe-americas-2026-09.md) |
| Morocco (MA) | 1 | 4 | [asia-africa](asia-africa-2026-09.md) |
| Myanmar (MM) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Nepal (NP) | 3 | 2 | [asia-africa](asia-africa-2026-09.md) |
| Netherlands (NL) | 2 | 50 | [europe-americas](europe-americas-2026-09.md) |
| Nicaragua (NI) | 1 | 13 | [europe-americas](europe-americas-2026-09.md) |
| Nigeria (NG) | 2 | 1 | [asia-africa](asia-africa-2026-09.md) |
| North Macedonia (MK) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Oman (OM) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Pakistan (PK) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Panama (PA) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Papua New Guinea (PG) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Paraguay (PY) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Peru (PE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Philippines (PH) | 2 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Portugal (PT) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Romania (RO) | 2 | 21 | [europe-americas](europe-americas-2026-09.md) |
| Russia (RU) | 1 | 46 | [europe-americas](europe-americas-2026-09.md) |
| Saudi Arabia (SA) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Senegal (SN) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Serbia (RS) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Singapore (SG) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Slovakia (SK) | 2 | 20 | [europe-americas](europe-americas-2026-09.md) |
| South Africa (ZA) | 7 | 58 | [asia-africa](asia-africa-2026-09.md) |
| South Korea (KR) | 1 | 6 | [asia-africa](asia-africa-2026-09.md) |
| Spain (ES) | 2 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Sri Lanka (LK) | 3 | 9 | [asia-africa](asia-africa-2026-09.md) |
| Sudan (SD) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Suriname (SR) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Sweden (SE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Switzerland (CH) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Taiwan (TW) | 1 | 5 | [asia-africa](asia-africa-2026-09.md) |
| Tanzania (TZ) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Thailand (TH) | 1 | 7 | [asia-africa](asia-africa-2026-09.md) |
| Trinidad and Tobago (TT) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Tunisia (TN) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Türkiye (TR) | 2 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Uganda (UG) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| Ukraine (UA) | 2 | 0 | [europe-americas](europe-americas-2026-09.md) |
| United Arab Emirates (AE) | 1 | 0 | [asia-africa](asia-africa-2026-09.md) |
| United Kingdom (GB) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| United States (US) | 3 | 48 | [europe-americas](europe-americas-2026-09.md) |
| Uruguay (UY) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Uzbekistan (UZ) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Venezuela (VE) | 1 | 0 | [europe-americas](europe-americas-2026-09.md) |
| Vietnam (VN) | 2 | 4 | [asia-africa](asia-africa-2026-09.md) |
| Zimbabwe (ZW) | 2 | 0 | [asia-africa](asia-africa-2026-09.md) |

Qatar, New Zealand, Norway and Japan also have a separate [PDF backlog audit](pdf-transcription-2026-09.md). Its drawing transcriptions are additional to the regional counts above.
<!-- country-index:end -->
