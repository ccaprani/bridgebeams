"""bridgebeams: standard precast/prestressed bridge beam sections for use
with the ``sectionproperties`` package.

Subpackages
-----------
- ``bridgebeams.aus``: Australian Super-T and I-girders to AS5100.5 App. D.
- ``bridgebeams.ukie``: Irish/UK standard precast beams (T, Y and YE
  families).

All geometry is in millimetres and returned as ``sectionproperties``
``Geometry`` objects, so sections feed directly into ``sectionproperties``
analysis and into ``concreteproperties``/``PyBridge`` by adding materials.
Adapters in :mod:`bridgebeams.adapters` provide one-call bridges to
``concreteproperties`` sections and ``ospgrillage`` section properties.
"""

from bridgebeams.adapters import osp_grillage_properties, to_concreteproperties
from bridgebeams.aus import IGirderSection, SuperTGirderSection
from bridgebeams.kr import KhcIGirderDimensions, KhcISection
from bridgebeams.ru import Su3503I33Dimensions, Su3503I33Section
from bridgebeams.th import ThDOHIGirderDimensions, ThDOHIGirderSection
from bridgebeams.tr import KGMIDimensions, KGMISection
from bridgebeams.za import CivilconIBeamDimensions, CivilconIBeamSection
from bridgebeams.ukie import (
    IeTBeamDimensions,
    IeTBeamSection,
    IeYBeamDimensions,
    IeYBeamSection,
    IeYEBeamDimensions,
    IeYEBeamSection,
    strand_locations,
    wf_of_depth,
)

__version__ = "0.3.0"

__all__ = [
    "IGirderSection",
    "SuperTGirderSection",
    "KGMIDimensions",
    "KGMISection",
    "ThDOHIGirderDimensions",
    "ThDOHIGirderSection",
    "KhcIGirderDimensions",
    "KhcISection",
    "Su3503I33Dimensions",
    "Su3503I33Section",
    "CivilconIBeamDimensions",
    "CivilconIBeamSection",
    "IeTBeamDimensions",
    "IeTBeamSection",
    "IeYBeamDimensions",
    "IeYBeamSection",
    "IeYEBeamDimensions",
    "IeYEBeamSection",
    "strand_locations",
    "wf_of_depth",
    "to_concreteproperties",
    "osp_grillage_properties",
    "__version__",
]
