"""bridgebeams: standard precast/prestressed bridge beam sections for use
with the ``sectionproperties`` package.

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
    "__version__",
]
