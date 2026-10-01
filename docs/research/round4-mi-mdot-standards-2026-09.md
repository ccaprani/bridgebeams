# Round 4: MDOT standard prestressed beams (2026-09)

Closing the Michigan lead list from round 3. The Wayback-captured
`mi-wayback` folder held no beam geometry, but its Index to Bridge Detail
Sheets named the MDOT special-detail sheets (PC series). With the owner
VPN'd to US egress, the current revisions (plan dates 12-22-2025) and the
complete Bridge Design Guides (BDG) set were downloaded live from
`mdotjboss.state.mi.us` (Cloudflare blocks non-US IPs; curl with a US
egress works). 13 profiles implemented in
`us/state_r4_mi_mdot_standard.py`; 199 tests pass. Machine-readable
record: `docs/research/data/round4-mi-mdot-standards-2026-09.json`.

## Sources

| Source | Local path | SHA-256 (first 12) | Outcome |
|---|---|---|---|
| PC-1Q Prestressed Concrete I-Beam Details (12-22-2025), 2 pp | sources/expansion/round3/mi-wayback/redownloaded/live-2026/PC-1Q_a.pdf | 12bdae9fbfa3 | 4 profiles |
| PC-2L 70 in I-Beam Details (12-22-2025), 2 pp | …/live-2026/PC-2L.pdf | bd50afeae3a4 | 1 profile |
| PC-4J 1800 Beam Details (12-22-2025), 2 pp | …/live-2026/PC-4J.pdf | 315a625b55da | 1 profile |
| PC-5D Bulb-Tee Beam Details (12-22-2025), 2 pp | …/live-2026/PC-5D.pdf | 6b8064ebbf27 | 7 profiles |
| BDG English complete set (232 pp) incl. 6.60.01/.02/.03 | …/live-2026/BDG-complete-set.pdf | 41a5a153fbef | Property tables |

Mirror of all source PDFs: `~/Downloads/bridgebeams-manual/us/mi/` (the
non-repo local source store). Wayback 2022 revisions (PC-1N/2I/4G/5A) are
kept alongside for provenance; see
`sources/expansion/round3/mi-wayback/redownloaded/README-recovery-status.md`
for the full recovery story, including the MI 1800 lead closure.

## Implemented families (`us/state_r4_mi_mdot_standard.py`)

### `MiMdotISection` — PC-1Q Types I–IV, 4 profiles, `transcribed`

Section B-B (midspan) chains sum exactly per type. The Type I chain
prints four values (3¾ + 11 + 5 + 5 = 24¾ of 28 in); the missing segment
is the 3¼ in top-flange taper, pinned by the printed BDG 6.60.01 BEAM
PROPERTIES. Model residuals against the printed table (fillets omitted):

| Type | A model/printed | St | Sb | I |
|---|---|---|---|---|
| I (28 in) | 274.7 / 276 | 1465 / 1475 | 1794 / 1805 | 22,575 / 22,800 |
| II (36 in) | 368.4 / 369 | 2524 / 2530 | 3207 / 3220 | 50,842 / 51,000 |
| III (45 in) | 558.9 / 560 | 5066 / 5070 | 6168 / 6190 | 125,165 / 125,000 |
| IV (54 in) | 788.4 / 789 | 8903 / 8910 | 10,521 / 10,550 | 260,403 / 261,000 |

All within 1 % (mostly 0.1–0.5 %), the deficit consistent with the
unprinted web-flange fillets.

### `MiMdot70ISection` — PC-2L, 1 profile, `transcribed`

Chain 6 + 2 + 1½ + 4'-1½ + 3½ + 7½ = 70 in exactly (tip face, taper,
vertical step at web top, web, splay, bulb edge). No printed properties
exist for this beam; computed A = 814.4 in² (yb 36.03, Ix 539,616 in⁴).
End face (SECTION A-A, 1'-4 in web) not modelled.

### `MiMdot1800Section` — PC-4J, 1 profile, `transcribed-with-convention`

The "MI 1800" lead from the round-3 handoff. Depth 5'-10⅞ in = 1800 mm;
chain 3 + 2 + 4'-6½ + 5½ + 5⅞ = 5'-10⅞ in exactly. The 4'-6½ in member
reads 4'-6⅞ on a 600 dpi render; the ½ reading is required for closure
and matches the ~10:1 top-flange slope measured on the sheet. Fillets
R7⅞ (web junctions) and R2 (tip, bulb) are printed and modelled as
circular tangent arcs. Residuals vs BDG 6.60.02 (A 875, St 16,600,
Sb 18,800, I 624,700): A 867.0 (−0.9 %), St 16,481 (−0.7 %), Sb 18,813
(+0.1 %), I 622,633 (−0.3 %). Without the fillets A falls 5 % short.

### `MiMdotBulbTeeSection` — PC-5D / BDG 6.60.03, 7 profiles, `transcribed`

49 in top-flange bulb tee, depths 36–72 in. The outline is identical to
the round-3 OR15-182 BTB 002 transcription (tested polygon-equal), and it
reproduces the BDG printed A, Ybot, Ixx to 0.1 % at every depth (e.g.
BT36: 877.9 / 878.3, 18.18 / 18.2, 145,539 / 145,592). BT42 has no
printed row in the BDG table (text extraction drops it); its computed
values are recorded as calculated only. The three sizes shared with
`MiBulbTeeSection` (BT36/42/48) are intentionally kept in both families:
same geometry, different source (research report vs governing standard).

## Follow-up leads (recorded, not implemented)

- **BDG 6.65.02/02A/02B box beam property tables** (pp 146–148, issued
  05/22/23): 15 printed sizes, 12×36 through 60×48, with full A/YT/YB/
  St/Sb/I. This is the MDOT-standard box family and the counterpart to
  the OR15-182 recommendations already implemented. Note: OR15-182's
  17×36 calculated A (434.25) differs from BDG's printed 427 — the
  standard void/chamfer details must be transcribed from the p146–148
  sections, not assumed from OR15-182.
- **61 in top-flange bulb tee** (BDG 6.60.03 second table column, A
  932.4–1220.4): flange detail on BDG p127 / PC-5D p1 not yet transcribed.
- **Box Beam DGN bundle** (8 MicroStation files, BDG 6.29/6.65 sheets):
  native CAD for exact shear-key geometry; would upgrade the round-3
  SSBB `transcribed-with-convention` estimates.
- The five 1 MiB-truncated wayback files (roadside details) remain
  truncated; two were recovered from later captures (R-130-A, R-53-A).
