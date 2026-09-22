# Global bridge beams

`bridgebeams` has two related collections: implemented section geometry and
sources for additional families. They have different evidence requirements.
The [research catalogue](research.md) records original titles, English
translations, dimensions, source URLs and remaining blockers from the
September 2026 international search.

![Representative new and corrected beam profiles at a common scale](_static/images/global-additions.svg)

## Implemented families

| Jurisdiction | Module | Families | Evidence limits |
|---|---|---|---|
| Australia | `bridgebeams.aus` | Super-T T1–T5; I-girders 1–4 | AS5100.5 Appendix D; historical variants retained |
| Ireland / UK practice | `bridgebeams.ie` | T, TY/TYE, Y/YE, U/SU, M/UMB, SY/SYE, MY/MYE, Solid Box | Exact and reconstructed families; Solid Box width classes 1–3 validated against published properties |
| Belgium | `bridgebeams.be` | FEBE standardised I-beams | Flange thicknesses must be supplied by the designer |
| Greece | `bridgebeams.gr` | Egnatia extended-I families | Published depth law/widths; flange thicknesses are design inputs |
| Japan | `bridgebeams.jp` | JIS/PCCEN AG/BG T-girders | Chubu drawing metadata; additional drawing audit is in the PDF report |
| Korea | `bridgebeams.kr` | KHC PSC I-girders | Published 25/30/35 m data; 20/40 m sizes are extrapolated |
| Mexico | `bridgebeams.mx` | SEPSA I-MODIFIED, II, III, IV, IV-MODIFIED, V, VI | Producer-specific metric profiles; published areas match within 50 mm² rounding |
| New Zealand | `bridgebeams.nz` | RR364 Super-T; 1500/1600 mm I-beams | Super-T is a corrected gross-profile approximation; I-beams use dimensioned outlines |
| Poland | `bridgebeams.pl` | Mosty-Łódź T12–T27 | Family-specific dimension/provenance metadata |
| Qatar | `bridgebeams.qa` | Ashghal Q-girders T1–T5 | Documented reconstruction; maximum A/centroid/Ixx deviations 0.88%/0.85%/1.26% |
| Russia | `bridgebeams.ru` | 3.503.1-81, 33 m I-beams | Fitted flange profile validated against producer volumes |
| South Africa | `bridgebeams.za` | Civilcon I1–I20 | Published producer dimensions |
| Taiwan | `bridgebeams.tw` | Freeway Bureau Types IV–VIII | Dimensioned post-tensioned gross midspan profiles; analytically checked |
| Thailand | `bridgebeams.th` | DOH IG-205 | Published 20 m standard drawing |
| Türkiye | `bridgebeams.tr` | KGM-lineage I90/I120/I140/I170 | Worked-example profile assumptions; project drawing confirmation needed |

The `bridgebeams.uk` namespace remains a planned separate historical UK
catalogue. Shared British ancestry does not establish that all national or
producer variants have identical dimensions.

## Expanded source collection

See {doc}`research` for the complete regional reports and downloadable JSON:

- {doc}`research-europe-americas`: highway-agency standards, national
  catalogues and producer families across Europe and the Americas.
- {doc}`research-asia-africa`: Asia, Middle East and African sources, with
  English translations and explicit access limits.
- {doc}`research-pdf-transcription`: direct checks of the Qatar, New Zealand,
  Norway and Japan drawing backlog, including corrections to older notes.

The source records distinguish inspected documents from search leads and
unavailable downloads. Overall depths and widths alone do not define an
exact section. Some publications give independently tabulated area, centroid
and inertia; others still need internal haunch/flange dimensions.

## How to use the collection

Select a family by the original designation and source revision. Read its
accuracy statement before calculating section properties. For a researched
family that is not implemented, use the page-specific transcription and
original source to establish all necessary dimensions, then validate the
resulting polygon against independent published properties where available.

The new and audited families use millimetres and a soffit-based vertical
coordinate. Legacy Australian classes retain their existing negative-y
coordinate convention and older interface; check the family API. Research
records retain source units; centroid direction and inertia units must be
converted explicitly. Source publications remain copyrighted and are kept
as ignored local working materials. Their factual dimensions and provenance
are retained in versioned records.
