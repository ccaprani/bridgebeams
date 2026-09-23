# Canadian sections: Ontario follow-up

The [Ontario Ministry of Transportation's current Structural Standard
Drawings](https://www.library.mto.gov.on.ca/SydneyPLUS/TechPubs/Portal/tp/ssdViews.aspx)
list **SS107-25, Prestressed Solid Slabs and Bearings (S300, S400, S500),
June 2025** and companion **SS107-26, Prestressed Solid Slabs Details**.
The listed drawings were downloaded through the portal on 22 September 2026;
the portal uses a form postback rather than stable per-drawing PDF links.
Locally retained source copies are in `sources/expansion/europe-americas/`
(gitignored; reference only). The [machine-readable follow-up](data/canada-followup.json)
records filenames and SHA-256 hashes.

SS107-25 shows a constant **1220 mm** width and three gross depths:
**300, 400, and 500 mm**. Its typical section shows **20 x 20 mm bottom
chamfers**; SS107-26 repeats the chamfer in the detail for extended and bent
strands outside the solid slab. These three source designations are implemented
as `CaMtoSolidSlabSection("S300" | "S400" | "S500")` in
`src/bridgebeams/ca/mto_solid_slab.py`. The coordinates are in millimetres,
soffit at y=0, and represent the uninterrupted gross section. Holes,
reinforcement, strands, end undercuts and bearing details are local features
and are excluded. The independent area check is `1220 * depth - 400` mm²;
the final 400 mm² removes two triangular chamfers. Widths at y=10 mm and
y≥20 mm are respectively 1200 and 1220 mm. There is no published section
property table on these two sheets for comparison.

These are **Ontario MTO** sections, not a single national Canadian standard.
The older 2023 NU drawing and accompanying design guidelines already in the
research catalogue bear **DRAFT**. The same official portal now lists June 2025
SS107-16 through SS107-23 for NU900 through NU2400 and SS107-24 for details.
SS107-16 (NU900) was downloaded and visually checked; its outline retains
R50 and R200 curved transitions and was not converted into a straight-sided
polygon. The catalogue's partial 2023 NU dimensions should be superseded with
the 2025 sheets before NU implementation or claims of current MTO approval.

> **Update 23 September 2026:** SS107-13 to SS107-24 (June 2025) are now
> downloaded and hash-recorded. NU900–NU2400 (eight depths) and the
> 1220 mm box girders are implemented from them; see the
> [Ontario extraction record](extraction-ontario-2026-09.md).

Further official Canadian drawing leads:

- [British Columbia, Volume 3 standard drawings](https://www2.gov.bc.ca/gov/content/transportation/transportation-infrastructure/engineering-standards-guidelines/structural/standards-procedures/volume-3), **D202 Standard Prestressed Concrete I Beams** (listing updated 25 March 2026). The PDF link needs a direct download and visual transcription.
- [Alberta, NU Girder Design and Detailing Manual](https://www.alberta.ca/nu-girder-design-and-detailing-manual) and [active precast girder drawing index](https://www.alberta.ca/system/files/custom_downloaded_images/trans-bridge-precast-girders-drawings.pdf), which lists NU typical drawings T-1750-18 through T-1753-18 and standard SL/SLW/SLC girder sheets. Source geometry remains to be read.
- [Manitoba, Water Management and Structures CADD standards](https://www.gov.mb.ca/mti/wms/structures/standards.html) includes prestressed channel girder bridge sheets. The inspected 12 m channel example is a project template with unresolved midspan inner-wall geometry; it was not added as a verified standard profile.
