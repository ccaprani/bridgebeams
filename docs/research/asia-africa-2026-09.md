# Asia, Middle East and Africa: sources and translated data

Accessed 22 September 2026. This pass records 72 sources across 52 jurisdictions, plus seven jurisdictions with no usable primary girder source established in this pass. It adds 136 factual dimension/property rows (including explicitly flagged source contradictions). Source discovery is not equivalent to implementation readiness: a producer capability page, a project example, a historical standard, and a fully dimensioned authority drawing are separate evidence classes.

The machine-readable register is [asia-africa-sources.json](data/asia-africa-sources.json). Each record preserves original and English titles, organisation, URL, access status, evidence scope, and blockers. Downloaded PDFs and rendered reference images are private working materials in `sources/expansion/asia-africa/`; the register preserves their SHA-256 hashes and PDF page counts. The source PDFs retain their owners' copyright; this report translates technical labels and records dimensional facts rather than reproducing manuals.

## Highest-value findings

1. **Taiwan now has five implemented gross midspan profiles.** The Freeway Bureau's May 2020 *橋梁及結構工程設計注意事項* has Figure 10 and Table 14 on PDF p34, printed p30. Five precast **post-tensioned** types IV–VIII are fully dimensioned. Depths are 1350/1600/1850/2000/2100 mm. Type IV has top/web/base widths 500/200/650 mm; V–VIII have 1050/200/700 mm. B/C are longitudinal end-block lengths, not cross-section dimensions. The source does not publish section-property tables, so analytical geometric verification must be labelled separately from published-property validation. [Official PDF](https://www.freeway.gov.tw/Upload/DownloadFiles/%E7%99%BC%E6%96%87%E9%99%84%E4%BB%B62_%E6%A9%8B%E6%A2%81%E8%A8%AD%E8%A8%88%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A0%85%28%E5%88%9D%E7%89%88%29%20109.05.04%28%E9%A0%92%E5%AE%9A%E7%A8%BF%29_250654.pdf)
2. **Nepal has public precast RC drawings, not merely cast-in-situ PSC guidance.** Downloaded the 20 m and 25 m DoR volumes, 12 pages each. Sheet 5/10, PDF p7, gives midspan I profiles: depths 1300/1700 mm; top and base 700 mm; web 325 mm; top stack 150+65 mm, bottom 250+150 mm, clear webs 685/1085 mm. These are reinforced concrete, not prestressed. A 12×12 mm formwork chamfer note requires interpretation before an exact outline is coded. A 15 m volume is also indexed. [DoR library](https://dor.gov.np/index.php/home/publication/standard-superstructures-for-road-bridges)
3. **Indonesia supplies substantially more than five I girders.** WIKA's 44-page 2022 brochure contains six U sections, five I sections, four bare voided slabs, a bulb tee and four channel sections with published areas and inertias on PDF pp 17–20 and22. Twenty bare-section rows, four separately labelled composite rows and three conflicting segmental-box drawing/table rows are transcribed. I/U/bulb-tee sketches lack all flange/haunch dimensions; property tables do not justify inventing them. Voided slabs with 180 mm topping are composite properties and remain separate from bare precast values. [Manufacturer brochure](https://crm.wika-beton.co.id/wika-crm-storage/brochure/1660206289_Brosur%20WTON%202022.pdf)
4. **China's Chongqing T-girder volumes have an official public route.** A March 2022 transport commission notice links twelve full drawing volumes. It is explicitly a consultation version; the indexed drawing title identifies Ver1.0. A July 2022 attachment also surfaced, but publication status is not established. Local routing to the authority host fails; this is an access blocker rather than a purchase-only conclusion. [Official notice](https://jtj.cq.gov.cn/zwgk_240/zfxxgkml/gggs/tzgg/202203/t20220329_10565851.html)
5. **Sri Lanka and Malaysia have readily usable partial tables.** ICC supplies nine RDA drawing identifiers with overall dimensions and mass. OKA supplies PRT1/2/3 depth, clear web depth and area, plus a modified-depth range. Exact profile internals remain to be recovered. [ICC](https://icc-construct.com/public/products/bridge-beam), [OKA](https://www.oka.com.my/index.asp?CompanyID=29&LanguagesID=1&TitleReferenceID=1215)
6. **Bangladesh has a five-size preliminary PC-I series.** JICA report Table 8.3.1, PDF p94/printed 8-14, gives span/depth/base width: 25/1.60/0.70, 30/1.70/0.70, 35/1.85/0.65, 40/2.10/0.65, 45/2.20/0.80 m. These are explicitly preliminary cost-estimation designs. [JICA report](https://openjicareport.jica.go.jp/pdf/12249504_02.pdf)
7. **Morocco provides a new manufacturer I family.** SADET's raster p2 lists I40/I45/I50/I55 base widths 400/450/500/550 mm, span limits 25/26/28/29 m and masses 282/888/995/1150 kg/m. Bridge decks are explicitly an application. The anomalous first mass is preserved exactly as printed, not repaired. Heights and haunches remain unavailable. [SADET PDF](https://sadet.ma/wp-content/uploads/2023/09/poutres-industrrielles.pdf)
8. **Japan's alleged purchase gate is not exhausted.** SMC Preconcrete publicly links a six-page PC橋げた PDF and CAD download route. Local fetch and web screenshots timed out; no dimensions from it are claimed. [Catalogue](https://precon.co.jp/doboku-top/catalog/), [girder PDF](https://precon.co.jp/download/doboku-catalog/04-bridge/pc-bridge-girder.pdf)

## Translated terminology for existing sources

These translations support reading the existing `sources/research/research-china-jtg.md`, `research-japan-korea-sea.md`, `japan-ag-dim-tables.md`, `research-africa-mideast-cis.md`, and `final-kr-th-id.md`. They do not independently validate numerical assertions in those briefs.

| Language | Original term | English meaning and interpretation |
|---|---|---|
| Chinese | 装配式预应力混凝土T梁 | Precast/assembled prestressed-concrete T girder |
| Chinese | 梁高 / 腹板 / 梁肋 | Girder depth / web / girder rib or web |
| Chinese | 翼板 / 马蹄 / 湿接缝 | Flange / bottom bulb (literally horseshoe) / wet-cast closure joint |
| Chinese | 先张 / 后张 | Pretensioned / post-tensioned |
| Chinese | 先简支后连续 | Erect as simply supported, then make structurally continuous |
| Chinese | 通用图 / 公示 / 总校稿 | Standard/general-use drawings / public consultation notice / final proof submitted for review; do not equate a consultation draft to an issued standard |
| Taiwan | 預鑄後拉 / 配置尺度 / 梁端塊 | Precast post-tensioning / dimensional layout / girder end block |
| Japanese | 橋げた / けた高 / けた長 | Bridge girder / girder depth / girder length |
| Japanese | プレテンション / ポストテンション | Pretensioning / post-tensioning |
| Japanese | 断面 / 寸法 / 推奨仕様 / 許容差 | Cross-section / dimensions / recommended specification / permitted dimensional tolerance |
| Japanese | 上幅 / 下幅 | Top width / bottom width; neither is automatically a web width |
| Korean | 지간장 / 단면 제원 / 표준도 | Span length / section dimensions / standard drawings |
| Korean | 도심 / 긴장재 / 설계긴장력 | Centroid / prestressing tendon / design prestressing force; in CODIL tendon tables 도심 is the tendon centroid, not concrete centroid |
| Indonesian | Bentang / Tinggi / Lebar | Span / height / width |
| Indonesian | Penumpukan balok / Penyusunan balok | Beam stacking / beam arrangement or alignment |
| Indonesian | Pracetak / Prategang | Precast / prestressed |
| Vietnamese | Dầm / Dài / Rộng / Cao / Trọng lượng | Girder / length / width / height / mass or weight; inspect units |
| Vietnamese | Dầm hộp / Dầm T ngược / Bản rỗng | Box girder / inverted T girder / hollow slab; T ngược is not an upright T |
| Thai | คานสะพานคอนกรีตอัดแรง / คานรูปตัวไอ | Prestressed concrete bridge girder / I-shaped girder |
| Turkish | Köprü kirişleri / öngerilmeli / kesit | Bridge girders / prestressed / cross-section |
| French, North Africa | Poutres à fils adhérents | Beams pretensioned using bonded wires |
| French, North Africa | Double T / talon / âme / hourdis | I section (context dependent) / bottom bulb or flange / web / deck slab |
| French, North Africa | Base / portée limite / kg/ml | Base width / limiting span / kilograms per linear metre |
| Persian | تیرهای پیش ساخته / دهانه / پیش تنیده | Precast beams / span / prestressed |
| Arabic | كمرات سابقة الصب / سابقة الإجهاد | Precast girders / prestressed; precast does not itself imply prestressed |

## Source interpretation corrections

- HANDOFF and older briefs say "no national catalogue exists" for several countries. This pass establishes only what was found or not found; global nonexistence claims should not survive as facts.
- Manufacturer product names do not establish cross-country geometric identity. UAE/SA/Zimbabwe Y, M or U labels require their own drawing verification.
- An indexed document's recent crawl or upload date is not its design edition. WIKA's separately uploaded 2023 voided-slab manual has a 2009 internal date.
- WIKA area/inertia use cm²/cm⁴ while the library uses mm²/mm⁴: factors are100 and10000. Indonesian dots may be thousands separators. Vietnamese decimal commas must not be parsed as thousands separators.
- TN E&C's page headed "Super T" actually presents I, box and inverted-T rows. Its page heading cannot identify the geometry of every table row.
- Historical Korean Ministry and ADB sections are separate families from the KHC sections already in code. Their different widths must not be blended.
- Singapore BCA building catalogues and Pakistani girder/slab roofing catalogues are rejected as bridge-section sources unless an explicit bridge drawing is found.
- Ghana's AGC page is retained as a low-confidence lead because of internally inconsistent experience statements and a placeholder-like contact number. It does not count as an established section source.

## Coverage and next actions


### Indonesia

- **ID-WIKA-2022** — [WIKA Beton product brochure 2022](https://crm.wika-beton.co.id/wika-crm-storage/brochure/1660206289_Brosur%20WTON%202022.pdf); dimensions-transcribed. Manufacturer catalogue, not a national section mandate. cm dimensions converted by x10; cm2 by x100; cm4 by x10000. Dots in Indonesian property values are thousands separators. Flange/haunch details remain missing for I/U/bulb tee; do not reconstruct by scaling sketches.
- **ID-WIKA-VOIDED-MANUAL** — [Voided slab product manual](https://crm.wika-beton.co.id/wika-crm-storage/brochure/1700029120_Manual%20Voided%20Slab.pdf); downloaded-untranscribed. Dated 2009 internally; web upload date 2023 is not design edition.
- **ID-WIKA-PCI-MANUAL** — [PC I girder handling manual](https://crm.wika-beton.co.id/wika-crm-storage/brochure/1700029057_Manual%20Produk%20PC%20I%20Girder.pdf); downloaded-untranscribed. Six raster pages; inspected pp 2-3 describe transport, stacking, segment alignment and stressing beds. This is a handling manual, not the missing geometric dimension schedule.

### Taiwan

- **TW-FREEWAY-2020** — [Bridge and structural engineering design considerations, first edition May 2020](https://www.freeway.gov.tw/Upload/DownloadFiles/發文附件2_橋梁設計注意事項(初版)%20109.05.04(頒定稿)_250654.pdf); dimensions-transcribed. PDF p34 = printed p30, Fig10/Table 14. All drawing dimensions cm. A is beam depth; B and C are longitudinal end-block dimensions, not flange dimensions. Applies to standard precast post-tensioned midspan sections.

### Nepal

- **NP-DOR-PRECAST-25** — [Standard precast reinforced-concrete beams for 25 m span](https://dor.gov.np/home/publication/standard-superstructures-for-road-bridges/force/25-m-simply-supported-span-rc-deck-with-precast-rc-beams-compressed); dimensions-transcribed. Reinforced concrete, NOT prestressed. Sheet 5/10; plain outline dimensions transcribed, 12x12 mm formwork chamfer note retained. Span and full beam mass are not sectional properties. Midspan differs from 700mm-wide full rectangular end blocks.
- **NP-DOR-PRECAST-20** — [Standard precast reinforced-concrete beams for 20 m span](https://dor.gov.np/home/publication/standard-superstructures-for-road-bridges/force/2-m-simply-supported-span-rc-deck-with-precast-rc-beams-compressed); dimensions-transcribed. Reinforced concrete, NOT prestressed. Sheet 5/10; plain outline dimensions transcribed, 12x12 mm formwork chamfer note retained. Span and full beam mass are not sectional properties. Midspan differs from 700mm-wide full rectangular end blocks.
- **NP-DOR-INDEX** — [Standard superstructure drawings library](https://dor.gov.np/index.php/home/publication/standard-superstructures-for-road-bridges); source-confirmed. 15 m precast volume also available. Separate 30/35/40 m prestressed slab-deck entries are cast in situ: exclude those from precast families.

### Sri Lanka

- **LK-ICC-RDA** — [ICC RDA precast bridge beams](https://icc-construct.com/public/products/bridge-beam); dimensions-transcribed. Producer states RDA-standard products. Overall dimensions only; profile classification per each drawing still requires PDF. Companion PDF download returns 406.
- **LK-ICC-PDF** — [Prestressed bridge beam data sheet](https://icc-construct.com/wp-content/uploads/2023/04/2-Concrete-bridge-beams-_-bridge-component.pdf); access-blocked. Web index confirms source; local server response 406. HTML table recovered separately.
- **LK-ELS** — [RDA I and flat bridge beams](https://elslanka.com/product/bridge-beams/); source-confirmed. Manufacturer confirms standard range 5–25 m and RDA drawing basis; no outline dimensions captured.

### Malaysia

- **MY-OKA-PRT** — [JKR standard and OKA modified prestressed T beams](https://www.oka.com.my/index.asp?CompanyID=29&LanguagesID=1&TitleReferenceID=1215); dimensions-transcribed. Page explicitly marked old version. PRT-M depths 1450/1500/1550/1600/1650/1700/1800; area range 518350–623350 mm2. Do not infer individual PRT-M rows.
- **MY-PRESTASI** — [Prestasi beam range and properties](https://prestasi-concrete.com/products/); source-confirmed. Product page provides per-family beam-property links and brochure; local brochure fetch 403 while web reader can parse 4-page PDF.

### Vietnam

- **VN-TNEC** — [Bridge girder product table](https://tnec.com.vn/dam-super-t/); dimensions-transcribed. Page title says Super T but numeric table contains I, box and inverted T: do not label its I-section numbers as Super-T. Vietnamese Dài/Rộng/Cao = length/width/depth; comma decimal separator.
- **VN-620** — [Girder products](https://620chauthoi.com/danh-muc-sanpham/san-pham-dam/); source-confirmed. Primary producer catalogue with separate family product links; drawings not transcribed.

### Singapore

- **SG-CONINCO** — [Prestressed road and pedestrian bridge beams](https://coninco.com.sg/); source-confirmed. Producer confirms bridge applications but no numeric section catalogue captured. BCA structural precast handbook found in search is predominantly buildings, not a bridge-family authority.

### Philippines

- **PH-DPWH-25A00296** — [DPWH project drawings for AASHTO Type IV girders](https://www.dpwh.gov.ph/dpwh/sites/default/files/webform/civil_works/advertisement/25a00296_plans.pdf); source-confirmed. Primary procurement plans identify 24.70 and 24.40 m Type IV girders. Drawing geometry not visually transcribed this pass; adoption evidence only.
- **PH-FREYFIL** — [Precast prestressed girder producer](https://www.freyfil.com.ph/); source-confirmed. Producer capability lead; no dimensions captured.

### Bangladesh

- **BD-JICA-PC-I** — [Preliminary standard PC-I girders](https://openjicareport.jica.go.jp/pdf/12249504_02.pdf); dimensions-transcribed. Explicitly preliminary design for civil cost estimation, not final national standard. Report Fig8.3.2 maps b6 to bottom flange width; Table 8.3.1 gives H and b6.

### India

- **IN-RDSO-BS141** — [Railway PSC girder and slab standard-drawing index](https://rdso.indianrailways.gov.in/uploads/BS-141.pdf); access-blocked. Official PDF indexed with standard drawing numbers including B-10256/10258/10275/10276/10270/10290. Local connection refused; table column semantic check pending, so no structural-height numbers promoted.

### Pakistan

- **PK-EDS** — [Bridge girder casting-yard project capability](https://www.edsintl-pk.com/); source-confirmed. Primary engineering practice shows precast bridge girder yard; no cross-section schedule found. Roofing girder/slab vendors excluded from bridge data.

### China

- **CN-CQ-T-DRAFT-2022** — [Consultation on standard drawings for precast prestressed concrete T girders](https://jtj.cq.gov.cn/zwgk_240/zfxxgkml/gggs/tzgg/202203/t20220329_10565851.html); source-confirmed. Official notice links 12 complete volumes. March 2022 consultation draft status explicitly retained; July 2022 indexed attachment is a further publication lead. Local network cannot reach host. This corrects older implication that only reseller copies can be located; full dimensions not yet transcribed.
- **CN-CQ-T30-C-DRAWINGS** — [Precast prestressed T-girder standard drawings, 30 m, C series](https://jtj.cq.gov.cn/zwgk_240/zfxxgkml/gggs/tzgg/202203/W020220329617790453573.pdf); access-blocked. Indexed title block identifies Ver1.0, highway-I loading, span30 m, deck16.25 m, skew0°, TL-30-I-C-12. Not copied into section dimensions.

### Japan

- **JP-SMC-PC** — [Prestressed-concrete bridge girders](https://precon.co.jp/download/doboku-catalog/04-bridge/pc-bridge-girder.pdf); access-blocked. New free producer PDF: six raster pages; linked from https://precon.co.jp/doboku-top/catalog/ alongside CAD download link. Direct fetch and web screenshot timeout. Strong residual alternative to buying handbook; no dimensions claimed.

### South Korea

- **KR-CODIL-HISTORICAL** — [Historical PSC I girder standard-drawing tendon-work summary](https://www.codil.or.kr/filebank/original/MA/OTMCMA500808/OTMCMA500808.pdf); dimensions-transcribed. Table 2.4/2.5 distinguish historical standard families from KHC current-family data. 도심 is tendon centroid, not concrete-section centroid. H/BU/BB are depth/top width/bottom width in cm. Local TLS trust failure.

### Thailand

- **TH-POUND-MULTIBEAM** — [Prestressed concrete bridge multibeams](https://poundconcrete.co.th/product/i-shaped-prestressed-concrete-bridge-beam/); dimensions-transcribed. Published column labels w,W,D,T retained without assuming which flange each width describes until dimension sketch read. Dimensions cm; spans m.

### Türkiye

- **TR-BETONEL** — [Bridge girders](https://www.betonel.com.tr/assets/katalog/koprukirisleri.pdf); downloaded-untranscribed. Concise translation: high-strength prestressed bridge beams are made in varying sections and sizes to project requirements, erected spaced or adjacent. No dimension table in extracted text.
- **TR-ASSOCIATION** — [Precast association member product types 2024](https://www.prefab.org.tr/uploads/pdfcatalog/2023-yili-sektor-raporu.pdf); source-confirmed. Authoritative supplier index names bridge-beam manufacturers; scope does not assert one national KGM geometry.

### Iran

- **IR-PISHTANIDEH** — [Completed projects](https://www.pishtanideh.com/پروژه-ها/پروژههای-اجرا-شده/); source-confirmed. Project heading translates: decking of Bouin Baneh bridge using precast beams with 19 m span. No section drawing captured; span is project evidence.

### United Arab Emirates

- **AE-DUBAI-PRECAST** — [Civil engineering precast bridge girders](https://www.dubaiprecast.ae/_files/ugd/7455ee_31bff935f5fe4a10a51d9f2dd41faf3a.pdf); downloaded-untranscribed. Primary family list confirms local production. Do not silently assign Irish geometry to UAE types; project cover and mould details may differ.

### Saudi Arabia

- **SA-DLT-RIYADH** — [Riyadh Metro full-span precast deck beams](https://www.dlteng.com/Download_files/DLT%20brochure_7.1.pdf); source-confirmed. Equipment supplier describes 35 m, 500tonne deck beams for Line4. This is project-scale evidence, not a highway I-girder section catalogue.

### Oman

- **OM-OPHIOLITE** — [Precast beam types and applications](https://ophioman.com/wp-content/uploads/2018/02/Corporate_Brochure.pdf); source-confirmed. Printed p11 explicitly includes bridges in applications. Dimension labels are placeholders Depth/Breadth, not numbers; bespoke producer lead.

### Kuwait

- **KW-INDEX** — [Sabah Al Ahmad Sea City precast bridge girders](https://www.index-precast.com/infrastructure-projects); source-confirmed. Primary producer project confirms casting/installation of girder beams. No standard dimensions captured.

### Bahrain

- **BH-DELMON** — [Prestressed bridge beams and segmental bridge units](https://www.nasscorporation.com/delmon-precast/); source-confirmed. Primary manufacturer infrastructure product list, without numeric catalogue.

### Egypt

- **EG-ECPC** — [Precast bridge girder producer](https://www.ecpc.com.eg/about-us-precast-concrete-leaders/precast-concrete-infrastructure-history/); source-confirmed. Primary producer confirms bridge girder portfolio; dimension request lead only.

### Morocco

- **MA-SADET-I** — [Industrial prestressed beams for buildings and bridges](https://sadet.ma/wp-content/uploads/2023/09/poutres-industrrielles.pdf); dimensions-transcribed. Raster p2 explicitly lists bridge decks and civil bridges. Base = flange base width; Portées limites = limiting spans; Poids kg/ml = mass per linear metre. I40 mass printed 282 kg/m is retained as published, not corrected to fit progression. Depth and haunches absent; small web labels are not reliable enough to transcribe.

### Algeria

- **DZ-ENP-2018** — [Design of a post-tensioned prestressed beam bridge](https://repository.enp.edu.dz/jspui/handle/123456789/2543); research-lead. 2018 original student project in institutional repository, not an issued manufacturer/national catalogue. 36 m project spans; design PDF available, not transcribed.

### Tunisia

- **TN-PREFAB-IND** — [Bridge and civil-structure girders](https://www.prefabind.com/poutres-pour-ouvrages-dart/); source-confirmed. French double T means I-section in this context, not two-web US double tee. Fils adhérents means pretensioned bonded wire. Producer gives lengths up to30 m, no cross-section dimensions.

### Kenya

- **KE-MOLDTECH** — [Mombasa ring-road AASHTO girder moulds](https://moldtechsl.es/en/projects/post-tensioned-bridge-girders-in-kenya/); source-confirmed. 2021 supplier project: IV approximately30 m/48t; VI approximately40 m/81t. Adoption evidence, not certification that dimensions match unmodified AASHTO sections.

### Zimbabwe

- **ZW-TENSOR** — [Precast and prestressed bridge beam production](https://tensor.co.zw/services); source-confirmed. Primary local producer confirms bridge-beam production; no section tables.
- **ZW-OVUM-Y8** — [Mbudzi interchange Y8 precast beam decks](https://www.linkedin.com/pulse/new-mbudzi-interchange-harare-zimbabwe-ovum-corporation-1c2gf); source-confirmed. Designer-authored project article identifies Y8 beams at 23.85 m and22.4 m spans. Do not assume Irish Y8 cross-section is identical.

### South Africa

- **ZA-CIVILCON** — [Prestressed I/M/Y/T/U bridge-beam catalogue](https://civilcon-za.co.za/catalog/); existing-source. Existing source re-opened live and all six beam PDFs downloaded and visually checked. All 58 section/property rows are now in the machine-readable register. M10 drawing explicitly says1360 while table says360; both are preserved. Additional source discrepancies are documented below.

### Ethiopia

- **ET-AAU-2016** — [Original research on precast prestressed bridge girders](https://etd.aau.edu.et/items/1eff2da6-0998-4b9b-902f-2c6e3b9c20a2); research-lead. Institutional research source, not a national catalogue. No dimensions promoted; ERA2002 manual reseller copies not used as authority.

### Tanzania

- **TZ-MAGUFULI** — [Magufuli approach PSC beam construction](https://ptmc.tongji.edu.cn/yyljsen/article/html/202502005); research-lead. Original technical paper documents62 approach spans of40 m; figure-level beam outline still untranscribed. Deck-panel dimensions are not beam dimensions.

### Uganda

- **UG-UNABCEC** — [Ugandan precast industry report](https://www.unabcec.co.ug/site/assets/files/1378/the_contractor_magazine_-_issue_08.pdf); source-confirmed. Association publication confirms bridge beams among local precast applications; no supplier section table found in pass.

### Ghana

- **GH-AGC-LEAD** — [Precast producer bridge-project claim](https://agcprecast.com.gh/); research-lead. Uncorroborated commercial-site claim; internally inconsistent experience claims and placeholder-like phone number. Not trusted as established manufacturer evidence; keep only a low-priority verification lead.

### Nigeria

- **NG-NWAJA** — [Nwaja precast prestressed U-girder bridges](https://www.kedmor.co.il/nwaja-bridges); dimensions-transcribed. Designer primary project source: each20 m bridge uses three precast prestressed U girders, depth 1.2 m, structural in-situ topping220 mm. Overall project geometry only.
- **NG-JULIUS-BERGER** — [Precast full-span and segmental bridge decks](https://www.julius-berger.com/references/admiralty-alexander-link-bridge-lagos); source-confirmed. Design-build contractor confirms full-span precast approach elements and segmental box main bridge; no section schedule.

### Cambodia

- **KH-NEAK-LOEUNG** — [Precast PC composite T-girder approaches](https://openjicareport.jica.go.jp/pdf/12026142_02.pdf); source-confirmed. Printed p3-68 Fig3.2-39 has approach cross-section; main girders erected simply supported then connected with RC over supports. Figure dimensions remain untranscribed.

### Laos

- **LA-JICA-2010** — [Lao PC girder standard-drawing provenance](https://openjicareport.jica.go.jp/pdf/12013090_02.pdf); research-lead. Printed p2-87 explicitly begins discussion of standard PC girder drawings. Follow following page to identify issuing source; do not repeat its dated no-design-standard statement as a current fact.

### Myanmar

- **MM-JICA-DRAWINGS** — [PC-I and PC-box bridge drawing volume](https://openjicareport.jica.go.jp/pdf/12304721_01.pdf); source-confirmed. Official consultant drawing volume; PC I specified separately from segmental box and RC deck. Precise report title and section pages need catalogue lookup; no dimensions promoted.

### Brunei

- **BN-DYWIDAG** — [Jalan Telanai precast post-tensioned I girders](https://assets.ctfassets.net/wz1xpzqb46pe/2C80OZ0JEm8ItSlLOyXVd7/23aa08d4f7624777cf75fcdca467569b/Case-Study2015Info-2346DYWIDAG-Strand-Tendons-for-flowing-Road-TrafficNew-Viaducts-in-BruneiDSI-ConstructionBrunei.pdf); source-confirmed. Supplier case study printed 46 identifies27 m and36 m precast girders plus mould/stressing-bed supply. No transverse dimensions.

### Mozambique

Native Portuguese search did not establish a primary reusable beam-section source in this pass. Historical Tete bridge paper mirrors and building-beam catalogues were not promoted. No claim is made that a national or manufacturer catalogue does not exist.

## Concrete unblocking queue

1. Taiwan: implemented five fully dimensioned gross midspan profiles in `bridgebeams.tw`; 16 targeted geometry checks pass. Analytical strip integration validates area/centroid/inertia, but no published property table exists for independent published validation.
2. Nepal: obtain15 m volume and verify precisely where12 mm chamfers apply to the 20/25 m main profiles.
3. WIKA: resolve I/U flange haunches from manufacturer drawing rather than fitting properties; channel profiles have much richer dimensions.
4. China: obtain the issued Chongqing drawing volumes via authority-host access; consultation draft status must remain attached.
5. Japan: retrieve SMC public six-page PDF/CAD through a functioning network route; do not infer all AG/BG series geometry from a single drawing.
6. Sri Lanka: retrieve ICC PDF through a browser if406 persists; map each RDA identifier to an actual section type.
7. Malaysia: follow Prestasi family-property links, using browser PDF access where the local fetcher returns403.
8. Bangladesh/Cambodia/Myanmar: use report drawing volumes for project-specific sections, retaining preliminary versus issued status.
9. Manufacturer-only countries: obtain a dimensioned product sheet before creating a geometry family. No supplier messages were sent.


## Final PDF audit: South Africa and Indonesian composite properties

All six Civilcon one-page PDFs are retained locally with SHA-256 metadata in the register. This is re-verification and enrichment of an existing source, not six new manufacturers. Their factual dimension/property tables add 58 rows:20 I, 9 M, 8 Y, 10 T, 9 U and2 special U. Top/bottom section moduli are stored in mm³ after multiplying the printed ×10⁶ columns; area remains mm² and centroid mm. Raw suspect numbers are preserved with discrepancy notes.

| Sheet | Verified drawing interpretation and remaining issue |
|---|---|
| [PPBI](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBI.pdf) | B1 is soffit width; B2 is width at the upper edge of the bottom flange; B3 is web width; B4 is top width. D2/D3/D4/D5/D6 progress upward from the soffit: bottom flange, bottom splay, clear web, top splay, top flange. All 20 integrated areas match exactly; centroid rounds within 0.49 mm; top/bottom modulus errors are below 0.0003% except I18 top modulus (printed 213.0987×10⁶, 0.417% discrepancy). Weight header says kN/m³ but numeric values represent kN/m at 25 kN/m³. |
| [PPBM](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBM.pdf) | Maximum base970 mm. Drawing explicitly marks M10 as1360 mm; table prints360 mm. M4 table area37860 mm² is inconsistent with listed9.47 kN/m at 25 kN/m³. Neither anomaly is silently repaired. Upper flange/step contour still needs complete decoding. |
| [PPBY](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBY.pdf) | Maximum base750 mm; bottom chamfers25 mm; lower flange side zone177 mm and upper bottom splay177 mm; side offset5 mm; web junction radius100 mm. Top ledge detail distinguishes70 mm topdeck and40 mm in-situ slab arrangements. Variable top-width/step interpretation remains a geometry blocker. |
| [PPBT](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBT.pdf) | Base495 mm, web105 mm, upper flange205 mm, chamfer25 mm, bottom side offset6 mm. T10 drawing labels850 mm while property table says815 mm. Resolve against another manufacturer-issued drawing before implementation. |
| [PPBU](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBU.pdf) | Actual table sizes U1/U3/U5/U7/U8/U9/U10/U11/U12; no U2/U4/U6 rows. Base970 mm, outer batter6.75vertical:1horizontal, labelled web165 mm, top flange250 mm, top step30 mm. U10 bottom modulus255.65×10⁶mm³ is inconsistent with its top modulus/centroid. U5 weight13.76 kN/m conflicts with area×25 kN/m³=13.6004 kN/m. |
| [PPBUS](https://civilcon-za.co.za/wp-content/uploads/2017/05/PPBUS.pdf) | Index calls these US1/US2; drawing/table use SU1/SU2. Base2000 mm; depths900/1200 mm; top lobes350 mm; top steps50 mm; normal web125 mm. Explicit density is25.5 kN/m³; listed weights19.5/22.56 agree with that density. Header erroneously labels weight kN/m³. |

The existing `za/civilcon_i_beam.py` was compared directly with the source during this audit. Its numeric dimension rows matched, but the old implementation started the B4 face at y=0 and called the drawing's B1 soffit an "as-cast" face without source support. For I1 the old implementation gave centroid 391.78 mm from y=0, whereas the source-oriented profile gives318.22 mm. Vertical reflection leaves area and centroidal inertia unchanged; it swaps top/bottom interpretation. The implementation is now corrected to B1 soffit at y=0. All 24 focused tests pass:20 source-table rows enforce centroid, top/bottom widths and top/bottom moduli; I1 also has an independent source-literal orientation regression. The I18 top-modulus discrepancy is specifically pinned; it does not weaken tolerances for the other39 modulus values. Dimension metadata keys were renamed to match their actual bottom/top meanings; dataclass b1…d6 attributes remain unchanged.

WIKA p19 composite rows are VS57/62/66/74 plus 180 mm topping. Published composite areas are5766/5815/6201/6492 cm² and inertias2855560/3435186/4020154/5300499 cm⁴. These are explicitly separate from bare precast values; the effective transformed topping basis is not stated in that brochure. On p20, the 50 m road/LRT box bottom slab is200 mm on drawing versus 300 mm in table; the 100 m road/LRT box has depth upper bound3483 versus 3484 and top slab250 versus 225; the 40 m rail box top slab is250 versus 300. Store raw alternatives, do not manufacture a consistent polygon from the mixed labels.

WIKA's voided-slab manual is predominantly handling/erection guidance: its contents translate as beam overview, prestressing, lifting, transport, unloading, installation system, installation stages, stressing stages, asphalt surfacing and final arrangement. It is not a replacement for missing section/haunch dimensions. The short PC-I manual likewise concerns handling/segment alignment/stressing. No further beam profile schedule was established in these two manuals.


## Final geographic gap pass

The final bounded pass searched Jordan, Lebanon, Israel, Iraq, Senegal, Côte d’Ivoire, Cameroon, Rwanda, Zambia, Botswana, Namibia, Mauritius, Angola, Sudan, Mongolia, Bhutan, Maldives, Timor-Leste, Fiji and Papua New Guinea. Oman was already represented by the Ophiolite source. It adds 15 source records across14 additional jurisdictions and five partial dimensional rows; it adds no further executable geometry. Non-beam precast products, generic bridge pages and unverified national-standard claims were excluded.

| Jurisdiction | Useful primary or original project evidence | Geometry limit |
|---|---|---|
| Jordan | [CECC: Wadi Mujib precast transverse bridge beams](https://www.cecc.com.jo/projects.php?cat=31&id=84) | Transverse members; no longitudinal-girder dimensions. |
| Lebanon | [CCL: Fidar precast post-tensioned bridge beams](https://www.cclint.com/case-studies/fidar-bridge-lebanon/) | 100 post-tensioned precast beams, 34 m length each; no section. |
| Israel | [Cebus Rimon: Prestressed U, AASHTO and reversed-DT bridge products](https://www.cebus-rimon.co.il/en/products/productsinfrastructure/) | U/AASHTO/reversed-DT families explicit; no geometric equivalence presumed. |
| Iraq | [Dijla Precast: Prestressed and post-tensioned bridge girder production](https://dijla-precast.com/production-lines/) | Bridge girder production explicit; indexed extract only after fresh-open timeout. |
| Senegal | [Bruno Theaudin, Eiffage TP; RGRA903: Dakar-Diamniadio precast RC I-beam structures](https://www.editions-rgra.com/system/files/revues/rgra_903.pdf) | Constructor-authored RGRA article; precast RC I beams, not PSC; spans are not lengths. |
| Côte d’Ivoire | [Millennium Challenge Account Côte d’Ivoire: Yopougon precast bonded-wire girder specification](https://www.mcacotedivoire.ci/uploads/pdf3/MCA-CI_QPBS290%20DAO%20BPaix%20et%20Yop%20Exp_Addendum%20n01_06092022_VF.pdf) | Agency tender addendum identifies bonded-wire pretensioned beams; superseded material table excluded. |
| Cameroon | [African Development Bank / project agencies: Logone post-tensioned precast girder bridge option](https://www.afdb.org/fileadmin/uploads/afdb/Documents/Environmental-and-Social-Assessments/Cameroun-Tchad-projet_de_pont_sur_le_logone-resume_EIES_07_2017-fr.pdf) | Agency-selected VIPP project type, no section schedule; direct PDF access blocked. |
| Botswana | [Corestruc / CoreSlab; Civil Engineering Contractor: Platjan precast prestressed T-beam project](https://www.corestruc.co.za/wp-content/uploads/2019/05/sa-botswana-platjan-brdge.pdf) | Supplier-hosted site report p2:800 mm depth, 15.3 m beam length, 15.5 m structural span; imported SA production. |
| Angola | [Tecnovia Angola: Prestressing of Pumangol viaduct deck beams](https://tecnovia.pt/portfolio-posts/pre-esforco-em-vigas-do-tabuleiro-viaduto-da-pumangol/) | Depth 1350 mm; web180 mm; manufacture lengths17.4/20.5/20.4/22.9/13.9/19.6 m; flange/haunch dimensions absent. |
| Angola | [BETAR: Soyo bridge over Cadal Channel](https://www.betar.pt/projecto/ponte-do-soyo-sobre-o-canal-cadal-para-acesso-a-base-do-kwanda-da-alng/) | 1200mm-deep pretensioned I beams manufactured in Portugal; four beams across deck; no width/haunch schedule. |
| Sudan | [World Bank: Atbara precast post-tensioned girders, historical project](https://documents1.worldbank.org/curated/en/270271468340280874/pdf/multi-page.pdf) | Historical1989 report p23 identifies precast post-tensioned girders, 9 spans about 40 m; no current catalogue claim. |
| Mongolia | [Mongolia public procurement portal / Ulaanbaatar project employer: First Ring Road, Ulaanbaatar — Technical Requirements, PartIII-B](https://user.tender.gov.mn/uploads/techspec/68c2ce03aef2e.pdf) | 220-page official tender recovered; precast small boxes25–30 m distinguished from cast-in-place special crossings. |
| Maldives | [Afcons Infrastructure: Greater Malé Connectivity Project precast segment dimensions](https://www.afcons.com/sites/default/files/2023-08/INSIGHT-JULY-2023.pdf) | Constructor reports maximum segment height8177 mm; indexed PDF extract, page unverified and direct download403. |
| Fiji | [Fletcher Higgins Fiji: Fiji precast bridge beam manufacture and construction](https://www.higgins.co.nz/fletcher-higgins) | Constructor confirms bridge-beam manufacture at Suva casting bed; no section catalogue. |
| Papua New Guinea | [CB Builders: Prestressed precast concrete for PNG bridges](https://cbbuilders.com.pg/) | Producer explicitly supplies prestressed concrete for bridges; separate steel-girder claims excluded. |

New translation aids: Portuguese *altura* = depth, *alma* = web, *comprimentos de fabrico* = manufacturing lengths, *pré-lajes* = precast subdeck panels, and *pré-tensionadas com cordões aderentes* = pretensioned with bonded strands. Mongolian *угсармал урьдчилан хүчитгэсэн бетонон жижиг хайрцган дам нуруу* denotes precast prestressed small-box girders; *цутгамал* in the contrasted bridge descriptions denotes cast-in-place construction. The latter distinction prevents promoting the longer special-span cast-in-place boxes as precast products.

No usable primary girder source was established in this pass for:

- **Rwanda:** general specifications and third-party mirrors, without a producer/agency section source.
- **Zambia:** steel-bridge lifting projects and broad regional contractor pages, without specific concrete girder evidence.
- **Namibia:** OTESA/SMEC describe prestressed twin-spine bridges but do not establish precast beam production in the inspected pages.
- **Mauritius:** fascia details, generic precast claims and an unnamed footbridge reference did not establish a specific beam source.
- **Bhutan:** official generic precast-handling clauses do not establish an actual precast main-girder family. The Dechencholing construction paper describes cast-in-place girders with precast slab formwork.
- **Timor-Leste:** the inspected Comoro JICA report identifies precast kerbs/blocks; the port report identifies imported piles/slabs. Neither establishes a precast bridge-girder family.

These are documented search limits, not assertions that suitable sources do not exist. All three newly retained PDFs (Mongolia220pp, Senegal72pp, Botswana4pp) have checked SHA-256 hashes. The new inaccessible PDFs retain explicit fetch errors; no files or hashes are invented. Guinea's separately discovered JICA project source is recorded in the Europe/Americas worker's register to avoid duplication.
