"""Pakistan NHA prestressed concrete I-girders.

Two families are provided.

``NhaStandardIGirderSection``: NHA standard Types A-H (H = 1200-2600 mm).
These come from NHA drawings STANDARD/04-06 (March 2005). The dimensions are
transcribed from the Table 1 reproduction in Mustafa & Javed (2025), PDF p2.
The table is read as a five-segment I with straight splays (convention). The
original NHA sheets have not been inspected, and the paper's Figure 1
schematic conflicts with its own table.

``LsmPscIGirderSection``: the 20 m, 30 m and 45 m precast post-tensioned
girders of the Lahore-Sialkot Motorway link highway. Source: NHA-hosted
structural drawings, December 2017: LSM-EBP-BR-ST-008 (PDF p177),
LSM-EBP-BR-ST-012 (PDF p139) and LSM-EBP-BR-ST-015 (PDF p142). The midspan
outlines are fully dimensioned. This is a project design, not a national
standard.

Neither family is a US AASHTO type. Millimetres, origin at mid-soffit,
y upwards. Gross midspan concrete only.
"""

from __future__ import annotations

import json
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile
from bridgebeams.pk._i_outline import FiveSegmentIDimensions


def _load(name: str) -> dict:
    return json.loads(
        resources.files("bridgebeams.pk").joinpath(f"data/{name}").read_text(encoding="utf-8")
    )


class _FiveSegmentISection:
    _DATA = ""
    _KEY = ""
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load(self._DATA)
        row = data[self._KEY][size]
        self.size = size
        self.record = row
        self.source_status = data["source_status"]
        self.provenance = row.get("provenance", data["provenance"])
        self.dimensions = FiveSegmentIDimensions(
            **{k: float(v) for k, v in row["dimensions_mm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.right_half)

    @property
    def geometry(self):
        """Gross concrete ``sectionproperties`` geometry (mm)."""
        return geometry_from_polygon(self.polygon)


class NhaStandardIGirderSection(_FiveSegmentISection):
    """NHA Pakistan standard PSC I-girder, Type ``"A"`` to ``"H"``.

    Examples
    --------
    >>> from bridgebeams.pk import NhaStandardIGirderSection
    >>> NhaStandardIGirderSection("G").dimensions.depth
    2400.0
    """

    _DATA = "nha_standard_i.json"
    _KEY = "types"
    SIZES = ("A", "B", "C", "D", "E", "F", "G", "H")

    def __init__(self, size: str = "E") -> None:
        super().__init__(size)
        self.span_range_m = self.record["span_m"]


class LsmPscIGirderSection(_FiveSegmentISection):
    """Lahore-Sialkot Motorway link precast PSC I-girder: ``"20m"``, ``"30m"``, ``"45m"``."""

    _DATA = "lsm_psc_i.json"
    _KEY = "sizes"
    SIZES = ("20m", "30m", "45m")

    def __init__(self, size: str = "30m") -> None:
        super().__init__(size)
        self.drawing = self.record["drawing"]


__all__ = ["FiveSegmentIDimensions", "NhaStandardIGirderSection", "LsmPscIGirderSection"]
