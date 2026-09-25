"""bridgebeams: standard precast/prestressed bridge beam sections for use
with the ``sectionproperties`` package.

.. warning::
   Not authoritative. See :data:`bridgebeams.DISCLAIMER`; check each
   profile's ``provenance`` and ``source_status`` before use.

Subpackages
-----------
- ``bridgebeams.aus``: Australian Super-T and I-girders to AS5100.5 App. D.
- ``bridgebeams.ie``: Irish producer precast beams (T, Y and YE
  families).

All geometry is in millimetres and returned as ``sectionproperties``
``Geometry`` objects, so sections feed directly into ``sectionproperties``
analysis and into ``concreteproperties``/``PyBridge`` by adding materials.
Adapters in :mod:`bridgebeams.adapters` provide one-call bridges to
``concreteproperties`` sections and ``ospgrillage`` section properties.
"""

from bridgebeams.adapters import osp_grillage_properties, to_concreteproperties
from bridgebeams.aus import IGirderSection, SuperTGirderSection
from bridgebeams.be import FebeIDimensions, FebeISection
from bridgebeams.gr import GrExtendedISection, depth_law as gr_depth_law, web_width as gr_web_width
from bridgebeams.india import Nh45aPscIDimensions, Nh45aPscISection
from bridgebeams.pl import MostostalTDimensions, MostostalTSection
from bridgebeams.jp import JisTGirderDimensions, JisTGirderSection
from bridgebeams.kr import KhcIGirderDimensions, KhcISection
from bridgebeams.mx import SepsaIGirderDimensions, SepsaIGirderSection
from bridgebeams.nz import (
    NzIBeamDimensions, NzIBeamSection, NzSuperTDimensions, NzSuperTSection,
    NzHollowCoreDimensions, NzHollowCoreSection,
)
from bridgebeams.no import NoNtbKtbDimensions, NoNtbKtbSection
from bridgebeams.qa import QaQBeamDimensions, QaQBeamSection
from bridgebeams.ru import Su3503I33Dimensions, Su3503I33Section
from bridgebeams.th import ThDOHIGirderDimensions, ThDOHIGirderSection
from bridgebeams.tr import KGMIDimensions, KGMISection
from bridgebeams.tw import TaiwanIDimensions, TaiwanISection
from bridgebeams.za import (
    CivilconIBeamDimensions, CivilconIBeamSection,
    CivilconYBeamDimensions, CivilconYBeamSection,
)
from bridgebeams.us import AashtoIBeamDimensions, AashtoIBeamSection
from bridgebeams.ie import (
    IeWBeamDimensions,
    IeWBeamSection,
    IeSolidBoxBeamDimensions,
    IeSolidBoxBeamSection,
    IeTBeamDimensions,
    IeTBeamSection,
    IeYBeamDimensions,
    IeYBeamSection,
    IeYEBeamDimensions,
    IeYEBeamSection,
    strand_locations,
    wf_of_depth,
)

from bridgebeams.ca import (
    CaMtoBoxGirderDimensions, CaMtoBoxGirderSection,
    CaMtoNuGirderDimensions, CaMtoNuGirderSection,
)
from bridgebeams.cn import Beijing20bgql2BoxDimensions, Beijing20bgql2BoxSection
from bridgebeams.es import Hp1BeamDimensions, Hp1BeamSection
from bridgebeams.hu import (
    FerrobetonFi150Dimensions, FerrobetonFi150Section,
    FerrobetonFpDimensions, FerrobetonFpSection,
    FerrobetonFpt7050Dimensions, FerrobetonFptDimensions, FerrobetonFptSection,
    FerrobetonItgDimensions, FerrobetonItgSection,
)
from bridgebeams.id import (
    WikaBulbTeeSection, WikaChannelGirderSection, WikaGirderDimensions,
    WikaPcIGirderSection, WikaPcUGirderSection,
)
from bridgebeams.india import DelhiVadodaraPscISection, Nh45aIGirderSection, NhaiIGirderDimensions
from bridgebeams.mx import (
    SepsaBoxDimensions, SepsaBoxGirderSection,
    SepsaDoubleTeeDimensions, SepsaDoubleTeeSection,
    SepsaNebraskaDimensions, SepsaNebraskaSection,
)
from bridgebeams.nl import (
    HaitsmaHipDimensions, HaitsmaHipSection, HaitsmaHkoDimensions, HaitsmaHkoSection,
    HaitsmaHkoXlDimensions, HaitsmaHkoXlSection, HaitsmaHrpDimensions, HaitsmaHrpSection,
)
from bridgebeams.np import DorPrecastRcIDimensions, DorPrecastRcISection
from bridgebeams.ro import AsaGrindaPodDimensions, AsaGrindaPodSection
from bridgebeams.sk import (
    VphGirderDimensions, VphGirderSection, VphSlabBeamDimensions, VphSlabBeamSection,
)
from bridgebeams.us import (
    WsdotBulbTeeDimensions, WsdotBulbTeeSection,
    WsdotDeckBulbTeeDimensions, WsdotDeckBulbTeeSection,
    WsdotSlabDimensions, WsdotSlabGirderSection,
    WsdotTubDimensions, WsdotTubGirderSection,
    WsdotWfDimensions, WsdotWfGirderSection,
)
from bridgebeams.za import (
    CivilconMBeamDimensions, CivilconMBeamSection,
    CivilconSpecialUBeamDimensions, CivilconSpecialUBeamSection,
    CivilconTBeamDimensions, CivilconTBeamSection,
    CivilconUBeamDimensions, CivilconUBeamSection,
)

