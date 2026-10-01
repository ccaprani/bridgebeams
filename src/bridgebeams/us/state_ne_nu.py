"""Nebraska NU I-girders NU900-NU2000 (NDOR metric designation).

Source: Nebraska Department of Roads / University of Nebraska-Lincoln,
"Design Aids of NU I-Girder Bridges", section 1.1, Figure 1 (PDF/printed
p13) and Table 1 NU Girder Properties (p14),
https://dot.nebraska.gov/media/cf4norno/design-aids-nu-i-girder-bridges.pdf
(retrieved from the 2025-05-15 Wayback snapshot; the NDOT host refused
connections, so the current 2026 BDM Figure 5.4/Table 5.7 was not seen).

The NU girder is a metric design: Table 1 gives 900-2000 mm heights,
150 mm web, 1225 mm top and 975 mm bottom flange; Figure 1's rounded inch
callouts are conversions of 65/45 mm (top flange edge/taper), 135/140 mm
(bottom flange edge/taper), R200 web fillets and R50 flange-corner radii.
Tapers end on the web faces. A 20 mm soffit chamfer, not drawn, is
included as an estimate fitted to the published areas (provenance
``fitted-reconstruction``; see ``geometry_notes`` in the JSON).

Gross concrete only. Millimetres, origin at soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import ccw_polygon, load_json, mirror_half
from bridgebeams.us.state_mo_girders import nu_half_in

DATA_FILE = "state_ne_nu.json"


@dataclass(frozen=True)
class NeNuGirderDimensions:
    """NU dimensions in millimetres (metric template)."""

    size: str
    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    template_mm: dict


class NeNuGirderSection:
    """NDOR NU900, NU1100, NU1350, NU1600, NU1800 and NU2000 girders."""

    SIZES = ("NU900", "NU1100", "NU1350", "NU1600", "NU1800", "NU2000")

    def __init__(self, size: str = "NU1350"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["sections"][size]
        t = data["template_mm"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_mm = nu_half_in(float(row["depth_mm"]), t)
        self.dimensions = NeNuGirderDimensions(
            size=size, depth=float(row["depth_mm"]), top_width=float(t["top_width"]),
            web_width=float(t["web_width"]), bottom_width=float(t["bottom_width"]),
            template_mm=dict(t),
        )

    @property
    def polygon(self):
        return ccw_polygon(mirror_half(self._half_mm))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["NeNuGirderDimensions", "NeNuGirderSection"]
