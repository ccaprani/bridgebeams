"""Standard AASHTO I-girders as presented for Philippine (DPWH) practice.

Source: an owner-supplied presentation slide, "Types of Bridges (Philippines)
— Deck Girder Bridges — Prestressed Concrete Girders (PSCG) — Standard AASHTO
I-Girders", with five metric-dimensioned outlines labelled TYPE I to TYPE V.
The slide's origin (author, date, URL) is unrecorded, so it is treated as a
secondary presentation of DPWH practice, not a DPWH standard drawing. Local
copy: ``sources/expansion/round2/manual/ph/owner-supplied-types-of-bridges-
philippines-aashto.png`` (SHA-256 ``c5e9056f…4d44988f2d``).

Label conflict: the outline the slide calls "TYPE V" is 1829 mm deep with a
1067 mm top flange — exactly AASHTO/PCI **Type VI** (72 in), not Type V
(63 in, 1600 mm). It is kept under the size name ``"V-as-drawn"``; its
geometry matches :class:`bridgebeams.us.AashtoIBeamSection` ``"VI"`` within
inch-to-mm rounding. Types I–IV match US Types I–IV likewise. This is a
separate jurisdiction record from its own metric source, not an alias.

Millimetres, origin at mid-soffit, y upwards; gross outline only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ph")
        .joinpath("data/dpwh_aashto.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class PhDpwhAashtoDimensions:
    """Slide callouts (mm). ``top_fillet``/``top_fillet_width`` are 0 for I–IV."""

    depth: float
    top_width: float
    web: float
    bottom_width: float
    top_flange: float
    top_taper: float
    top_fillet: float
    top_fillet_width: float
    web_height: float
    bottom_taper: float
    bottom_flange: float

    @property
    def right_half(self) -> list[tuple[float, float]]:
        chain = (self.top_flange + self.top_taper + self.top_fillet
                 + self.web_height + self.bottom_taper + self.bottom_flange)
        if abs(chain - self.depth) > 1e-9:
            raise ValueError(f"vertical chain {chain} does not close on depth {self.depth}")
        b, w, t = self.bottom_width / 2, self.web / 2, self.top_width / 2
        y_web_bot = self.bottom_flange + self.bottom_taper
        y_web_top = y_web_bot + self.web_height
        pts = [(b, 0.0), (b, self.bottom_flange), (w, y_web_bot), (w, y_web_top)]
        if self.top_fillet:
            pts.append((w + self.top_fillet_width, y_web_top + self.top_fillet))
        pts += [(t, self.depth - self.top_flange), (t, self.depth)]
        return pts


class PhDpwhAashtoSection:
    """Philippine Standard AASHTO I-girder ``"I"``–``"IV"`` or ``"V-as-drawn"``.

    ``"V-as-drawn"`` is the slide's "TYPE V", whose dimensions are those of
    AASHTO Type VI (1829 mm deep).

    Examples
    --------
    >>> PhDpwhAashtoSection("V-as-drawn").polygon.bounds
    (-533.5, 0.0, 533.5, 1829.0)
    """

    SIZES = ("I", "II", "III", "IV", "V-as-drawn")
    source_status = "secondary presentation slide (origin unrecorded); DPWH practice"

    def __init__(self, size: str = "I") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        chain = row["chain_as_drawn"]
        self.size = size
        self.label_on_slide = row["label_on_slide"]
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = PhDpwhAashtoDimensions(
            depth=float(row["depth"]),
            top_width=float(row["top_width"]),
            web=float(row["web"]),
            bottom_width=float(row["bottom_width"]),
            top_flange=float(chain["top_flange"]),
            top_taper=float(chain["top_taper"]),
            top_fillet=float(chain.get("top_fillet", 0)),
            top_fillet_width=float(row.get("top_fillet_width", 0)),
            web_height=float(row["web_height_used"]),
            bottom_taper=float(chain["bottom_taper"]),
            bottom_flange=float(chain["bottom_flange"]),
        )

    @property
    def polygon(self) -> Polygon:
        return orient(polygon_from_half_profile(self.dimensions.right_half), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["PhDpwhAashtoDimensions", "PhDpwhAashtoSection"]