from bridgebeams.us.fdot_girders import FdotFloridaIBeamDimensions
from bridgebeams.us.fdot_girders import FdotFloridaIBeamSection
from bridgebeams.us.fdot_girders import FdotFloridaSlabBeamDimensions
from bridgebeams.us.fdot_girders import FdotFloridaSlabBeamSection
from bridgebeams.us.fdot_girders import FdotFloridaUBeamDimensions
from bridgebeams.us.fdot_girders import FdotFloridaUBeamSection
from bridgebeams.us.pci_regional_products import PciNeBulbTeeDimensions
from bridgebeams.us.pci_regional_products import PciNeBulbTeeSection
from bridgebeams.us.pci_regional_products import PciNeDeckBulbTeeDimensions
from bridgebeams.us.pci_regional_products import PciNeDeckBulbTeeSection
from bridgebeams.us.pci_regional_products import PciNextBeamDimensions
from bridgebeams.us.pci_regional_products import PciNextBeamSection
from bridgebeams.us.pci_regional_products import PciZone6UGirderDimensions
from bridgebeams.us.pci_regional_products import PciZone6UGirderSection
from bridgebeams.us.pci_standard_products import PciBoxBeamDimensions
from bridgebeams.us.pci_standard_products import PciBoxBeamSection
from bridgebeams.us.pci_standard_products import PciBulbTeeDimensions
from bridgebeams.us.pci_standard_products import PciBulbTeeSection
from bridgebeams.us.pci_standard_products import PciDeckBulbTeeDimensions
from bridgebeams.us.pci_standard_products import PciDeckBulbTeeSection
from bridgebeams.us.pci_standard_products import PciDoubleTeeDimensions
from bridgebeams.us.pci_standard_products import PciDoubleTeeSection
from bridgebeams.us.pci_standard_products import PciSlabBeamDimensions
from bridgebeams.us.pci_standard_products import PciSlabBeamSection
from bridgebeams.us.state_ca_girders import CaBathTubDimensions
from bridgebeams.us.state_ca_girders import CaBathTubSection
from bridgebeams.us.state_ca_girders import CaBulbTeeSection
from bridgebeams.us.state_ca_girders import CaGirderDimensions
from bridgebeams.us.state_ca_girders import CaIGirderSection
from bridgebeams.us.state_ca_girders import CaVoidedSlabDimensions
from bridgebeams.us.state_ca_girders import CaVoidedSlabSection
from bridgebeams.us.state_ca_girders import CaWideFlangeSection
from bridgebeams.us.state_co_cbt import CoCbtDimensions
from bridgebeams.us.state_co_cbt import CoCbtGirderSection
from bridgebeams.us.state_ia_beams import IaBeamDimensions
from bridgebeams.us.state_ia_beams import IaBulbTeeSection
from bridgebeams.us.state_ia_beams import IaIBeamSection
from bridgebeams.us.state_il_deck_beams import IlDeckBeamDimensions
from bridgebeams.us.state_il_deck_beams import IlDeckBeamSection
from bridgebeams.us.state_mo_girders import MoDotIGirderDimensions
from bridgebeams.us.state_mo_girders import MoDotIGirderSection
from bridgebeams.us.state_mo_girders import MoDotNuDimensions
from bridgebeams.us.state_mo_girders import MoDotNuGirderSection
from bridgebeams.us.state_mo_slabs_boxes import MoDotBoxBeamSection
from bridgebeams.us.state_mo_slabs_boxes import MoDotBoxDimensions
from bridgebeams.us.state_mo_slabs_boxes import MoDotSolidSlabDimensions
from bridgebeams.us.state_mo_slabs_boxes import MoDotSolidSlabSection
from bridgebeams.us.state_mo_slabs_boxes import MoDotVoidedSlabDimensions
from bridgebeams.us.state_mo_slabs_boxes import MoDotVoidedSlabSection
from bridgebeams.us.state_ne_nu import NeNuGirderDimensions
from bridgebeams.us.state_ne_nu import NeNuGirderSection
from bridgebeams.us.state_ny_beams import NyBoxBeamSection
from bridgebeams.us.state_ny_beams import NyGirderDimensions
from bridgebeams.us.state_ny_beams import NyPcefBulbTeeSection
from bridgebeams.us.state_ny_beams import NySlabUnitSection
from bridgebeams.us.state_ny_beams import NyUnitDimensions
from bridgebeams.us.state_or_girders import OrBoxDimensions
from bridgebeams.us.state_or_girders import OrBoxSection
from bridgebeams.us.state_or_girders import OrIGirderDimensions
from bridgebeams.us.state_or_girders import OrIGirderSection
from bridgebeams.us.state_or_girders import OrSlabDimensions
from bridgebeams.us.state_or_girders import OrSlabSection
from bridgebeams.us.state_pa_beams import PaAashtoIBeamSection
from bridgebeams.us.state_pa_beams import PaBeamDimensions
from bridgebeams.us.state_pa_beams import PaBoxBeamDimensions
from bridgebeams.us.state_pa_beams import PaBoxBeamSection
from bridgebeams.us.state_pa_beams import PaBulbTeeSection
from bridgebeams.us.state_pa_beams import PaIBeamSection
from bridgebeams.us.state_va_girders import VaBoxBeamDimensions
from bridgebeams.us.state_va_girders import VaBoxBeamSection
from bridgebeams.us.state_va_girders import VaPcbtDimensions
from bridgebeams.us.state_va_girders import VaPcbtSection
from bridgebeams.us.state_va_girders import VaVoidedSlabDimensions
from bridgebeams.us.state_va_girders import VaVoidedSlabSection
from bridgebeams.us.state_wi_girders import WiBoxGirderDimensions
from bridgebeams.us.state_wi_girders import WiBoxGirderSection
from bridgebeams.us.state_wi_girders import WiGirderDimensions
from bridgebeams.us.state_wi_girders import WiGirderSection
from bridgebeams.us.txdot_girders import TxDotDoubleTSection
from bridgebeams.us.txdot_girders import TxDotGirderDimensions
from bridgebeams.us.txdot_girders import TxDotIGirderSection
from bridgebeams.us.txdot_girders import TxDotLegacyIBeamSection
from bridgebeams.us.txdot_girders import TxDotUBeamSection
from bridgebeams.us.txdot_girders import TxDotWideFlangeGirderSection
from bridgebeams.us.txdot_slabs_boxes import TxDotBoxBeamSection
from bridgebeams.us.txdot_slabs_boxes import TxDotDeckedSlabBeamSection
from bridgebeams.us.txdot_slabs_boxes import TxDotSlabBeamSection
from bridgebeams.us.txdot_slabs_boxes import TxDotSlabBoxDimensions
from bridgebeams.us.txdot_slabs_boxes import TxDotXBeamSection
from bridgebeams.qa.r2_ty_beams import QaTyBeamDimensions
from bridgebeams.qa.r2_ty_beams import QaTyBeamSection
from bridgebeams.qa.r2_ty_beams import QaTyeBeamSection
from bridgebeams.kr.r2_improved_psc_beam import ImprovedPscBeamDimensions
from bridgebeams.kr.r2_improved_psc_beam import ImprovedPscBeamSection
from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiHingedHollowSlabDimensions
from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiHingedHollowSlabSection
from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiRigidHollowSlabDimensions
from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiRigidHollowSlabSection
from bridgebeams.jp.r2_bipre_girders import BipreHollowGirderDimensions
from bridgebeams.jp.r2_bipre_girders import BipreHollowGirderSection
from bridgebeams.jp.r2_bipre_girders import BipreIGirderDimensions
from bridgebeams.jp.r2_bipre_girders import BipreIGirderSection
from bridgebeams.jp.r2_jis_slab_girders import JisSlabGirderDimensions
from bridgebeams.jp.r2_jis_slab_girders import JisSlabGirderSection
from bridgebeams.tw.r2_thb_pci_girders import ThbPciGirderDimensions
from bridgebeams.tw.r2_thb_pci_girders import ThbPciGirderSection
from bridgebeams.th.r2_doh_girders import ThDohBoxBeamDimensions
from bridgebeams.th.r2_doh_girders import ThDohBoxBeamSection
from bridgebeams.th.r2_doh_girders import ThDohIGirderR2Dimensions
from bridgebeams.th.r2_doh_girders import ThDohIGirderR2Section
from bridgebeams.th.r2_doh_girders import ThDohPlankDimensions
from bridgebeams.th.r2_doh_girders import ThDohPlankGirderSection
from bridgebeams.id.r2_waskita import WaskitaPcIDimensions
from bridgebeams.id.r2_waskita import WaskitaPcIGirderSection
from bridgebeams.id.r2_waskita import WaskitaVoidedSlabDimensions
from bridgebeams.id.r2_waskita import WaskitaVoidedSlabSection
from bridgebeams.id.r2_wika_voided_slab import WikaVoidedSlabDimensions
from bridgebeams.id.r2_wika_voided_slab import WikaVoidedSlabSection
from bridgebeams.aus.r2_tfnsw_cbs_modules import TfnswCbsModuleDimensions
from bridgebeams.aus.r2_tfnsw_cbs_modules import TfnswCbsModuleSection
from bridgebeams.aus.r2_tmr_deck_units import TmrDeckUnitDimensions
from bridgebeams.aus.r2_tmr_deck_units import TmrDeckUnitSection
from bridgebeams.vn.c620_girders import Vn620GirderDimensions
from bridgebeams.vn.c620_girders import Vn620GirderSection
from bridgebeams.kh.vong_scc_girder import KhVongGirderDimensions
from bridgebeams.kh.vong_scc_girder import KhVongGirderSection
from bridgebeams.my.gcast_beams import GcastIBeamSection
from bridgebeams.my.gcast_beams import GcastTBeamSection
from bridgebeams.my.gcast_beams import GcastTmBeamDimensions
from bridgebeams.my.gcast_beams import GcastTmBeamSection
from bridgebeams.my.gcast_beams import GcastUBeamDimensions
from bridgebeams.my.gcast_beams import GcastUBeamSection
from bridgebeams.my.jkr_prt import JkrPrtBeamSection
from bridgebeams.my.jkr_prt import JkrPrtDimensions
from bridgebeams.my.oka_m_beam import OkaMBeamDimensions
from bridgebeams.my.oka_m_beam import OkaMBeamSection
from bridgebeams.pk.nha_i_girders import LsmPscIGirderSection
from bridgebeams.pk.nha_i_girders import NhaStandardIGirderSection
from bridgebeams.lk.rda_beams import RdaTB505BeamSection
from bridgebeams.lk.rda_beams import RdaTB505Dimensions
from bridgebeams.bd.jica_pc_i import JicaPcIDimensions
from bridgebeams.bd.jica_pc_i import JicaPcIGirderSection
from bridgebeams.ma.sadet_i_beams import SadetIBeamDimensions
from bridgebeams.ma.sadet_i_beams import SadetIBeamSection

