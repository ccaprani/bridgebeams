# Expansion verification, 22 September 2026

## Latest visual-review follow-up

An additional 46 profiles are implemented: 16 W, 8 SD class 4, 10 Norway, 4 NZ hollow-core
and 8 Civilcon Y. The full suite passes **314 tests**, with 14 existing dependency
warnings. The isolated wheel contains **24 family JSON files**, and all 46 new
profiles construct outside the checkout. See the [follow-up record](visual-review-followup-2026-09.md)
for evidence, individual source discrepancies and the corrected review queue.
UK/Ireland are now separate coverage entries; the complete map/table separates
research records from implemented profiles. The checks below describe the
initial expansion and its then-current blockers, retained as history.

## Initial expansion

The regional registries contain **149 source records across 111 jurisdiction
codes and 530 dimension/property rows**. The separate PDF backlog adds 28
records and the Banagher transcription adds 48, for **606 recorded rows**.
Qatar, New Zealand and Norway extend the represented jurisdictions to
**114**; Japan's PDF audit overlaps the regional register.

These are research counts, not counts of exact profiles or independently
approved designs. They include partial dimensions, project examples,
historical publications, draft/preliminary drawings, access blockers and
explicitly rejected leads. Searches without usable results are documented
separately. The collection does not claim that the worldwide search is
exhaustive or that an unsuccessful search proves absence of a catalogue.

## Implementations and source corrections

Added **43 profiles**: 24 Banagher Solid Box, seven Mexican SEPSA, five
Taiwan Freeway Bureau, five Qatar Ashghal Q-girders and two NZTA I-beams.
The NZ Super-T also gains its narrower 1990 mm flange arrangement.

Two existing geometry errors were corrected: NZ Super-T previously filled
its open centre, and Civilcon I-beams were reflected vertically. The latter
was invisible to area and centroidal-inertia tests; source soffit widths,
direct centroids and actual top/bottom moduli now enforce orientation.

Qatar remains an explicitly documented reconstruction, with maximum source
residuals of 0.88% area, 0.85% centroid and 1.26% inertia. NZ Super-T omits
the unresolved formwork-ledge detail. Width-class-4 Solid Box, W, Norway and
NZ hollow-core geometry retain source-specific blockers. No interpolated
dimension is presented as a source transcription.

## Executed checks

| Check | Result |
|---|---|
| Full repository tests | 266 passed in 44.26 s; 14 existing Matplotlib/Pyparsing deprecation warnings |
| Isolated wheel | All 21 family JSON tables present; all 43 new profiles construct outside the checkout; Civilcon correction present |
| Regional source checker | 149 records parsed; 77 local PDF/HTML files hash-verified, including 52 PDFs whose page counts also match |
| Saved PDF backlog | Qatar/NZ/Norway/Japan hashes and page counts independently rechecked |
| Documentation | Sphinx HTML build with `-E -W` completed with zero warnings |
| Local documentation links | Research pages' local assets and JSON download targets exist |
| Profile figure | Example executed; SVG parsed and rendered image inspected at a common scale |
| Whitespace | `git diff --check` passed |

The interpreter used for package and documentation checks was
`/home/ccaprani/anaconda3/envs/pybridge/bin/python`. The repeatable source
check is `python3 tools/check_source_catalogue.py --verify-downloads`.
Downloads are private ignored working materials; a fresh clone can run the
checker without `--verify-downloads` to validate the versioned records.

## Independent review

Reviewers who did not author the relevant implementations or records checked
the source images and data. Checks included:

- NZ and Qatar dimension leaders, open-centre topology and published Qatar
  property fixtures; NZ I-beam upper/lower dimension stacks.
- Mexico's seven drawn profiles against published area, including explicit
  modified variants and last-digit rounding.
- Taiwan's Fig.10/Table14, post-tensioned terminology and end-block metadata.
- All 24 implemented Solid Box rows, with independent exact-fraction
  integration; the 32 SD and 16 W source-table transcriptions.
- All 30 Haitsma HIP/HRP property rows, 21 Somaco rows, seven Ferrobeton
  rows and selected VÁHOSTAV rows, including unit multipliers.
- WIKA bare/composite separation and property-unit conversions, ICC's
  complete nine-row table, and Civilcon source orientation.
- Draft/preliminary stamps and the rejected German source; translations and
  access limitations were kept separate from geometry readiness.

Review corrections were incorporated, including missing ICC rows, misleading
Civilcon work-status wording, stale report counts, integer conversion
artefacts, and documentation claims that incorrectly generalized the new
API and coordinate convention to the legacy Australian classes.

The original source documents retain their own copyright. The repository
contains factual tables, citations, translations of technical labels and
the resulting code, rather than copies of the publications.
