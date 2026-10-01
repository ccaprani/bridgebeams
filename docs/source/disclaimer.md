# Disclaimer

`bridgebeams` is **not an authoritative source** of bridge-beam geometry. It
collects public information from national and state standards, producer
catalogues, project and feasibility drawings, theses and papers, in many
languages and editions. The authors have tried to transcribe it faithfully.
Many profiles still required judgement:

| `provenance` | Meaning |
|---|---|
| `transcribed` | Every coded dimension was read from the cited drawing or table. |
| `transcribed-with-convention` | Read from the source, plus a stated convention for an undimensioned fillet, chamfer or similar detail. |
| `fitted-reconstruction` | Undimensioned details were fitted to published section properties. |
| `estimate` | A best estimate from an incomplete, schematic or low-resolution source. Treat it as indicative only. |

`source_status` records the status of the source itself, for example current
standard, DRAFT, PRELIMINARY, Final Feasibility Report, historic standard
or producer catalogue. A current source can still be superseded without notice.
Families implemented before September 2026 predate these attributes; see
their module documentation and {doc}`research`.

Some sources contradict themselves. Where that happens, the tests pin the
discrepancy instead of hiding it; the research records list each one.
Nothing here certifies structural adequacy, manufacturability or current
availability. Verify dimensions against the governing document before any
design, assessment or procurement use. The software is provided under the
MIT licence without warranty of any kind.