from bridgebeams.pl.r2_pekabex_mg_t import PekabexMgtDimensions
from bridgebeams.pl.r2_pekabex_mg_t import PekabexMgtSection
from bridgebeams.ro.r2_somaco import SomacoGirderDimensions
from bridgebeams.ro.r2_somaco import SomacoGirderSection
from bridgebeams.ro.r2_prebet import PrebetGirderDimensions
from bridgebeams.ro.r2_prebet import PrebetGirderSection
from bridgebeams.es.r2_tierra import TierraBeamDimensions
from bridgebeams.es.r2_tierra import TierraBeamSection
from bridgebeams.es.r2_prethor import PrethorBeamDimensions
from bridgebeams.es.r2_prethor import PrethorVaSection
from bridgebeams.es.r2_prethor import PrethorVaaSection
from bridgebeams.es.r2_prethor import PrethorVcSection
from bridgebeams.es.r2_prethor import PrethorViSection
from bridgebeams.es.r2_prethor import PrethorVuSection
from bridgebeams.nl.r2_haitsma import HaitsmaHbmDimensions
from bridgebeams.nl.r2_haitsma import HaitsmaHbmSection
from bridgebeams.nl.r2_haitsma import HaitsmaHgrDimensions
from bridgebeams.nl.r2_haitsma import HaitsmaHgrSection
from bridgebeams.nl.r2_haitsma import HaitsmaHkpDimensions
from bridgebeams.nl.r2_haitsma import HaitsmaHkpSection
from bridgebeams.nl.r2_spanbeton import SpanbetonPiqDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonPiqSection
from bridgebeams.nl.r2_spanbeton import SpanbetonSjpDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonSjpFlexDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonSjpFlexSection
from bridgebeams.nl.r2_spanbeton import SpanbetonSjpSection
from bridgebeams.nl.r2_spanbeton import SpanbetonSkkDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonSkkSection
from bridgebeams.nl.r2_spanbeton import SpanbetonSrpDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonSrpSection
from bridgebeams.nl.r2_spanbeton import SpanbetonZipDimensions
from bridgebeams.nl.r2_spanbeton import SpanbetonZipSection
from bridgebeams.nl.r2_spanbeton import SpanbetonZipxlSection
from bridgebeams.gr.r2_projects import GrProjectGirderDimensions
from bridgebeams.gr.r2_projects import GrProjectGirderSection
from bridgebeams.uk.r2_fpmccann import FpMcCannBoxBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannBoxBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannMyBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannMyBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannMyeBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannSyBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannSyBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannTyBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannTyBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannTyeBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannWBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannWBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannYBeamDimensions
from bridgebeams.uk.r2_fpmccann import FpMcCannYBeamSection
from bridgebeams.uk.r2_fpmccann import FpMcCannYeBeamSection
from bridgebeams.hu.r2_sw_shp import SwShpDimensions
from bridgebeams.hu.r2_sw_shp import SwShpSection
from bridgebeams.tr.r2_itu_tip import ItuTipBeamDimensions
from bridgebeams.tr.r2_itu_tip import ItuTipBeamSection
from bridgebeams.ru.r2_su3503_b12 import Su3503B12Dimensions
from bridgebeams.ru.r2_su3503_b12 import Su3503B12Section
from bridgebeams.mx.r2_producer_aashto import DragonAashtoSection
from bridgebeams.mx.r2_producer_aashto import R2AashtoIDimensions
from bridgebeams.mx.r2_producer_aashto import TubecoAashtoSection
from bridgebeams.it.paver import PaverBeamDimensions
from bridgebeams.it.paver import PaverBeamSection
from bridgebeams.fr.afgc_vipp import AfgcVippBeamSection
from bridgebeams.fr.afgc_vipp import AfgcVippDimensions
from bridgebeams.dk.crh_ot import CrhOtBeamSection
from bridgebeams.dk.crh_ot import CrhOtDimensions
from bridgebeams.ua.i_beams import ThreeBetBeamSection
from bridgebeams.ua.i_beams import UaB40BeamSection
from bridgebeams.ua.i_beams import UaBeamDimensions
from bridgebeams.ua.i_beams import UaBmBeamSection
from bridgebeams.bg.rila_gt import RilaGtDimensions
from bridgebeams.bg.rila_gt import RilaGtSection
from bridgebeams.bg.zbe_mg import ZbeMgDimensions
from bridgebeams.bg.zbe_mg import ZbeMgSection
from bridgebeams.lt.tilsta import TilstaSijaDimensions
from bridgebeams.lt.tilsta import TilstaSijaSection
from bridgebeams.hr.viadukt_san import ViaduktSanDimensions
from bridgebeams.hr.viadukt_san import ViaduktSanSection
from bridgebeams.br.dnit_pcp import DnitPcpLongarinaDimensions
from bridgebeams.br.dnit_pcp import DnitPcpLongarinaSection
from bridgebeams.ar.pretensa import PretensaViDimensions
from bridgebeams.ar.pretensa import PretensaViSection
from bridgebeams.cr.puenteprefa import PuentePrefaBeamDimensions
from bridgebeams.cr.puenteprefa import PuentePrefaBeamSection

