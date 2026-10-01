"""bridgebeams: standard precast/prestressed bridge beam sections for use
with the ``sectionproperties`` package.

Subpackages
-----------
- ``bridgebeams.aus``: Australian Super-T and I-girders to AS5100.5 App. D.

All geometry is in millimetres and returned as ``sectionproperties``
``Geometry`` objects, so sections feed directly into ``sectionproperties``
analysis and into ``concreteproperties``/``PyBridge`` by adding materials.
"""

from bridgebeams.aus import IGirderSection, SuperTGirderSection

__version__ = "0.2.0"

__all__ = ["IGirderSection", "SuperTGirderSection", "__version__"]
