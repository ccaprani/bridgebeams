"""WSDOT 2006 bulb-tee, deck bulb-tee and precast slab girder sections.

Geometry source: WSDOT Bridge Design Manual M 23-50.01 (June 2006),
Appendix A: 5.6-A1-3 bulb tees W32BTG/W38BTG/W62BTG (PDF p. 442; 1 in
bottom chamfer confirmed on detail sheet 5.6-A13-1 Section C, PDF p. 534),
5.6-A1-4 wide-flange bulb tees WF32/38/50/62BTG (PDF p. 443), 5.6-A1-7
deck bulb tees W35DG/W41DG/W53DG/W65DG (PDF p. 446; keyway from detail
5.6-A24-2 Section A, PDF p. 581) and 5.6-A1-8 slabs (PDF p. 447).

These are legacy/hedged families. Every convention and estimate is listed
in ``data/wsdot_extended_girders.json`` (``geometry_notes`` per family) with
per-size residuals against the published properties that exist:

* BTG: 2006 Table 5.6.1-1 (A, Iz, Yb). The drawn outline is 4 in^2 (0.8%)
  larger than the table; unexplained, pinned in tests.
* WFBTG: no published properties; flange width is variable (4'-0" to
  8'-0"), taper run/bevel assumed equal to the BTG values. ``estimate``.
* DG: W35DG at 48 in spacing vs Appendix 5-B8 worked example (A = 669 in^2,
  yb = 20.9 in, I = 100096 in^4, Ip = 169341 in^4). Drip notch omitted.
* Slabs: WSDOT's 2025 properties equal a (module - 1 in) wide rectangle
  minus circular voids at mid-depth, with the joint keys omitted; this
  implementation follows that convention exactly. 24 in and 30 in slabs
  (not in 2006) take H, W, void count and diameter from the 2026
  PRELIMINARY sheet 5.6-A1-11; their void spacing is an estimate.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Point

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us._wsdot_common import (
    INCH_TO_MM,
    ccw_polygon,
    load_data,
    mirrored_ring_in,
    to_mm,
)


# --------------------------------------------------------------------------
# Bulb tees (W*BTG, WF*BTG)
# --------------------------------------------------------------------------
def bulb_tee_right_half_in(depth: float, top_width: float, t: dict):
    tw = t["web_width_in"] / 2
    bb = t["bottom_flange_width_in"] / 2
    c = t["bottom_chamfer_in"]
    ye = t["bottom_edge_height_in"]
    yt = ye + t["bottom_taper_rise_in"]
    y_edge = depth - t["top_edge_in"]
    y_taper = y_edge - t["top_taper_in"]
    y_bev = y_taper - t["top_bevel_rise_in"]
    x_bev = tw + t["top_bevel_run_in"]
    x_taper = x_bev + t["top_taper_run_in"]
    pts = [(0.0, 0.0), (bb - c, 0.0), (bb, c), (bb, ye), (tw, yt), (tw, y_bev), (x_bev, y_taper)]
    half = top_width / 2
    if half >= x_taper:
        pts += [(x_taper, y_edge), (half, y_edge)]
    else:  # narrower than the taper: taper clipped at the flange tip
        pts += [(half, y_taper + (y_edge - y_taper) * (half - x_bev) / (x_taper - x_bev))]
    pts += [(half, depth), (0.0, depth)]
    return pts


@dataclass(frozen=True)
class WsdotBulbTeeDimensions:
    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class WsdotBulbTeeSection:
    """WSDOT 2006 bulb tees W32/38/62BTG and wide-flange WF32/38/50/62BTG.

    ``top_flange_width_in`` applies to WF*BTG only (48-96 in; default from
    the JSON, 72 in). W*BTG have the fixed 49 in flange.
    """

    SIZES = ("W32BTG", "W38BTG", "W62BTG", "WF32BTG", "WF38BTG", "WF50BTG", "WF62BTG")

    def __init__(self, size: str = "W32BTG", top_flange_width_in: float | None = None):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_data()["families"]["BTG"]
        row = fam["sections"][size]
        t = fam["template_in"]
        width = row["top_flange_width_in"]
        if top_flange_width_in is not None:
            if not size.startswith("WF"):
                raise ValueError("top_flange_width_in only applies to WF*BTG sizes")
            lo, hi = fam["wf_flange_width_range_in"]
            if not lo <= top_flange_width_in <= hi:
                raise ValueError(f"top_flange_width_in must be within {lo}-{hi} in")
            width = float(top_flange_width_in)
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row.get("published_2006")
        half_in = bulb_tee_right_half_in(row["depth_in"], width, t)
        self._ring_in = mirrored_ring_in(half_in)
        self.dimensions = WsdotBulbTeeDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_flange_width=width * INCH_TO_MM,
            bottom_flange_width=t["bottom_flange_width_in"] * INCH_TO_MM,
            web_width=t["web_width_in"] * INCH_TO_MM,
            right_half=tuple(to_mm(half_in)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------------------
# Deck bulb tees (W*DG)
# --------------------------------------------------------------------------
def deck_bulb_tee_right_half_in(depth: float, spacing: float, t: dict):
    tw = t["web_width_in"] / 2
    bb = t["bottom_flange_width_in"] / 2
    c = t["bottom_chamfer_in"]
    ye = t["bottom_edge_height_in"]
    yt = ye + t["bottom_taper_rise_in"]
    y_fl = depth - t["flange_thickness_in"]
    y_taper = y_fl - t["top_taper_in"]
    y_bev = y_taper - t["top_bevel_rise_in"]
    x_bev = tw + t["top_bevel_run_in"]
    x_taper = x_bev + t["top_taper_run_in"]
    k = t["keyway"]
    x_top = spacing / 2 - k["top_gap_from_joint_in"]
    x_lip = spacing / 2 - k["bottom_gap_from_joint_in"]
    pts = [(0.0, 0.0), (bb - c, 0.0), (bb, c), (bb, ye), (tw, yt), (tw, y_bev), (x_bev, y_taper)]
    if x_lip >= x_taper:
        pts += [(x_taper, y_fl), (x_lip, y_fl)]
    else:
        pts += [(x_lip, y_taper + (y_fl - y_taper) * (x_lip - x_bev) / (x_taper - x_bev))]
    pts += [
        (x_lip, depth - k["lip_top_below_top_in"]),
        (x_top - k["depth_in"], depth - k["apex_below_top_in"]),
        (x_top, depth - k["top_face_height_in"]),
        (x_top, depth),
        (0.0, depth),
    ]
    return pts


@dataclass(frozen=True)
class WsdotDeckBulbTeeDimensions:
    size: str
    depth: float
    spacing: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class WsdotDeckBulbTeeSection:
    """WSDOT 2006 deck bulb tees W35DG, W41DG, W53DG and W65DG.

    ``spacing_in`` is the girder spacing (joint centreline to centreline,
    48-72 in on the 2006 sheet; default 48 in as in the W35DG worked
    example). The concrete top flange is ``spacing_in - 1``.
    """

    SIZES = ("W35DG", "W41DG", "W53DG", "W65DG")

    def __init__(self, size: str = "W35DG", spacing_in: float | None = None):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_data()["families"]["DG"]
        row = fam["sections"][size]
        t = fam["template_in"]
        lo, hi = fam["spacing_range_in"]
        s = float(fam["default_spacing_in"] if spacing_in is None else spacing_in)
        if not lo <= s <= hi:
            raise ValueError(f"spacing_in must be within {lo}-{hi} in")
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row.get("published_worked_example")
        half_in = deck_bulb_tee_right_half_in(row["depth_in"], s, t)
        self._ring_in = mirrored_ring_in(half_in)
        self.dimensions = WsdotDeckBulbTeeDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            spacing=s * INCH_TO_MM,
            top_flange_width=(s - 2 * t["keyway"]["top_gap_from_joint_in"]) * INCH_TO_MM,
            bottom_flange_width=t["bottom_flange_width_in"] * INCH_TO_MM,
            web_width=t["web_width_in"] * INCH_TO_MM,
            right_half=tuple(to_mm(half_in)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# --------------------------------------------------------------------------
# Solid and voided slab girders
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class WsdotSlabDimensions:
    size: str
    depth: float
    module_width: float
    width: float
    void_diameter: float
    void_x: tuple[float, ...]


class WsdotSlabGirderSection:
    """WSDOT precast prestressed solid/voided slab girders (gross, keys omitted).

    Voids are circular interiors discretised with ``void_segments`` sides;
    note that ``bridgebeams._geometry.section_properties`` ignores holes.
    """

    SIZES = ("SLAB12x48", "SLAB18x48", "SLAB24x48", "SLAB26x48", "SLAB30x52")

    def __init__(self, size: str = "SLAB18x48", void_segments: int = 256):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = load_data()["families"]["SLAB"]
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row.get("published_2025")
        self.void_segments = int(void_segments)
        width = row["module_width_in"] - fam["joint_gap_total_in"]
        self._w_in = width
        self.dimensions = WsdotSlabDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            module_width=row["module_width_in"] * INCH_TO_MM,
            width=width * INCH_TO_MM,
            void_diameter=row["void_diameter_in"] * INCH_TO_MM,
            void_x=tuple(x * INCH_TO_MM for x in row["void_x_in"]),
        )

    @property
    def polygon(self):
        d = self.dimensions
        hw = d.width / 2
        shell = [(-hw, 0.0), (hw, 0.0), (hw, d.depth), (-hw, d.depth)]
        holes = []
        if d.void_x:
            r = d.void_diameter / 2
            q = max(1, self.void_segments // 4)
            for x in d.void_x:
                ring = list(Point(x, d.depth / 2).buffer(r, quad_segs=q).exterior.coords)[:-1]
                holes.append(ring)
        return ccw_polygon(shell, holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "WsdotBulbTeeDimensions", "WsdotBulbTeeSection",
    "WsdotDeckBulbTeeDimensions", "WsdotDeckBulbTeeSection",
    "WsdotSlabDimensions", "WsdotSlabGirderSection",
    "bulb_tee_right_half_in", "deck_bulb_tee_right_half_in",
]
