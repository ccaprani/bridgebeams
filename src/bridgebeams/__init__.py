"""bridgebeams: standard precast/prestressed bridge beam sections for use
with the ``sectionproperties`` package.

Subpackages
-----------
- ``bridgebeams.aus``: Australian Super-T and I-girders to AS5100.5 App. D.
- ``bridgebeams.ukie``: Irish/UK standard precast beams (Y family pilot).

All geometry is in millimetres and returned as ``sectionproperties``
``Geometry`` objects, so sections feed directly into ``sectionproperties``
analysis and into ``concreteproperties``/``PyBridge`` by adding materials.
"""

from bridgebeams.aus import IGirderSection, SuperTGirderSection
from bridgebeams.ukie import IeYBeamDimensions, IeYBeamSection, strand_locations

__version__ = "0.2.0"

__all__ = [
    "IGirderSection",
    "SuperTGirderSection",
    "IeYBeamDimensions",
    "IeYBeamSection",
    "strand_locations",
    "__version__",
]
