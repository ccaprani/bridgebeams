"""Turkish precast pretensioned I-beams TİP I/II/III x A/B/C (İTÜ thesis, 2008).

Source: S. T. Sarsık, "Öngerilmeli Prefabrike I Kesitli Köprü Kirişlerinin
Optimizasyonu", M.Sc. thesis, İstanbul Teknik Üniversitesi, 2008, §3
(Şekil 3.1-3.3, Tablo 3.1-3.6, PDF pp 20-23). Nine "tip" beams used in
bridge superstructures: three flange types (TİP I: 75/50 cm, TİP II: 75/75 cm,
TİP III: 95/75 cm top/bottom flange width) by three heights (A 75, B 90,
C 120 cm). Plain I-sections with splayed flanges and a 20 cm web of height
H - 45 cm. The thesis does not attribute the shapes to KGM type drawings
(KGM is cited only for the H30-S24 live load), so that attribution is
unverified.

TİP I and II are transcribed exactly and reproduce the published F, yalt and
Ix. For TİP III the printed chain (9.5 + 13.5 + 7.5 + 15 = 45.5) does not close
with H - 45; a 13.0 cm top splay closes it and reproduces the published
properties exactly (convention, see ``data/r2_itu_tip.json``).

Geometry convention: millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "r2_itu_tip.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.tr.data").joinpath(_DATA_FILE).read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class ItuTipBeamDimensions:
    """Dimensions of one TİP beam, millimetres."""

    depth: float
    top_width: float
    top_flange: float
    top_splay_offset: float
    top_splay_height: float
    web_width: float
    bottom_splay_height: float
    bottom_flange: float
    bottom_width: float

    @property
    def web_height(self) -> float:
        return self.depth - (
            self.top_flange + self.top_splay_height + self.bottom_splay_height + self.bottom_flange
        )

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the bottom-left soffit corner."""
        h = self.depth
        bt, bb, w = self.top_width / 2, self.bottom_width / 2, self.web_width / 2
        y1 = self.bottom_flange
        y2 = y1 + self.bottom_splay_height
        y4 = h - self.top_flange
        y3 = y4 - self.top_splay_height
        xs = bt - self.top_splay_offset  # splay start on the flange underside
        right = [(bb, 0.0), (bb, y1), (w, y2), (w, y3), (xs, y4)]
        if self.top_splay_offset > 0:
            right.append((bt, y4))
        right.append((bt, h))
        left = [(-x, y) for x, y in reversed(right)]
        return right + left


class ItuTipBeamSection:
    """TİP I/II/III x A/B/C precast I-beam as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.tr.r2_itu_tip import ItuTipBeamSection
    >>> ItuTipBeamSection("TIP-II-A").dimensions.depth
    750.0
    """

    SIZES = (
        "TIP-I-A", "TIP-I-B", "TIP-I-C",
        "TIP-II-A", "TIP-II-B", "TIP-II-C",
        "TIP-III-A", "TIP-III-B", "TIP-III-C",
    )

    source_status = (
        "M.Sc. thesis (İTÜ 2008) documenting 9 standard 'tip' beams; "
        "issuing authority not stated"
    )

    def __init__(self, size: str = "TIP-II-A"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        fam = data["families"][size.split("-")[1]]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.composite_effective_width = fam["composite_effective_width"] * 10.0
        cm = 10.0
        self.dimensions = ItuTipBeamDimensions(
            depth=row["H_cm"] * cm,
            top_width=fam["top_width"] * cm,
            top_flange=fam["top_flange"] * cm,
            top_splay_offset=fam["top_splay_offset"] * cm,
            top_splay_height=fam["top_splay_height"] * cm,
            web_width=fam["web"] * cm,
            bottom_splay_height=fam["bottom_splay_height"] * cm,
            bottom_flange=fam["bottom_flange"] * cm,
            bottom_width=fam["bottom_width"] * cm,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["ItuTipBeamDimensions", "ItuTipBeamSection"]
