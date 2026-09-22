"""Belgian FEBE standardised prestressed bridge I-beams.

FEBE (Federation de l'Industrie du Beton), *Standardisation des poutres
prefabriquees en beton precontraint pour ouvrages d'art*, 4th ed. 2017:
I-sections ``h = 900-2050 mm`` in 50 mm steps, in two sub-families
(small ``h <= 1650``; large ``h >= 1700``). Designation convention
``h/b`` (e.g. ``900/620``, ``2050/880``); the FEBE drawing labels ``b``
on both flanges (symmetric I, per Ergon's 2018 reproduction of the
standard sections).

Pairing rules (attested): ``b = bw + 480`` (small) / ``bw + 660``
(large); gorge ``g = b - 240`` (small) / ``b - 320`` (large).

Evidence levels (see ``data/febe_i_beams.json``): flange/web widths,
gorge and the n/r/s constants are attested; the per-height ``m`` cycle
and the flange **thicknesses** are search-attested/not published, so the
thicknesses are REQUIRED constructor arguments and ``m`` is carried as
flagged metadata (not used geometrically - the letter-to-dimension
mapping requires the FEBE drawing).

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "febe_i_beams.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.be.data").joinpath(_DATA_FILE).read_text()
    )


def _subfamily_for(h: float) -> str:
    if 900 <= h <= 1650:
        return "small"
    if 1700 <= h <= 2050:
        return "large"
    raise ValueError(
        f"height {h} mm outside the FEBE family (900-1650 or 1700-2050 mm)"
    )


def _rule(subfamily: str, b: float) -> tuple[float, float, float, float, float]:
    """Derive (bw, g, n, r, s) from the sub-family pairing rules."""
    data = _load_data()
    if subfamily == "small":
        rule = data["pairing_rules"]["small"]
        sub = data["subfamilies"]["small"]
        bw = b - rule["b_from_bw"]
        g = b - rule["g_from_b"]
        return bw, g, sub["n"], sub["r"], sub["s"]
    rule = data["pairing_rules"]["large"]
    sub = data["subfamilies"]["large"]
    bw = b - rule["b_from_bw"]
    g = b - rule["g_from_b"]
    return bw, g, sub["n"], sub["r"], sub["s"]


def _validate_size(h: float, b: float, subfamily: str) -> None:
    data = _load_data()
    sub = data["subfamilies"][subfamily]
    if b not in sub["b_values"]:
        raise ValueError(
            f"flange width {b} mm not standard for the {subfamily} family "
            f"(h {subfamily == 'small' and '900-1650' or '1700-2050'}: "
            f"b in {sub['b_values']})"
        )
    bw, g, _, _, _ = _rule(subfamily, b)
    if bw not in sub["bw_values"]:
        raise ValueError(f"web width {bw} mm not in {sub['bw_values']}")
    if g < bw:
        raise ValueError(f"gorge {g} mm narrower than web {bw} mm")


@dataclass(frozen=True)
class FebeIDimensions:
    """Dimensions of one FEBE I-beam size, millimetres.

    ``tf_top``/``tf_bot`` are design thicknesses (the FEBE proposal does
    not publish them); ``m`` is the search-attested cycling dimension
    carried as metadata (its physical mapping needs the FEBE drawing).
    """

    depth: float
    flange_width: float  # b, both flanges (symmetric I)
    web_width: float  # bw
    gorge: float  # g
    n: float
    r: float
    s: float
    m_search_attested: float
    top_flange_thickness: float
    bottom_flange_thickness: float
    subfamily: str

    @property
    def outline(self) -> list[tuple[float, float]]:
        h = self.depth
        t = self.flange_width / 2.0
        w = self.web_width / 2.0
        y1 = h - self.top_flange_thickness
        y3 = self.bottom_flange_thickness
        return [
            (-t, 0.0),
            (t, 0.0),
            (t, y3),
            (w, y3),
            (w, y1),
            (t, y1),
            (t, h),
            (-t, h),
            (-t, y1),
            (-w, y1),
            (-w, y3),
            (-t, y3),
        ]


class FebeISection:
    """Belgian FEBE standardised I-beam as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.be import FebeISection
    >>> beam = FebeISection("900/620", top_flange_thickness=150,
    ...                     bottom_flange_thickness=150)
    >>> beam.dimensions.depth
    900.0
    """

    def __init__(
        self,
        size: str = "900/620",
        *,
        top_flange_thickness: Optional[float] = None,
        bottom_flange_thickness: Optional[float] = None,
    ):
        """
        Parameters
        ----------
        size:
            Designation ``h/b`` per the FEBE convention, e.g. ``"900/620"``
            (small family) or ``"2050/880"`` (large family).
        top_flange_thickness, bottom_flange_thickness:
            Design thicknesses in mm - REQUIRED (keyword-only, no
            defaults): the FEBE proposal does not publish them in open
            sources. For 2050/880 the literature hints 300 (top) /
            210 (bottom), search-attested only.
        """
        if top_flange_thickness is None or bottom_flange_thickness is None:
            raise ValueError(
                "FEBE flange thicknesses are not published in open sources - "
                "supply top_flange_thickness and bottom_flange_thickness "
                "(design values; search-attested hints for 2050/880: 300/210)"
            )
        try:
            h_s, b_s = size.split("/")
            h, b = float(h_s), float(b_s)
        except ValueError as exc:
            raise ValueError(
                f"size must be the designation 'h/b' (e.g. '900/620'), got {size!r}"
            ) from exc
        subfamily = _subfamily_for(h)
        _validate_size(h, b, subfamily)
        bw, g, n, r, s = _rule(subfamily, b)

        data = _load_data()
        # search-attested m cycle across successive 50 mm steps from the
        # sub-family base height: 150 -> 200 -> 250 -> 300 -> 150 -> ...
        base = data["subfamilies"][subfamily]["h_range"][0]
        cycle = [150.0, 200.0, 250.0, 300.0]
        m_attested = cycle[int((h - base) // 50) % 4]

        self.size = size
        self.subfamily = subfamily
        self.dimensions = FebeIDimensions(
            depth=h,
            flange_width=b,
            web_width=bw,
            gorge=g,
            n=n,
            r=r,
            s=s,
            m_search_attested=m_attested,
            top_flange_thickness=float(top_flange_thickness),
            bottom_flange_thickness=float(bottom_flange_thickness),
            subfamily=subfamily,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["FebeIDimensions", "FebeISection"]
