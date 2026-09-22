# Banagher CAD recovery and implementation follow-up

Colin's visual review of 22 September 2026 confirmed that the W inner concrete contour consists of flat surfaces, and directed the search to locally held CAD. **All sixteen current W sizes and the eight 1500 mm Solid Box variants are now implemented.** The two families have different evidence: W combines current catalogue dimensions with recovered producer CAD; Solid Box class (4) retains the fully dimensioned nominal manual outline despite an inconsistent property table.

The [machine-readable audit](data/banagher-cad-followup.json) records source hashes, 50 extracted DWG streams, converted DXFs, units, entity types, CAD handles, dimensions and current W property residuals. Original drawings and workbook remain private working sources under the ignored `sources/expansion/banagher-cad/` directory.

## Recovered workbook

The source is `/mnt/data/sync/consulting/Roughan O'Donovan/Structure B01/05316 Beam Design/05316 Precast Beam Properties.xls`. The copy `/home/ccaprani/projects/PyBridge/05316 Precast Beam Properties.xls` has the identical SHA-256 `6fef29031818d59e96600517c4e2012441fe2eebb57f998bb84261a30fe9855d`.

Fifty `MBD…/Contents` OLE streams are embedded DWGs, signatures AC1014/AC1015. Extraction reads their exact bytes with `olefile`, preserving a separate hash per stream. All match the earlier `/tmp/xls_extract/` extraction. Previously converted DXFs, made with LibreDWG 0.11.3876, were copied into persistent local source storage. `ezdxf.recover` reads all fifty without remaining audit errors; its recovery fixes are recorded per drawing. Some drawings declare unit code 0 and others 4: this is not permission to assume every drawing is full-scale millimetres.

The nineteen worksheet names are T, TX, TY SS, TYE SS, TYS SS, TYR SS, TY–TYE BS, TYS–TYR BS, JS, Y–YE BS, YS–YR BS, SY–HY BS, U, HU–SU BS, MB–UMB, BOX BEAM, GR–LR, DT 60+80 and DT 80+80. **Neither W nor SD Solid Box is a named worksheet.** The BOX BEAM table is the hollow B family. The U-family CAD `MBD00011259` has a 970 mm lower flange, so it must not be used as the 1500 mm lower-flange W outline.

## W: a separate producer project drawing resolves the lower contour

Actual source: `/mnt/data/sync/consulting/Roughan O'Donovan/W19 BEAM STRUCTURE B06 BALLYKEEFFE BOREEN OB.dwg`. The drawing carries Banagher Concrete Ltd and W19 internal/external beam titles for Structure 6. It is an older project source, with file modification date in November 2006; no current catalogue revision is inferred from that timestamp. Read-only conversion used the installed `/home/ccaprani/anaconda3/envs/dwg/bin/dwg2dxf`.

The dimensioned section is drawn at 1:25 within modelspace: the 2300 mm depth spans 92 drawing units and the 1500 mm width spans 60. Dimension entities explicitly establish the scale. The section's bottom dimensions are:

| Detail | Dimension | CAD dimension handles |
|---|---:|---|
| Lower flat / overall width | 1460 / 1500 mm | 118A82 / 118A84 |
| Bottom corner horizontal chamfers | 20 mm each | 118A81 / 118A83 |
| Bottom corner vertical rise | 20 mm | Exact LINE endpoints 118A66 / 118A73 |
| Central inner valley above soffit | 160 mm | 118A8D |
| Inner valley to haunch rise | 50 mm | 118A8A |
| Valley to haunch horizontal run | 500 mm each | 118A8B / 118A8C |
| Lower inner haunch | 125 mm run × 150 mm rise | 118A7F / 118A89 |

Thus the inner lower right vertices are `(0,160)`, `(500,210)`, `(625,360)` mm. Their connections are straight LINE entities. No radius is present. Modelspace coordinates and LINE handles are preserved in the audit rather than estimated from the rendered image.

The old project's upper W19 details are **F = 52 and V = 512 mm**; the current third-edition manual gives **F = 100 and V = 464 mm**. The implementation uses the current manual's F/S/V/Web and W1/W2/W3 values separately for each row, and only the verified common lower contour from the older CAD. Every variable vertical chain closes exactly at the 360 mm inner haunch. It does not substitute the old W19 wholesale.

All sixteen current polygons reproduce published areas within 4 mm² and centroidal Ixx within 0.0025%. Centroids agree within 0.05 mm except W11: calculated 631.247381 mm versus printed 631.3 mm, a signed residual of −0.052619 mm. That individual rounding/intermediate-calculation discrepancy is explicitly pinned; no family-wide tolerance is relaxed to hide it. Published values remain unchanged. The API is `IeWBeamSection` / `IeWBeamDimensions` in `bridgebeams.ie.ie_w`; W2, W4 and W6 are absent from the source and not invented.

## Solid Box width class (4): nominal geometry with explicit source discrepancy

The current manual already fully dimensions the outline: overall width 1500 mm, upper width 1370 mm, shoulder run 65 mm, shoulder rise 30 mm, outer vertical face 35 mm and bottom chamfer 25 × 25 mm. Those dimensions define an unambiguous polygon. No matching SD CAD was identified in the recovered workbook, and no claim of CAD verification is made for this family.

The eight variants `SD1 (4)` through `SD8 (4)` are now exposed by `IeSolidBoxBeamSection`. They use the nominal drawing without fitting. Published area exceeds geometry by 225 mm² for SD1–SD5 and 275 mm² for SD6–SD8. Calculated centroid and section-modulus differences are preserved beside literal source properties in `ie_solid_box.json`. Tests pin those signed area discrepancies and independently transcribed nominal moments; classes (1)–(3) retain their existing strict checks. Resolution of the inconsistent table is still a source erratum task, but it does not prevent use of the clearly specified nominal outline.

## Verification

`python -m pytest tests/test_ie_w.py tests/test_ie_solid_box.py -q`: **45 passed**, including sixteen independent W property comparisons, all twenty-four existing Solid Box property comparisons, eight class-(4) nominal checks, actual sectionproperties mesh creation for both families, symmetry, validity, winding and the current-versus-old W19 revision distinction. All fifty recovered DWG hashes and DXF hashes are reread from persistent storage and recorded in the audit. Geometry/property agreement is not a structural capacity check or manufacturer approval.
