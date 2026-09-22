# India source follow-up

Checked 2026-09-22. India was already present in the regional source register as `IN-RDSO-BS141`, but had no implemented constructor. It should appear on a research-coverage map even while geometry remains incomplete. This follow-up provides **five primary-source records: one update to that existing record and four additional records**. Do not count the repeated BS-141 entry twice. Structured evidence is in [india-followup.json](data/india-followup.json).

## Downloaded project drawings: NHAI precast PSC I girder

The [NHAI Delhi–Vadodara Expressway package II, Volume III drawings](https://nhai.gov.in/nhai/sites/default/files/Agreements_document/pkg2-VOL-III.pdf) downloaded successfully. The cover identifies the Sohna–Firozpur Jhirka section, km 18+500 to 47+000, Haryana, July 2019. It is a **project source**, not a national profile catalogue.

- PDF page 39 / printed 38 identifies a 1 × 30.0 m PSC I-beam crossing at km 37+744.
- PDF page 41 / printed 40 explicitly labels precast PSC girder sections at support and midspan. Both top widths read **1100 mm**; the support stem/base width reads **750 mm**.
- The midspan is an I profile and the support region is thickened. The retained raster scan is degraded: web/depth/haunch digits are not promoted without a clearer source. The main elevation appears to label 2225 mm for the girder, but that remains an unverified reading rather than a public dimension.
- PDF page 6 labels a different RCC girder **cast in situ**. It is excluded from the precast section collection; a document containing both systems must not be classified wholesale as precast.

Local source: `sources/expansion/india-followup/nhai-project.pdf`, 196 pages, 2,976,865 bytes. SHA-256: `828db4e970519efa152ae40f8326f235d7fccfea775869d8e81ce68fb2a9cc0f`. Retained renders: `nhai-p39.png`, `nhai-p40.png`, `nhai-p41.png`, and focused `nhai-p41-section.png` in the same directory. The PDF has no useful text layer; targeted OCR located the relevant sheets, and the dimensions above were checked visually.

## MoRTH standard precast RCC girders, 32 m

The primary [January 2025 MoRTH 32 m, zero-skew standard drawing set](https://www.morth.gov.in/sites/default/files/comprehensive_compendium_circular/1910.6-%2032m%20span%20with%200%20skew%20Bridge%20Drawing.pdf) is indexed with drawing `MORTH/LSM/32m/13.0m/00/1001`, a 32 m span and 13 m deck width. Its indexed text explicitly says **PRECAST RCC GIRDER**, with cast-in-situ deck slab, and references separate inner/outer girder sheets `1007` and `1003`. General notes describe yard casting, lifting, transport and erection.

This is a useful new **reinforced-concrete precast** standard source, not a prestressed profile. The current `morth.nic.in` link redirects to HTML instead of the PDF in the local client; `www.morth.gov.in` produced a TLS error locally and a timeout through the web reader. Search-index text is readable, but no complete local PDF or exact outline has been obtained. Do not infer cross-section dimensions from flattened indexed drawing text.

## RDSO BS-141: access is partial, not wholly blocked

The [official March 2025 BS-141](https://rdso.indianrailways.gov.in/uploads/BS-141.pdf) is titled *Guidelines for Quality Control, Erection, Inspection & Maintenance of PSC Girders*. Its table of contents identifies Annexure XXIII, the standard PSC drawing list, starting at printed page 82. The web reader opened the 106-page document and returned readable text; later page requests timed out. Local requests still fail with connection refused.

Update the earlier blanket `access-blocked` classification to **web-readable; local download blocked**. The existing 2I/4I/U/box family leads remain leads to the drawing list; no height from that table has been newly verified or promoted here. A guideline/index does not itself supply an exact beam polygon.

## Two railway sources giving precise drawing leads

The [IRICEN accelerated bridge construction presentation](https://www.iricen.gov.in/iricen/ipwe_seminar/2017/2024%20Session-I/IPWE%20Nov%2023%20Vol-I%20Paper%207.pdf), slide 15, explicitly discusses prefabricated railway superstructures and lists PSC slabs for 3.05, 4.57, 6.1, 9.15 and 12.2 m spans, and PSC girders for 12.2, 18.3 and 24.4 m spans. These are **span designations, not section depths**. The official text is search-index readable; local download timed out.

The [November 2021 IRICEN Journal](https://iricen.gov.in/iricen/journals/Nov-2021.pdf), printed page 39, names **RDSO-B/10273**, an 18.4 m PSC I-girder deck for 25 t loading, as the analysis model. Preserve its printed 18.4 m designation; do not silently normalise it to the 18.3 m family label elsewhere. This provides a precise drawing-retrieval target, not a verified profile. Local download timed out; only the official indexed text was inspected.

## Next concrete work

Retrieve a higher-resolution NHAI girder sheet or its original drawing; recover MoRTH sheets 1003/1007 through a functioning publication link; obtain the RDSO-B/10273 drawing and BS-141 Annexure XXIII. Existing source coverage now includes an actually downloaded precast project section, a national RCC drawing-set lead and railway slab/I/U/box leads. It does not yet establish an implemented Indian beam family.
