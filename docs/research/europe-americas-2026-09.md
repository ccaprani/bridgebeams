# Europe, Americas and supplementary CIS/Baltic source expansion

Research and access date: 22 September 2026. This pass searches in native languages, downloads primary documents, and preserves published dimensions separately from future geometry reconstruction. The machine-readable companion is `data/europe-americas-sources.json`. Local PDFs, extracted text and rendered pages are reference-only materials under `sources/expansion/europe-americas/` and are intentionally ignored by git.

The registry contains **77 source records across 59 country codes and 394 transcribed dimension/property rows**. Four records reverify inherited Ireland/UK/Australia provenance; they are not newly discovered countries. A separate Banagher backlog transcription adds 48 rows from the existing manual in `data/banagher-pending-families.json`; 24 Solid Box variants are implemented and tested, while the inconsistent 1500 mm width and incomplete W geometry remain research-only.

## Verified additions and useful transcriptions

- **Slovakia:** VÁHOSTAV publishes a 32-page Slovak catalogue and a matching English edition. The English edition has 20 rows covering six PM edge/interior variants, three 1.0 m inverted-T girders, six 1.2 m I girders, three 1.4 m I girders, and 1.9/2.1 m post-tensioned R2 girders. Area, centroid from soffit and inertia are retained with explicit units. PDF pages 6, 8, 10, 12, 14, 16, 19, 21, 23. Full section drawings include rounded haunches and prestressing arrangements. This unlocks source access; it does not yet validate reconstructed geometry.
- **Netherlands:** Haitsma HRP/HIP brochure contains 30 bare-section area/centroid/inertia rows: 12 HRP, 9 HIP with topping and9 HIP with wet joint. The two HIP variants have different precast shapes. HKO/HKO-XL adds 20 rows. HKO inertia values are retained raw because its graphical header omits the multiplier; no normalized HKO inertia is asserted. HKO-XL explicitly prints its multiplier. Never mix bare and composite section columns.
- **Mexico:** SEPSA p4 supplies seven metric AASHTO-labelled profiles and their published areas; p5 supplies seven Nebraska variants with 18/20 cm web options. These are producer variants, including modified I and IV sections, and must not silently alias US AASHTO sections. Seven p4 producer profiles are now implemented under `src/bridgebeams/mx/` and independently tested against published area rounding. Pages 6–9 add 103 box/Type-U width-and-area rows plus six family envelopes. These retain original cm/cm² units and separate closed and first-stage open castings; no rounded box geometry is implemented.
- **Romania:** Somaco publishes 21 rows over IPTANA, Eurocod-labelled and motorway ranges (PDF pp 3-4), with explicit depth, beam length, design length, volume and mass. ASA Consolis pp 97 and99 add dimensioned/strand drawings for the 42/52/72/80 cm families. The two producers should remain separately attributed.
- **Italy:** Paver image-only datasheets were rendered and read visually. UHP80/100/120/140/160/170 and UHP60, plus HTP40/50/60, have transcribed overall/tabulated dimensions. Web and flange thicknesses are not published on those sheets. Another 23 VHP/IHP/THP/BOX envelope rows were transcribed from the brochure. The HP125 sheet and several IHP designations have conflicts; see below.
- **Hungary:** Ferrobeton supplies FPT,FP,ITG and FI150 PDFs, plus DWG links from its bridge page. FPT has seven size/length/mass rows; ITG has four depth/length ranges. Drawings distinguish support and midspan sections. Superscript terminal digits in drawing dimensions mean decimals, not powers.
- **Kazakhstan:** Search indexing of AZMK primary bilingual tables gives six TBN lengths and three VTK lengths with explicit mm dimensions and volumes. Direct retrieval failed TLS validation and the browser request timed out; these are `primary_search_index_table` records pending primary-body verification, not confirmed live-table transcriptions. TBN18 has two depth/volume alternatives that are retained as alternatives, not silently combined.
- **Czechia:** ŽPSV MK-T envelope is read from PDF p103 (printed spread204-205): maximum length3000 cm, B40-60 cm,H60-165 cm, maximum mass70000 kg. Producer explicitly offers project/design drawings on request. Do not treat B as overall flange width without the drawing definition.
- **US/Canada:** WSDOT provides 48 envelope rows across I/WF, deck and tub sheets. Its I/WF sheet was revised 2016-04-07; the deck and tub sheets are revised 2026-07-30 and stamped **PRELIMINARY PLAN — NOT FOR CONSTRUCTION**. Eight Ontario MTO NU envelopes are transcribed from sheets explicitly marked **DRAFT**, as is the accompanying guide. These are source snapshots, not verification that a particular edition governs a new design.

