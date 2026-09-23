# Visual review: responses incorporated

Colin's 12 responses, exported on 22 September 2026 at 11:24 UTC, are now
preserved in the repository. The illustrated page archives the answered
questions, displays each original response and records its follow-up.
No repeat description of the NZ inner/edge drawings is requested.

```{only} local_review
<p><a href="dims_review.html"><strong>Open the illustrated review and received answers</strong></a></p>
```

See {doc}`visual-review-followup-2026-09` for implementations, dimensional
interpretations and remaining source limitations. The detailed checks are
in {doc}`visual-followup-norway-nz`, {doc}`banagher-cad-followup`
and {doc}`visual-followup-za-ro-nepal`.

Download the {download}`verbatim received responses
<../research/data/visual-review-responses-2026-09-22.json>`.
Printed callouts, visually inferred dimensions and approximate suggestions
retain distinct provenance. In particular, the Norwegian 15 mm bottom
chamfer is a reviewer interpretation; the proposed Civilcon M notch and
UK equivalence are not treated as manufacturer-certified facts.

## Round 3 queue (23 September 2026)

The illustrated page now opens with a new queue of 15 cards covering the
two extraction rounds. The 12 answered round-2 cards are archived below it.

- **Source contradictions (1–9).** Civilcon M edge inset (fitted 15 mm vs
  printed 10 mm), VPH 2010-R2 2.1 m, WSDOT G6 fillet run and W*BTG +4 in²,
  SEPSA box tables, Spanbeton ZIPXL/PIQ/SRP, Pakistan NHA A–H, Ferrobeton
  FPT-45 and FPT-70/50, and DNIT PCP-10.
- **Visual readings (10–12).** NHAI Delhi–Vadodara web width, ASA 52 stem
  and 105 lower slope, and the Thai DOH IG20 web and splay.
- **Estimate gallery (13).** One outline per family with `estimate`
  profiles, each marked plausible, wrong shape or can't tell.
- **Policy (14).** Counting width matrices, shared sections and identical
  producer geometry, and whether estimates count in the headline.
- **Manual retrieval (15).** Blocked sources to download by hand into
  `sources/expansion/round2/manual/<cc>/`.

Each contradiction or reading card places a source crop beside the
implemented outline and states the question. It offers concrete options, a
note field and a status (not reviewed, answered or skip). The toolbar
counts progress. Answers save under a new browser-storage prefix
(`bbdims5_`); archived clarifications keep `bbdims4_`. **Copy answers**
or **Download answers** exports "BRIDGEBEAMS REVIEW v5 — ROUND 3",
round-3 answers first, then any archived clarifications. Paste that text
into the conversation. Review images are in the ignored
`sources/review-2026-09-23/`.

## Review-page behaviour

Each answered card is collapsed by default. Open it to see the received
answer and outcome, then expand the original source images if needed.
The old broad NZ comparison requests and Nepal chamfer-scope question are
archived, rather than presented again as current tasks.

Optional new clarifications use separate browser storage (`bbdims4_`).
The received v3 answers remain visible as recorded evidence. Earlier local
v2/v3 drafts can be exported with **Export earlier answers**. Copy or download
new notes before changing server address or port: browser storage belongs
to the current origin.

## Build and serve locally

From the repository root, using an environment with the documentation
dependencies installed:

```bash
python tools/build_local_docs.py --with-review
python -m http.server 8766 --bind 127.0.0.1 --directory docs/_build/html
```

Open <http://localhost:8766/research-visual-review.html> for this guide or
<http://localhost:8766/dims_review.html> for the illustrated archive.
The helper copies the ignored review page and links the ignored `sources/`
directory into the local output. The source publications and drawings stay
local. A normal `python tools/build_local_docs.py` build omits the review
link and removes those local attachments from the output.
