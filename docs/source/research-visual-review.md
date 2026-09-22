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