from bridgebeams.us.state_r3_or_deck_bulb_tee import OrDeckBulbTeeDimensions
from bridgebeams.us.state_r3_or_deck_bulb_tee import OrDeckBulbTeeSection
from bridgebeams.us.state_r3_oh_i_beams import OhAashtoIBeamSection
from bridgebeams.us.state_r3_oh_i_beams import OhIBeamDimensions
from bridgebeams.us.state_r3_oh_i_beams import OhWfBeamSection
from bridgebeams.br.r3_ifes_sao_domingos import SaoDomingosLongarinaDimensions
from bridgebeams.br.r3_ifes_sao_domingos import SaoDomingosLongarinaSection
from bridgebeams.cl.mop_mc_v4 import MopLosaNervadaVigaDimensions
from bridgebeams.cl.mop_mc_v4 import MopLosaNervadaVigaSection
from bridgebeams.cl.mop_mc_v4 import MopVigaPostensadaDimensions
from bridgebeams.cl.mop_mc_v4 import MopVigaPostensadaSection

from bridgebeams.us.state_r3_mi_beams import MiBoxBeamDimensions
from bridgebeams.us.state_r3_mi_beams import MiBulbTeeDimensions
from bridgebeams.us.state_r3_mi_beams import MiBulbTeeSection
from bridgebeams.us.state_r3_mi_beams import MiSideBySideBoxBeamSection
from bridgebeams.us.state_r3_mi_beams import MiSpreadBoxBeamSection
from bridgebeams.ph.dpwh_aashto import PhDpwhAashtoDimensions
from bridgebeams.ph.dpwh_aashto import PhDpwhAashtoSection

