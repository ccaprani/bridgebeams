"""Taiwan Directorate General of Highways PCI girders, Types I-VII.

Source: 公路總局預力混凝土簡支梁橋橋梁工程標準圖適用性之探討,
臺灣公路工程 Vol.38 No.4-5 (May 2012), Figure 2 (PCI 梁斷面圖) and
Table 4 (各類型 PCI 型梁尺寸表), PDF pp11-12, printed 12-13. The table
summarises the Dec 1991 (民國80年12月) DGH PCI standard drawings
橋-301 ... 橋-336, which the article records as no longer applicable, so
this is a historic family. These are Taiwanese sections: the Roman type
names are unrelated to the AASHTO or Freeway Bureau types.

Table dimensions are centimetres and converted to millimetres. Each
flange is a vertical edge (TFT/BFT) and one straight taper (H1/H3) to the
constant 200 mm web. Type I: Figure 2 prints an 18 cm bottom taper where
Table 4 gives H3 = 19 cm; the table is used and the conflict recorded.

Origin at mid-soffit, y upwards. Post-tensioned midspan gross section;
ducts and end blocks excluded. No published section properties.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.tw")
        .joinpath("data/r2_thb_pci_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class ThbPciGirderDimensions:
    """Gross section dimensions in millimetres (source labels in comments)."""

    depth: float  # GHT
    top_width: float  # GTF
    bottom_width: float  # GBF
    web_width: float  # GWB
    top_flange: float  # TFT
    bottom_flange: float  # BFT
    top_taper: float  # H1
    bottom_taper: float  # H3

    @property
    def clear_web(self) -> float:
        return self.depth - (
            self.top_flange + self.top_taper + self.bottom_flange + self.bottom_taper
        )

    def outline(self) -> list[tuple[float, float]]:
        xw = self.web_width / 2.0
        xb, xt = self.bottom_width / 2.0, self.top_width / 2.0
        d = self.depth
        right = [
            (xb, 0.0),
            (xb, self.bottom_flange),
            (xw, self.bottom_flange + self.bottom_taper),
            (xw, d - self.top_flange - self.top_taper),
            (xt, d - self.top_flange),
            (xt, d),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


class ThbPciGirderSection:
    """DGH 1991 PCI girder Type I-VII gross midspan section.

    >>> from bridgebeams.tw.r2_thb_pci_girders import ThbPciGirderSection
    >>> ThbPciGirderSection("IV").dimensions.depth
    2000.0
    """

    SIZES = ("I", "II", "III", "IV", "V", "VI", "VII")
    source_status = "historic 1991 DGH standard drawings (withdrawn), via 2012 DGH journal summary"

    def __init__(self, size: str = "IV"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        s = row["dimensions_source_cm"]
        self.size = size
        self.span_m = row["span_m"]
        self.provenance = row["provenance"]
        self.published = row
        self.dimensions = ThbPciGirderDimensions(
            depth=10.0 * s["GHT"],
            top_width=10.0 * s["GTF"],
            bottom_width=10.0 * s["GBF"],
            web_width=10.0 * s["GWB"],
            top_flange=10.0 * s["TFT"],
            bottom_flange=10.0 * s["BFT"],
            top_taper=10.0 * s["H1"],
            bottom_taper=10.0 * s["H3"],
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline()), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["ThbPciGirderDimensions", "ThbPciGirderSection"]