## Corrections to inherited claims

1. The old German Bauarchiv-DDR URL ending`00125-0105-z8463kme.pdf` was successfully downloaded but is **not a BT500/700 girder drawing catalogue**. Its 26 pages are an 1987 precast-concrete production/material-quantity catalogue. It is retained as `rejected_miscited_source`; a correct girder drawing source remains needed.
2. The inherited phrase “no national catalogue exists” is not repeated here. Finding producer sources, or failing to find a national source in a bounded search, cannot establish worldwide absence.
3. Paver `hp-125-sezione-filante.pdf` has headingHP125 but table designationHP100 and depth 100 cm. Its sketch shows120 cm top width and125 cm bottom width. The table is preserved without resolving the naming inconsistency.
4. Paver UHP60 sketch gives114.4 cm while its table rounds/prints114 cm. Neither is silently substituted for the other.
5. VÁHOSTAV English p14 incorrectly repeats a2016-T heading; p13 and the p14 table identify the 1.2 m section as2010-I. Keep this warning beside downstream data.
6. Source values are not “corrected” to force mass=volume*density or area=volume/length. End thickening and rounding can make those checks inappropriate; suspicious values remain explicit.
7. Paver IHP120/125/130/135/140 rows print H=90/85/80/75/70 cm respectively; these are recorded as designation/depth conflicts, not corrected from the family names. VHP width also differs between sketch (97.4 cm) and table (97 cm).
8. SEPSA TC180 Type-U area repeats 7280 cm² for widths 190 and 200 cm; retain the source and resolve the suspicious duplicate before implementation. TC135 closed drawing prints 300 cm maximum width while its tables use 310 cm.
9. The Finnish Parma PDF is an example bridge general arrangement dated23 November2017, with 16 m span and9.3 m useful width. It is not a complete dimensioned beam catalogue.

## Translation guide for existing and new material

| Language | Source term | English meaning / transcription caution |
|---|---|---|
| Spanish | peralte; alma; patín | overall depth; web; flange |
| Spanish | claro; longitud | span/opening; physical length; do not interchange |
| Spanish | trabe cajón; aleta | box girder; projecting flange/wing |
| Spanish | pretensado; postensado | pre-tensioned; post-tensioned |
| Portuguese | viga; banzo; alma; vão | beam; flange; web; span |
| French | poutre; âme; talon; hourdis | beam; web; bottom bulb/flange; deck slab |
| French | précontrainte par adhérence | pretensioning with force transferred by bond |
| Dutch | ligger; druklaag; natte knoop | girder; structural topping; cast-in-place wet joint |
| Dutch | zwaartepuntsafstand vanaf onderzijde | centroid distance from soffit |
| Dutch | h.o.h.; samengestelde doorsnede | centre spacing; composite section |
| Italian | altezza; larghezza; sezione filante | depth; width; constant longitudinal section |
| Italian | T rovesciata; trave a cassone | inverted T; box girder |
| Slovak/Czech | nosník; výška; dĺžka/délka | girder; depth; physical length |
| Slovak | ťažisko od spodnej hrany; moment zotrvačnosti | centroid from lower edge; second moment of area |
| Romanian | grindă; înălțime; lungime de calcul | beam; depth; design length |
| Romanian | corzi aderente; T întors; greutate | bonded prestressing strands; inverted T; mass in the kg/t tables |
| Hungarian | hídgerenda; tartómagasság; ajánlott hossz | bridge beam; girder depth; recommended length |
| Hungarian | tartóvég; tartóközép; súly | support/end section; midspan section; mass in kg/m tables |
| Finnish | jännepalkki; yleispiirustus; poikkileikkaus | prestressed beam; general arrangement; cross-section |
| Swedish/Danish | balk/bjælke; förspänd/forspændt | beam; prestressed |
| Russian | балка; двутавровый; тавровый | girder; I-section; T-section |
| Russian | пролетное строение; натяжение на упоры | bridge superstructure/span structure; pretensioning against abutments |
| Russian | ширина плиты; высота; масса | slab/flange width; depth; mass |
| Ukrainian | мостові балки; попередньо напружені | bridge girders; prestressed |
| Estonian/Latvian/Lithuanian | tala/sija/sija | beam (bridge application must be verified separately) |