DISCLAIMER = (
    "Not authoritative. bridgebeams is a best-effort, development-stage research catalogue. Many profiles are reconstructions or estimates from incomplete, draft or historic sources, and some sources contradict themselves. Check every profile's `provenance` and `source_status` and verify dimensions against the governing drawing before any design, assessment or procurement use. No warranty; the authors accept no liability."
)
"""Short usage disclaimer; see the documentation's *Disclaimer* page."""

__version__ = "0.3.0"

__all__ = [
    "IGirderSection",
    "SuperTGirderSection",
    "KGMIDimensions",
    "KGMISection",
    "ThDOHIGirderDimensions",
    "ThDOHIGirderSection",
    "JisTGirderDimensions",
    "JisTGirderSection",
    "KhcIGirderDimensions",
    "KhcISection",
    "SepsaIGirderDimensions",
    "SepsaIGirderSection",
    "TaiwanIDimensions",
    "TaiwanISection",
    "NzSuperTDimensions",
    "NzSuperTSection",
    "NzIBeamDimensions",
    "NzIBeamSection",
    "NzHollowCoreDimensions",
    "NzHollowCoreSection",
    "NoNtbKtbDimensions",
    "NoNtbKtbSection",
    "QaQBeamDimensions",
    "QaQBeamSection",
    "GrExtendedISection",
    "gr_depth_law",
    "gr_web_width",
    "FebeIDimensions",
    "FebeISection",
    "Nh45aPscIDimensions",
    "Nh45aPscISection",
    "MostostalTDimensions",
    "MostostalTSection",
    "Su3503I33Dimensions",
    "Su3503I33Section",
    "CivilconIBeamDimensions",
    "CivilconIBeamSection",
    "CivilconYBeamDimensions",
    "CivilconYBeamSection",
    "IeTBeamDimensions",
    "IeTBeamSection",
    "IeSolidBoxBeamDimensions",
    "IeSolidBoxBeamSection",
    "IeWBeamDimensions",
    "IeWBeamSection",
    "IeYBeamDimensions",
    "IeYBeamSection",
    "IeYEBeamDimensions",
    "IeYEBeamSection",
    "AashtoIBeamDimensions",
    "AashtoIBeamSection",
    "CaMtoBoxGirderDimensions",
    "CaMtoBoxGirderSection",
    "CaMtoNuGirderDimensions",
    "CaMtoNuGirderSection",
    "Beijing20bgql2BoxDimensions",
    "Beijing20bgql2BoxSection",
    "Hp1BeamDimensions",
    "Hp1BeamSection",
    "FerrobetonFi150Dimensions",
    "FerrobetonFi150Section",
    "FerrobetonFpDimensions",
    "FerrobetonFpSection",
    "FerrobetonFpt7050Dimensions",
    "FerrobetonFptDimensions",
    "FerrobetonFptSection",
    "FerrobetonItgDimensions",
    "FerrobetonItgSection",
    "WikaBulbTeeSection",
    "WikaChannelGirderSection",
    "WikaGirderDimensions",
    "WikaPcIGirderSection",
    "WikaPcUGirderSection",
    "DelhiVadodaraPscISection",
    "Nh45aIGirderSection",
    "NhaiIGirderDimensions",
    "SepsaBoxDimensions",
    "SepsaBoxGirderSection",
    "SepsaDoubleTeeDimensions",
    "SepsaDoubleTeeSection",
    "SepsaNebraskaDimensions",
    "SepsaNebraskaSection",
    "HaitsmaHipDimensions",
    "HaitsmaHipSection",
    "HaitsmaHkoDimensions",
    "HaitsmaHkoSection",
    "HaitsmaHkoXlDimensions",
    "HaitsmaHkoXlSection",
    "HaitsmaHrpDimensions",
    "HaitsmaHrpSection",
    "DorPrecastRcIDimensions",
    "DorPrecastRcISection",
    "AsaGrindaPodDimensions",
    "AsaGrindaPodSection",
    "VphGirderDimensions",
    "VphGirderSection",
    "VphSlabBeamDimensions",
    "VphSlabBeamSection",
    "WsdotBulbTeeDimensions",
    "WsdotBulbTeeSection",
    "WsdotDeckBulbTeeDimensions",
    "WsdotDeckBulbTeeSection",
    "WsdotSlabDimensions",
    "WsdotSlabGirderSection",
    "WsdotTubDimensions",
    "WsdotTubGirderSection",
    "WsdotWfDimensions",
    "WsdotWfGirderSection",
    "CivilconMBeamDimensions",
    "CivilconMBeamSection",
    "CivilconSpecialUBeamDimensions",
    "CivilconSpecialUBeamSection",
    "CivilconTBeamDimensions",
    "CivilconTBeamSection",
    "CivilconUBeamDimensions",
    "CivilconUBeamSection",
    "strand_locations",
    "wf_of_depth",
    "to_concreteproperties",
    "osp_grillage_properties",
    "DISCLAIMER",
    "__version__",
]

