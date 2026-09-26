# Sources

The expanded country-by-country source catalogue, English translations and
PDF transcriptions are available in {doc}`research`. These records are
versioned with the repository, including structured JSON evidence. Local
downloaded PDFs remain in the ignored `sources/` directory.

The first implemented Indian profile, `Nh45aPscISection`, comes from
[NHAI's NH 45-A Package II structural drawing pack](https://nhai.gov.in/nhai/sites/default/files/2020/PKG_II_Modified_Structural_drawings.pdf),
PDF p50, drawing `FIPL-HD-TPT-117-V-N-45A-MJB-CH-50+473-GA-01`, sheet 03/03
(November 2017). The midspan gross contour is fully dimensioned. The
title block says **Final Feasibility Report**; the library does not claim
that this profile was built or approved for construction.

The classic US AASHTO I-beam Types I–VI are transcribed from [PCI Bridge
Design Manual Appendix B-7/B-8](https://ems-www.pci.org/PCI_Docs/Design_Resources/Transportation_Resources/AASHTO%20I%20Beams.pdf)
(November 2011). The complete inch dimension table and rounded section
properties are checked in {doc}`pci-aashto-reference-2026-09`. This reference
does not establish that another jurisdiction uses an identical outline.

The original Irish section data are recovered from, or validated against,
published manufacturer documentation:

- **Banagher Precast Concrete**, *Bridge Beam Manual*, 3rd edition —
  <https://files.brintex.com/Occurrence/291/Brochure/7518/brochure.pdf>
  (M/UMB, MY/MYE, Solid Box, SY/SYE, T, TB, TY/TYE, U/SU, W, Y/YE: section
  properties, profile drawings, strand layouts, span tables).
- **Concast Precast Group** civil brochure —
  <http://concast.ie/wp-content/uploads/2020/03/Concast_Civil.pdf>
  (TY/TYE, Y/YE, M, U, CSU property tables; identical values for the
  common Irish ranges).
- "05316 Precast Beam Properties" spreadsheet (2007, C. Caprani /
  E. Stack) — property tables matching the above, with 50 embedded
  AutoCAD drawings of family profiles and strand grids.

The Banagher manual includes dimensioned vector drawings and property tables.
Some profiles were recovered directly from the drawings; others use
documented reconstructions fitted to published properties. The new Solid Box
profiles follow explicit drawing dimensions. See {doc}`families` for each
family's method and validation limits.

Manufacturer brochures are copyrighted; they are held as private working
references (not committed). Dimensional data of standard sections are
facts; this library cites the source manual and family page for each
encoded family. Full registry with access dates:
`sources/SOURCES.md` in the repository working tree.