Translations describe technical meaning, not equivalence of national product families. Keep original designations, original units and source page beside translated labels. Decimal commas are numeric decimal separators; superscript fractions/decimals on drawings require visual inspection.

## Country/source pass

Status is intentionally granular. `primary_web_source` verifies a producer/application lead, not a dimensioned catalogue. `verified_partial_transcription` means only listed facts were checked. Download failures describe this access attempt; they do not establish paywall or permanent unavailability.

| Country | ID | Organisation and source | Status | Transcribed rows |
|---|---|---|---|---:|
| Argentina | `ar_pretensa` | [Pretensa: Bridge system](https://www.pretensa.com.ar/multimedia/downloads/11/12/puentes.pdf) | `verified_partial_transcription` | 2 |
| Armenia | `am_kamurjshin` | [Kamurjshin CJSC: Bridge-beam production](https://kamurjshin.am/en/artadrutyun/2.html) | `primary_web_source` | 1 |
| Australia | `au_as5100` | Standards Australia: AS5100.5 Appendix D bridge beam sections (no verified URL) | `inherited_code_citation_unverified_source` | 0 |
| Austria | `at_tuwien` | [TU Wien: Thin-walled precast concrete girders in bridge and civil engineering](https://www.tuwien.at/cee/tragkonstruktionen/beton/forschung/abgeschlossene-forschungsprojekte/duennwandige-beton-fertigteiltraeger-im-bruecken-und-ingenieurbau) | `primary_web_source` | 0 |
| Belarus | `by_ozjbk` | [Osipovichi Reinforced Concrete Plant: Products](https://ozjbk.by/produkciya/obshhegrazhdanskoe-stroitelstvo/progony-zhelezobetonnye/) | `web_access_blocked` | 0 |
| Belize | `bz_mnm` | [M&M Engineering: Precast concrete bridge products](https://mnmengineeringbz.com/products) | `primary_search_index_lead` | 0 |
| Bosnia and Herzegovina | `ba_mucic` | [Mučić: Precast elements](https://mucic.ba/predgotovljeni-elementi/) | `primary_web_source` | 0 |
| Brazil | `br_protensul` | [Protensul: Products](https://www.protensul.com.br/site/) | `primary_web_source` | 0 |
| Bulgaria | `bg_rila` | [Rila: Road construction elements](https://www.rila-bg.com/bg/елементи-за-пътно-строителство.html) | `primary_web_source` | 0 |
| Canada | `ca_mto_guide` | [Ontario MTO: Prestressed Concrete Girder Guidelines August 2023](https://tcp.mto.gov.on.ca/sites/default/files/2023-08/Prestressed%20Concrete%20Girder%20Guidelines%20%28August11%202023%29.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Canada | `ca_mto_nu` | [Ontario MTO: Prestressed NU Girders and Bearings](https://tcp.mto.gov.on.ca/sites/default/files/2023-08/NU-Girder-July-2023.pdf) | `verified_partial_transcription` | 8 |
| Chile | `cl_hormisur` | [Hormisur: Bridge and grade-separated crossing beams](https://www.hormisur.cl/vigas-de-puente-y-pasos-desnivelados.php) | `primary_web_source` | 0 |
| Colombia | `co_preansa` | [Preansa: Infrastructure](https://preansa.com.co/infraestructura/) | `primary_web_source` | 0 |
| Costa Rica | `cr_puenteprefa` | [PuentePrefa Ltda: Precast bridge elements](https://www.puenteprefa.cr/elementos_prefabricados.html) | `primary_web_source` | 1 |
| Croatia | `hr_gpkrk` | [GP Krk: Precast elements catalogue](https://www.gp-krk.hr/img/Katalog.pdf) | `adjacent_catalogue_bridge_applicability_unverified` | 0 |
| Czechia | `cz_zpsv` | [ŽPSV: Concrete products catalogue 2022](https://www.zpsv.cz/wp-content/uploads/2023/04/ZPSV-katalog-2022.pdf) | `verified_partial_transcription` | 1 |
| Denmark | `dk_crh` | [CRH Concrete: Inverted-T beams](https://crhconcrete.dk/betonelementer/produktsortiment/bjaelker/ot-bjaelker/) | `primary_web_source` | 0 |
| Dominican Republic | `do_conde` | [CONDE: Precast beams for bridges and elevated roads](https://www.conde.com.do/prefabricados.html) | `primary_search_index_lead` | 0 |
| Ecuador | `ec_mavisa` | [MAVISA S.A.: Precast and prestressed concrete products](https://mavisa.ec/) | `primary_web_source` | 1 |
| Ecuador | `ec_mtop` | [Ministerio de Transporte y Obras Públicas: Vicolinci Daule bridge tender documents](https://www.obraspublicas.gob.ec/wp-content/uploads/downloads/2012/08/19-12-2011_documentos_licitacion_puente_vicolinci_daule.pdf) | `download_blocked` | 0 |
| El Salvador | `sv_platinium` | [Platinium: Pretensioned and post-tensioned bridge girders](https://www.platinium.com.sv/) | `primary_web_source` | 0 |
| Estonia | `ee_viaplus` | [E-Betoonelement Consolis: ViaPlus bridges, tunnels, noise barriers](https://betoonelement.ee/lahendused/viaplus-infrastruktuur/) | `primary_web_source` | 0 |
| Finland | `fi_parma` | [Parma Consolis: Parma prestressed beam bridge, general arrangement](https://parma.fi/wp-content/uploads/2018/06/parma_jannepalkkisilta_yleispiirustus_2017.pdf) | `verified_partial_transcription` | 1 |
| France | `fr_prad` | [Sétra / Cerema: Road bridges with precast pretensioned girders: design guide](https://piles.cerema.fr/IMG/pdf/prad_-_ponts-routes_a_poutres_prefabriquees_precontraintes_par_adherence_-_guide_de_conception_-_1996_cle6a996f.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Georgia | `ge_roads` | [Roads Department of Georgia: Third East-West Highway Improvement Project additional-financing EIA](https://www.georoad.ge/uploads/files/TEWHIPAFEIA_1_Engl.pdf) | `primary_indexed_project_download_blocked` | 0 |
| Germany | `de_bt` | [Bauarchiv DDR / BBR: Construction indices: material quantities for precast-industry concrete production](https://bauarchivddr.bbr-server.de/bauarchivddr/archiv/plarchiv/00125-0105/akten-und-mappen-pdf/00125-0105-z8463kme.pdf) | `rejected_miscited_source` | 0 |
| Guatemala | `gt_benque` | [Dirección General de Caminos / SEGEPLAN: Benque Viejo bridge construction drawings, CA-9](https://sistemas.segeplan.gob.gt/share/SCHE%24SINIP/PLANOS_DISENOS/24234-HCGGZEXDNP.pdf) | `primary_indexed_drawing_download_blocked` | 0 |
| Guinea | `gn_jica` | [JICA / Guinea Ministry of Public Works: Preparatory survey for reconstruction of a bridge on National Road3 in Guinea](https://openjicareport.jica.go.jp/pdf/12323457_01.pdf) | `primary_project_alternatives_document` | 0 |
| Guyana | `gy_dpi` | [Department of Public Information / Ministry of Public Works: Demerara River Bridge precast-girder installation](https://dpi.gov.gy/first-precast-girder-installed-for-new-demerara-river-bridge/) | `primary_project_source` | 1 |
| Haiti | `ht_fauche` | [MTPTC / SNC-Lavalin International: Fauché bridge reconstruction resettlement plan and structural alternatives](https://www.mtptc.gouv.ht/media/upload/doc/publications/PAR_Fauch_FINAL_2011_10-13.pdf) | `primary_project_alternatives_document` | 0 |
| Hungary | `hu_fi150` | [Ferrobeton: FI-150 prestressed bridge girders](https://ferrobeton.hu/images/upload/content/1489/files/FI%20150.pdf) | `verified_partial_transcription` | 1 |
| Hungary | `hu_fp` | [Ferrobeton: FP bridge girder family](https://ferrobeton.hu/images/upload/content/1490/files/FP%20H%C3%8DDG.%20CSAL%C3%81D.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Hungary | `hu_fpt` | [Ferrobeton: FPT bridge girder family](https://ferrobeton.hu/images/upload/content/1492/files/FPT%20H%C3%8DDG.%20CSAL%C3%81D.pdf) | `verified_partial_transcription` | 7 |
| Hungary | `hu_itg` | [Ferrobeton: ITG prestressed bridge girder family](https://ferrobeton.hu/images/upload/content/1524/files/ITG%20H%C3%8DDG.%20CSAL%C3%81D0715.pdf) | `verified_partial_transcription` | 4 |
| Ireland | `ie_banagher` | [Banagher Precast Concrete: Bridge Beam Manual, 3rd Edition](https://files.brintex.com/Occurrence/291/Brochure/7518/brochure.pdf) | `inherited_local_source_verified` | 0 |
| Ireland | `ie_concast` | [Concast Precast Group: Civil brochure](http://concast.ie/wp-content/uploads/2020/03/Concast_Civil.pdf) | `inherited_local_source_verified` | 0 |
| Italy | `it_hp125` | [Paver: HP 125 constant section](https://www.paver.it/wp-content/uploads/2024/08/hp-125-sezione-filante.pdf) | `verified_partial_transcription` | 1 |
| Italy | `it_htp` | [Paver: HTP bridge beam](https://www.paver.it/wp-content/uploads/2024/08/htp.pdf) | `verified_partial_transcription` | 3 |
| Italy | `it_paver` | [Paver: Bridge beams](https://www.paver.it/wp-content/uploads/2024/08/paver-via_2021_travi-da-ponte.pdf) | `verified_partial_transcription` | 23 |
| Italy | `it_uhp250` | [Paver: UHP 250 constant section](https://www.paver.it/wp-content/uploads/2024/08/uhp-250-sezione-filante.pdf) | `verified_partial_transcription` | 7 |
| Kazakhstan | `kz_azmk_tbn` | [Almaty Bridge Structures Plant (AZMK): TBN bridge beam](https://www.azmk.kz/?cat=0&frame=product&item=71) | `primary_search_index_table` | 6 |
| Kazakhstan | `kz_azmk_vtk` | [Almaty Bridge Structures Plant (AZMK): VTK bridge beam 21, 24, 33 m](https://www.azmk.kz/?cat=0&frame=product&item=73) | `primary_search_index_table` | 3 |
| Kyrgyzstan | `kg_ministry_pm` | [Ministry of Construction / OAO Zavod ZHBI-4: Construction-material conformity-certificate register](https://minstroy.gov.kg/ru/building/materials/sertificate?direction=desc&page=168&sort=c.validtyPeriod) | `primary_authority_product_register` | 0 |
| Latvia | `lv_tilts` | [TILTS SIA: Reinforced concrete](https://www.tilts.lv/dzelzsbetons) | `primary_web_source` | 0 |
| Mexico | `mx_anippac` | [ANIPPAC: Product catalogue version 1.1 March 2022](https://anippac.org.mx/wp-content/uploads/2022/03/Catalogo-de-productos-ANIPPAC-Version-1.1-Mar-22.pdf) | `download_blocked` | 0 |
| Mexico | `mx_sepsa` | [SEPSA: Precast components catalogue](https://sepsacv.com.mx/wp-content/uploads/2022/02/CATALOGO-DE-PIEZAS-SEPSA-V-05-27-21.pdf) | `verified_partial_transcription` | 123 |
| Moldova | `md_asd` | [Administrația de Stat a Drumurilor: Bridge rehabilitation execution-design update, M5 km215+530: explanatory report](https://www.asd.md/storage/topic/thumbs/files/1.%2006-15_439.%20Volumul%201.%20Memoriu%20explicativ.pdf) | `verified_partial_transcription` | 1 |
| Montenegro | `me_bemax` | [Bemax: Precast girder installation, Mijakovići–Vrulja bridges](https://bemax.me/en/vijesti/the-installation-of-the-girders-on-the-bridge-on-the-mijakovici-vrulja-road-has-begun/) | `primary_project_source` | 1 |
| Netherlands | `nl_hip` | [Haitsma Beton: HRP and HIP bridge girders](https://www.haitsma.nl/media/241925/folder-hrp-hip.pdf) | `verified_partial_transcription` | 30 |
| Netherlands | `nl_hko` | [Haitsma Beton: HKO and HKO-XL slab girders](https://www.haitsma.nl/media/kbqasilf/hko-hko-xl-folder.pdf) | `verified_partial_transcription` | 20 |
| Nicaragua | `ni_total` | [Concretera Total: Precast concrete bridge projects](https://concreteratotal.com/proyectos-de-concreto-prefabricados/) | `verified_web_project_transcription` | 13 |
| North Macedonia | `mk_karpos` | [Fabrika Karpoš: Civil engineering](https://www.fabrikakarpos.com.mk/niskogradba/) | `primary_web_source` | 0 |
| Panama | `pa_pacadar` | [PACADAR: Bridges](https://pacadar.com/category/soluciones/puentes/) | `primary_web_source` | 0 |
| Paraguay | `py_covipa` | [COVIPA: Precast pretensioned girder bridge](https://covipa.com.py/portfolio/obra-puentes-consorcio-santa-lucia-ii/) | `web_access_blocked` | 0 |
| Peru | `pe_supermix` | [Supermix: Precast concrete products](https://www.supermix.com.pe/wp-content/uploads/2024/07/brochure-prefabricados-concreto.pdf) | `download_blocked` | 0 |
| Portugal | `pt_vigobloco` | [Vigobloco / APCER: Factory production control certificate annex](https://www.vigobloco.pt/uploads/base/ficheiros/6842f78929a7c932576145.pdf) | `download_blocked` | 0 |
| Romania | `ro_asa` | [ASA CONS Consolis: Product catalogue](https://asacons.ro/wp-content/uploads/2025/09/ASA-CONSOLIS-catalog.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Romania | `ro_somaco` | [Somaco: Precast elements for road infrastructure](https://www.somaco.ro/sites/somaco/files/docs/b-infrastructura-rutiera-somaco_2025_web_.pdf) | `verified_partial_transcription` | 21 |
| Russia | `ru_mgbk` | [АО Благовещенский завод МЖБК: Bridge girders](https://mgbkrb.ru/produkcziya-i-uslugi/mostovyie-balki.html) | `verified_web_table` | 46 |
| Serbia | `rs_raj` | [Raj Ibelik: Civil engineering](https://www.rajibelik.rs/niskogradnja) | `primary_web_source` | 0 |
| Slovakia | `sk_vph` | [VÁHOSTAV-PREFA: Bridge girder catalogue](https://vph.sk/assets/Uploads/ProduktPage/14/Katalog-mostnych-nosnikov.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Slovakia | `sk_vph_en` | [VÁHOSTAV-PREFA: Prestressed beams VPH PTMN](https://vph.sk/assets/Uploads/ProduktPage/14/PRESTRESSED-BEAMS-VPH-PTMN.pdf) | `verified_partial_transcription` | 20 |
| Spain | `es_hp1` | [BOE / Ministerio de Obras Públicas: HP-1 standard bridge collection (historic)](https://www.boe.es/boe/dias/1977/05/18/pdfs/A10886-10915.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Spain | `es_tierra` | [Tierra Armada / Geoquest: Prestressed Concrete Beams](https://www.geoquest-group.es/wp-content/uploads/sites/17/2023/12/F_Beams_May2012-4.pdf) | `downloaded_not_fully_transcribed` | 0 |
| Suriname | `sr_kuldipsingh` | [Kuldipsingh Total Concrete: Prestressed bridge-girder production](https://kuldipsingh.net/en/ruwbouw/pre-stressed-concrete/) | `primary_web_source` | 0 |
| Sweden | `se_abetong` | [Heidelberg Materials Precast Abetong: Precast bridges and tunnels](https://www.precastabetong.heidelbergmaterials.se/sv/prefabricerade_broar_tunnlar) | `primary_web_source` | 0 |
| Switzerland | `ch_fanger` | [Fanger Elementtechnik: Precast concrete elements from Obwalden](https://www.fanger.ch/) | `producer_lead_unverified_beam_family` | 0 |
| Trinidad and Tobago | `tt_prestcon` | [PRESTCON2021 Limited: Prestressed concrete bridge products](https://www.prestcon2021.com/) | `primary_web_source` | 0 |
| Ukraine | `ua_kovalska` | [Kovalska: Bridge beams/slabs](https://beton.kovalska.com/products/individual/balky-mostovi/) | `primary_web_source` | 0 |
| Ukraine | `ua_oberbeton` | [Oberbeton: Bridge beams](https://oberbeton.ua/uk/мостові-балки/) | `primary_web_source` | 0 |
| United Kingdom | `uk_banagher` | [Banagher Precast Concrete: Bridge Beam Manual, 3rd Edition](https://files.brintex.com/Occurrence/291/Brochure/7518/brochure.pdf) | `inherited_local_source_verified` | 0 |
| United States | `us_wsdot_deck` | [Washington State DOT: 5.6-A1-11 Prestressed Concrete Deck Girders](https://wsdot.wa.gov/publications/fulltext/Bridge/Web_BSD/5.6_A1_11.PDF) | `verified_partial_transcription_preliminary` | 27 |
| United States | `us_wsdot_iwf` | [Washington State DOT: 5.6-A1-10 Prestressed Concrete I and WF Girders](https://wsdot.wa.gov/publications/fulltext/Bridge/Web_BSD/5.6_A1_10.PDF) | `verified_partial_transcription` | 13 |
| United States | `us_wsdot_tub` | [Washington State DOT: 5.6-A1-13 Prestressed Concrete Tub Girders](https://wsdot.wa.gov/publications/fulltext/Bridge/Web_BSD/5.6_A1_13.PDF) | `verified_partial_transcription_preliminary` | 8 |
| Uruguay | `uy_schmidt` | [Schmidt Premoldeados: Products](https://www.schmidt.com.uy/productos/) | `primary_web_source` | 0 |
| Uzbekistan | `uz_road_committee` | [Committee for Roads, Uzbekistan: Kuylyuk experimental bridge reinforced-concrete structures plant](https://www.uzavtoyul.uz/ru/post/qoyliq-tbktzk.html) | `primary_authority_producer_identity` | 0 |
| Venezuela | `ve_pilperca` | [PILPERCA: Second bridge over the Chama River and associated precast-beam bridges](https://pilperca.com/proyecto/segundo-puente-sobre-el-rio-chama/) | `primary_project_source` | 0 |

## Additional searched countries and rejected distractions

Native-language passes also covered Lithuania, Uzbekistan, Slovenia, Costa Rica and Bolivia. These are **searched gaps**, not claims that bridge beams are absent:

- **Lithuania:** government Rail Baltica design material indexes precast beam arrangements and drawingRBDG-DWG-072-A4, but individual beam outlines were not recovered. Betonika SI/I and RTL/RLL hits describe building/roof beams, so they were not entered as verified bridge sections.
- **Uzbekistan:** the official standards catalogue at https://www.standart.uz/upload/file/katalojniiy_list.pdf identifies the Kuylyuk experimental bridge-concrete plant and12-33 m bridge I girders. The current catalogue download fails DNS resolution; a Roads Committee page now verifies the specialised plant identity, but dimension sheets remain unavailable.
- **Slovenia:** Pomgrad ABI catalogue https://abi.pomgrad.si/docs/ABI_KATALOG_25_julij_2025.pdf yields building/roof IN/TN beams; no bridge application was verified for those sections. Retain as a rejected scope match, not a country beam family.
- **Costa Rica:** the initial PC search returned masonry/floor products; the final pass recovered a bridge-specific PuentePrefa source, now registered with its 4–40 m span envelope.
- **Bolivia:** Pretenbol hits concern building floor joists; excluded from bridge-beam counts.
- **Russia:** the initial series3.503.1-81 search yielded mirrors/resellers. The final pass recovered the actual Blagoveshchensk MZhBK producer table: 46 length/width/depth/volume rows, registered separately. It supplies envelopes, not full outlines; duplicate designation/volume conflicts remain explicit.
- **Germany:** modern Max Bögl searches largely resolve to steel-concrete composite girders, outside this concrete-only section scope. The inherited archive link is explicitly rejected above.


## Final geographic-gap pass

The final bounded pass checked all additional jurisdictions requested by the parent task. It adds **20 source records, 19 country codes and 65 dimension/property rows** to the earlier 57/40/329 snapshot. New country coverage includes primary project evidence and expressly labelled indexed/download-blocked leads; it must not be read as 19 new fully dimensioned families. Guinea is a cross-regional primary project study, coordinated with the Africa pass to avoid a duplicate.

The most useful dimensional additions are the Russian producer’s 46 envelope/volume rows, Nicaragua’s 13 project member length/mass records, Moldova’s existing 21.0 m long × 1.2 m deep girder with 1.4 m reduced slab width, and Guyana’s 42 m / approximately 120 t project member. Armenia supplies a 28 m maximum production length; Costa Rica a 4–40 m bridge-span range; Ecuador collectively lists 16/20/30/40/50/60 m lengths for Doble-T/California/Bulb-T families. Montenegro reports length and mass lists without an explicitly verified pairing. These are not cross-section polygons.

Additional successful bridge-specific leads are Belize M&M, Dominican Republic CONDE, Suriname Kuldipsingh, El Salvador Platinium, Trinidad and Tobago PRESTCON, Uzbekistan’s Kuylyuk factory identity, Venezuela PILPERCA’s two ancillary precast-beam bridges, Kyrgyzstan’s registered PM bridge slabs, and official project documents for Guatemala, Georgia and Haiti. Records say when evidence is only indexed, certification is expired, or a structural solution is merely an alternative.

The following searches did not recover a usable primary dimensioned concrete bridge-beam source in this pass:

| Jurisdiction | Search outcome / specific remaining gap |
|---|---|
| Honduras | Regional supplier hits and a Platinium El Poy border-project social post; no independent Honduran producer/authority dimension sheet recovered. |
| Cuba | TRB/TRID identifies MICONS RC-3093 (1981), *Structures: precast bridges; erection of road-bridge beams*. Only a bibliographic record was recovered, not the issuing ministry’s document or dimensions: https://trid.trb.org/View/949799 . |
| Jamaica | Official 2023 budget presentation lists proposed precast prestressed bridge solutions, but no beam section family/drawing: https://jis.gov.jm/media/2023/06/Budget-Presentation_Everald-Warmington-Wed-May-31-2023.pdf . |
| Bolivia | Searches returned academic bridge designs and building-joist suppliers; no primary bridge-girder product sheet recovered. |
| Luxembourg | Authority historical technical review includes precast cantilever widening beams; current product hits were building members or composite steel girders. A longitudinal concrete bridge-beam section source remains unverified. |
| Iceland | Road-authority concrete-material guidance and ÍST EN15050 product-standard listing recovered; neither establishes a dimensioned beam family. |
| Albania | APM brochure was downloaded and inspected: its bridge-girder production is **steel**, so it is excluded. IXHEM page establishes building precast activity but not bridge-beam profiles. |
| Azerbaijan | AZSTAND draft AZS EN15050:2025 explanatory document concerns bridge precast products generally; no product geometry. Draft standards are not national beam families. |
| Tajikistan | Technical-university paper mentions Dushanbe production of 18/33 m prestressed T beams, but it is not a producer/authority catalogue. Crane end-beam sales were rejected as out of scope. |

Two geographic/source errors were prevented: Albania APM’s steel brochure is not counted as a concrete source; JICA document12323457_01 is **Guinea**, verified from its title page, despite appearing in a Haiti search. It is saved as `sources/expansion/europe-americas/gn_jica.pdf`. Haiti has a separate MTPTC Fauché options document. No country’s lack of a national catalogue is inferred from these search outcomes.

## Remaining productive work

1. SEPSA p4 implementation is complete: all seven producer profiles reproduce published areas within the 50 mm² source rounding limit. Targeted tests passed (10 tests); downstream exports and documentation are integrated by the parent task. SEPSA box tables on pp 6–9 are now transcribed; rounded profiles still need reconstruction and validation.
2. Digitise VÁHOSTAV rounded cross-section profiles against published area/centroid/inertia; distinguish PM edge/interior and2010/2016 designs.
3. Extract Haitsma topologies and independently check published rounding. The HIP wet-joint and topping profiles cannot share one polygon with only a height change.
4. Read ASA Consolis pp 97/99 visually for Romanian42/52/72/80 cm profiles, then compare to Somaco only after geometry compatibility is established.
5. Paver IHP/THP/VHP/BOX envelope transcription is complete for the reviewed brochure. Obtain missing wall/flange dimensions and resolve the listed source conflicts before polygon implementation.
6. Recover actual German BT500/700 drawings from catalogue metadata, then continue historic FinnishJbe drawing-series recovery. Existing general arrangements and misplaced archive documents do not resolve these gaps.
7. Revisit blocked downloads using their primary landing pages. No authentication bypass, purchase, or unsolicited producer contact was attempted.

## Verification and provenance

Every successfully captured PDF is opened with PyMuPDF to verify it is a parseable PDF and record page count, byte size and SHA-256. Extracted page text is saved separately. Selected image-only pages and table layouts are rendered and visually inspected. JSON dimension keys carry their units; `pdf_page` is 1-based. Geometry validation is a separate downstream task, except where an implemented family and its tests are explicitly reported elsewhere. No national-catalogue nonexistence, copyright permission, code compliance or engineering approval is inferred from search results.