__all__ += ['FdotFloridaIBeamDimensions', 'FdotFloridaIBeamSection', 'FdotFloridaSlabBeamDimensions', 'FdotFloridaSlabBeamSection', 'FdotFloridaUBeamDimensions', 'FdotFloridaUBeamSection', 'PciNeBulbTeeDimensions', 'PciNeBulbTeeSection', 'PciNeDeckBulbTeeDimensions', 'PciNeDeckBulbTeeSection', 'PciNextBeamDimensions', 'PciNextBeamSection', 'PciZone6UGirderDimensions', 'PciZone6UGirderSection', 'PciBoxBeamDimensions', 'PciBoxBeamSection', 'PciBulbTeeDimensions', 'PciBulbTeeSection', 'PciDeckBulbTeeDimensions', 'PciDeckBulbTeeSection', 'PciDoubleTeeDimensions', 'PciDoubleTeeSection', 'PciSlabBeamDimensions', 'PciSlabBeamSection', 'CaBathTubDimensions', 'CaBathTubSection', 'CaBulbTeeSection', 'CaGirderDimensions', 'CaIGirderSection', 'CaVoidedSlabDimensions', 'CaVoidedSlabSection', 'CaWideFlangeSection', 'CoCbtDimensions', 'CoCbtGirderSection', 'IaBeamDimensions', 'IaBulbTeeSection', 'IaIBeamSection', 'IlDeckBeamDimensions', 'IlDeckBeamSection', 'MoDotIGirderDimensions', 'MoDotIGirderSection', 'MoDotNuDimensions', 'MoDotNuGirderSection', 'MoDotBoxBeamSection', 'MoDotBoxDimensions', 'MoDotSolidSlabDimensions', 'MoDotSolidSlabSection', 'MoDotVoidedSlabDimensions', 'MoDotVoidedSlabSection', 'NeNuGirderDimensions', 'NeNuGirderSection', 'NyBoxBeamSection', 'NyGirderDimensions', 'NyPcefBulbTeeSection', 'NySlabUnitSection', 'NyUnitDimensions', 'OrBoxDimensions', 'OrBoxSection', 'OrIGirderDimensions', 'OrIGirderSection', 'OrSlabDimensions', 'OrSlabSection', 'PaAashtoIBeamSection', 'PaBeamDimensions', 'PaBoxBeamDimensions', 'PaBoxBeamSection', 'PaBulbTeeSection', 'PaIBeamSection', 'VaBoxBeamDimensions', 'VaBoxBeamSection', 'VaPcbtDimensions', 'VaPcbtSection', 'VaVoidedSlabDimensions', 'VaVoidedSlabSection', 'WiBoxGirderDimensions', 'WiBoxGirderSection', 'WiGirderDimensions', 'WiGirderSection', 'TxDotDoubleTSection', 'TxDotGirderDimensions', 'TxDotIGirderSection', 'TxDotLegacyIBeamSection', 'TxDotUBeamSection', 'TxDotWideFlangeGirderSection', 'TxDotBoxBeamSection', 'TxDotDeckedSlabBeamSection', 'TxDotSlabBeamSection', 'TxDotSlabBoxDimensions', 'TxDotXBeamSection', 'QaTyBeamDimensions', 'QaTyBeamSection', 'QaTyeBeamSection', 'ImprovedPscBeamDimensions', 'ImprovedPscBeamSection', 'ShanghaiHingedHollowSlabDimensions', 'ShanghaiHingedHollowSlabSection', 'ShanghaiRigidHollowSlabDimensions', 'ShanghaiRigidHollowSlabSection', 'BipreHollowGirderDimensions', 'BipreHollowGirderSection', 'BipreIGirderDimensions', 'BipreIGirderSection', 'JisSlabGirderDimensions', 'JisSlabGirderSection', 'ThbPciGirderDimensions', 'ThbPciGirderSection', 'ThDohBoxBeamDimensions', 'ThDohBoxBeamSection', 'ThDohIGirderR2Dimensions', 'ThDohIGirderR2Section', 'ThDohPlankDimensions', 'ThDohPlankGirderSection', 'WaskitaPcIDimensions', 'WaskitaPcIGirderSection', 'WaskitaVoidedSlabDimensions', 'WaskitaVoidedSlabSection', 'WikaVoidedSlabDimensions', 'WikaVoidedSlabSection', 'TfnswCbsModuleDimensions', 'TfnswCbsModuleSection', 'TmrDeckUnitDimensions', 'TmrDeckUnitSection', 'Vn620GirderDimensions', 'Vn620GirderSection', 'KhVongGirderDimensions', 'KhVongGirderSection', 'GcastIBeamSection', 'GcastTBeamSection', 'GcastTmBeamDimensions', 'GcastTmBeamSection', 'GcastUBeamDimensions', 'GcastUBeamSection', 'JkrPrtBeamSection', 'JkrPrtDimensions', 'OkaMBeamDimensions', 'OkaMBeamSection', 'LsmPscIGirderSection', 'NhaStandardIGirderSection', 'RdaTB505BeamSection', 'RdaTB505Dimensions', 'JicaPcIDimensions', 'JicaPcIGirderSection', 'SadetIBeamDimensions', 'SadetIBeamSection']

__all__ += ['PekabexMgtDimensions', 'PekabexMgtSection', 'SomacoGirderDimensions', 'SomacoGirderSection', 'PrebetGirderDimensions', 'PrebetGirderSection', 'TierraBeamDimensions', 'TierraBeamSection', 'PrethorBeamDimensions', 'PrethorVaSection', 'PrethorVaaSection', 'PrethorVcSection', 'PrethorViSection', 'PrethorVuSection', 'HaitsmaHbmDimensions', 'HaitsmaHbmSection', 'HaitsmaHgrDimensions', 'HaitsmaHgrSection', 'HaitsmaHkpDimensions', 'HaitsmaHkpSection', 'SpanbetonPiqDimensions', 'SpanbetonPiqSection', 'SpanbetonSjpDimensions', 'SpanbetonSjpFlexDimensions', 'SpanbetonSjpFlexSection', 'SpanbetonSjpSection', 'SpanbetonSkkDimensions', 'SpanbetonSkkSection', 'SpanbetonSrpDimensions', 'SpanbetonSrpSection', 'SpanbetonZipDimensions', 'SpanbetonZipSection', 'SpanbetonZipxlSection', 'GrProjectGirderDimensions', 'GrProjectGirderSection', 'FpMcCannBoxBeamDimensions', 'FpMcCannBoxBeamSection', 'FpMcCannMyBeamDimensions', 'FpMcCannMyBeamSection', 'FpMcCannMyeBeamSection', 'FpMcCannSyBeamDimensions', 'FpMcCannSyBeamSection', 'FpMcCannTyBeamDimensions', 'FpMcCannTyBeamSection', 'FpMcCannTyeBeamSection', 'FpMcCannWBeamDimensions', 'FpMcCannWBeamSection', 'FpMcCannYBeamDimensions', 'FpMcCannYBeamSection', 'FpMcCannYeBeamSection', 'SwShpDimensions', 'SwShpSection', 'ItuTipBeamDimensions', 'ItuTipBeamSection', 'Su3503B12Dimensions', 'Su3503B12Section', 'DragonAashtoSection', 'R2AashtoIDimensions', 'TubecoAashtoSection', 'PaverBeamDimensions', 'PaverBeamSection', 'AfgcVippBeamSection', 'AfgcVippDimensions', 'CrhOtBeamSection', 'CrhOtDimensions', 'ThreeBetBeamSection', 'UaB40BeamSection', 'UaBeamDimensions', 'UaBmBeamSection', 'RilaGtDimensions', 'RilaGtSection', 'ZbeMgDimensions', 'ZbeMgSection', 'TilstaSijaDimensions', 'TilstaSijaSection', 'ViaduktSanDimensions', 'ViaduktSanSection', 'DnitPcpLongarinaDimensions', 'DnitPcpLongarinaSection', 'PretensaViDimensions', 'PretensaViSection', 'PuentePrefaBeamDimensions', 'PuentePrefaBeamSection']

__all__ += ['OrDeckBulbTeeDimensions', 'OrDeckBulbTeeSection', 'OhAashtoIBeamSection', 'OhIBeamDimensions', 'OhWfBeamSection', 'SaoDomingosLongarinaDimensions', 'SaoDomingosLongarinaSection', 'MopLosaNervadaVigaDimensions', 'MopLosaNervadaVigaSection', 'MopVigaPostensadaDimensions', 'MopVigaPostensadaSection']

__all__ += ['MiBoxBeamDimensions', 'MiBulbTeeDimensions', 'MiBulbTeeSection', 'MiSideBySideBoxBeamSection', 'MiSpreadBoxBeamSection', 'PhDpwhAashtoDimensions', 'PhDpwhAashtoSection']
