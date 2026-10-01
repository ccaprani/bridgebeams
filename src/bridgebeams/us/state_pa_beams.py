"""PennDOT prestressed beams: PA I-beams, AASHTO-type I-beams, PA bulb-tees, boxes and planks.

Source: PennDOT Bridge Design Standard BD-652M "Standard Prestressed Beam
Sizes and Section Properties", sheets 1-3, recommended 29 April 2016
(current file on docs.penndot.pa.gov, PDF modified January 2025).
Adjacent-box and plank shear keys follow the companion standard BC-775M
(recommended 23 November 2022), "Shear Key Detail", sheet 2.

Every dimension is tabulated in the source (inches). BD-652M note 5 says
"all chamfers 3/4 x 3/4 unless noted"; PennDOT's own tabulated properties
exclude these chamfers (the sharp-cornered outlines reproduce the printed
area, yb and I exactly), so the outlines here omit them as well. That is
the only convention for the I-beams, bulb-tees and spread boxes
(provenance ``transcribed-with-convention``).

The PennDOT "AASHTO I-beams" 28/63-28/96 are PennDOT's own tabulation; they
are kept separate from :class:`bridgebeams.us.AashtoIBeamSection` (PCI).

Gross concrete only: no strands, deck, end blocks or dapped ends.
Millimetres, origin at the soffit centre, y upwards.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    dedupe,
    load_json,
    mirror_half,
    to_mm,
)

DATA_FILE = "state_pa_bd652m.json"


def _data() -> dict:
    return load_json(DATA_FILE)


# ------------------------------------------------------------------ outlines
def pa_i_half_in(d: dict) -> list[tuple[float, float]]:
    """PA I-beam right half (inches): trapezoidal flanges, no top taper."""
    w = d["W3"] / 2
    return [
        (0.0, 0.0),
        (d["W1"] / 2, 0.0),
        (d["W1"] / 2, d["T1"]),
        (w, d["T1"] + d["B1"]),
        (w, d["T1"] + d["B1"] + d["C"]),
        (d["W2"] / 2, d["D"] - d["T2"]),
        (d["W2"] / 2, d["D"]),
        (0.0, d["D"]),
    ]


def pa_aashto_half_in(d: dict) -> list[tuple[float, float]]:
    """PennDOT AASHTO-type I-beam right half (inches)."""
    w = d["W3"] / 2
    y_web_top = d["T1"] + d["B1"] + d["C"]
    return [
        (0.0, 0.0),
        (d["W1"] / 2, 0.0),
        (d["W1"] / 2, d["T1"]),
        (w, d["T1"] + d["B1"]),
        (w, y_web_top),
        (w + d["B4"], y_web_top + d["B3"]),
        (d["W2"] / 2, d["D"] - d["T2"]),
        (d["W2"] / 2, d["D"]),
        (0.0, d["D"]),
    ]


def pa_bulb_tee_half_in(d: dict) -> list[tuple[float, float]]:
    """PA bulb-tee right half (inches)."""
    w = d["W3"] / 2
    y_bulb = d["T1"] + d["B1"]
    y_web_bot = y_bulb + d["D2"]
    y_web_top = y_web_bot + d["C"]
    return [
        (0.0, 0.0),
        (d["W1"] / 2, 0.0),
        (d["W1"] / 2, d["T1"]),
        (w + d["X2"], y_bulb),
        (w, y_web_bot),
        (w, y_web_top),
        (w + d["B4"], y_web_top + d["B3"]),
        (d["W2"] / 2, d["D"] - d["T2"]),
        (d["W2"] / 2, d["D"]),
        (0.0, d["D"]),
    ]


def bc775_key_right_in(width: float, depth: float, key: dict) -> list[tuple[float, float]]:
    """Right face with the BC-775M shear-key recess, listed bottom to top."""
    x = width / 2
    top, height = key["top_in"], key["height_in"]
    r1, r2 = key["upper_recess_in"], key["key_recess_in"]
    t1, t2 = key["upper_taper_rise_in"], key["lower_taper_rise_in"]
    down = [
        (x - r1, depth),
        (x - r1, depth - top),
        (x - r2, depth - top - t1),
        (x - r2, depth - top - height + t2),
        (x, depth - top - height),
    ]
    return list(reversed(down))


def box_void_in(width: float, depth: float, t: dict) -> list[tuple[float, float]]:
    x = width / 2 - t["web_in"]
    y0, y1 = t["bottom_slab_in"], depth - t["top_slab_in"]
    f = t["void_fillet_small_in"] if depth <= t["small_fillet_max_depth_in"] else t["void_fillet_large_in"]
    return [(-x + f, y0), (x - f, y0), (x, y0 + f), (x, y1 - f), (x - f, y1),
            (-x + f, y1), (-x, y1 - f), (-x, y0 + f)]


# ------------------------------------------------------------------ classes
@dataclass(frozen=True)
class PaBeamDimensions:
    """Overall dimensions (mm) plus the source table row (inches)."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    source_row_in: tuple[tuple[str, float], ...]


class _PaGirderBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()
    _half = staticmethod(pa_i_half_in)

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["families"][self.FAMILY]
        row = fam["sections"][size]
        dims = row["dimensions_in"]
        self.size = size
        self.row = row
        self.published = row["published"]
        self.provenance = row.get("provenance", fam["provenance"])
        self.source_status = fam["source_status"]
        self._ring_in = mirror_half(self._half(dims))
        self.dimensions = PaBeamDimensions(
            size=size,
            depth=dims["D"] * INCH_TO_MM,
            top_width=dims["W2"] * INCH_TO_MM,
            bottom_width=dims["W1"] * INCH_TO_MM,
            web_width=dims["W3"] * INCH_TO_MM,
            source_row_in=tuple(dims.items()),
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class PaIBeamSection(_PaGirderBase):
    """PennDOT BD-652M "PA. I-beams" 18/30 to 26/63 (top/bottom width, depth)."""

    FAMILY = "pa_i_beam"
    SIZES = (
        "18/30", "20/30", "18/33", "20/33", "24/33", "26/33", "18/36", "20/36",
        "24/36", "26/36", "20/39", "24/42", "24/45", "24/48", "24/51", "24/54",
        "26/54", "24/60", "26/60", "24/63", "26/63",
    )
    _half = staticmethod(pa_i_half_in)

    def __init__(self, size: str = "24/48"):
        super().__init__(size)


class PaAashtoIBeamSection(_PaGirderBase):
    """PennDOT BD-652M "AASHTO I-beams" 28/63 to 28/96 (PennDOT tabulation)."""

    FAMILY = "pa_aashto_i_beam"
    SIZES = ("28/63", "28/66", "28/72", "28/78", "28/84", "28/90", "28/96")
    _half = staticmethod(pa_aashto_half_in)

    def __init__(self, size: str = "28/72"):
        super().__init__(size)


class PaBulbTeeSection(_PaGirderBase):
    """PennDOT BD-652M PA bulb-tees: 33 in bottom, 36/42/48 in top, two bulb depths."""

    FAMILY = "pa_bulb_tee"
    SIZES = tuple(
        f"33/{d}"
        for d in (
            "31", "39", "47", "55", "63", "71", "79", "87", "95",
            "29", "37", "45", "53", "61", "69", "77", "85", "93",
            "31.25", "39.25", "47.25", "55.25", "63.25", "71.25", "79.25", "87.25", "95.25",
            "29.25", "37.25", "45.25", "53.25", "61.25", "69.25", "77.25", "85.25", "93.25",
            "31.5", "39.5", "47.5", "55.5", "63.5", "71.5", "79.5", "87.5", "95.5",
            "29.5", "37.5", "45.5", "53.5", "61.5", "69.5", "77.5", "85.5", "93.5",
        )
    )
    _half = staticmethod(pa_bulb_tee_half_in)

    def __init__(self, size: str = "33/63.25"):
        super().__init__(size)


@dataclass(frozen=True)
class PaBoxBeamDimensions:
    """Box/plank dimensions in millimetres."""

    size: str
    kind: str
    width: float
    depth: float
    has_void: bool
    has_shear_keys: bool


_BOX_DEPTHS = (17, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 54, 60, 66)


class PaBoxBeamSection:
    """PennDOT BD-652M adjacent and spread box beams (36/48 in) and 12 in planks.

    Sizes are ``"adjacent-48x33"``, ``"spread-36x21"`` and ``"plank-48x12"``.
    Adjacent boxes and planks carry the BC-775M shear-key recess on both
    faces (an interior unit); spread boxes have plain faces.
    """

    SIZES = tuple(
        [f"adjacent-{w}x{d}" for w in (48, 36) for d in _BOX_DEPTHS]
        + [f"spread-{w}x{d}" for w in (48, 36) for d in _BOX_DEPTHS]
        + ["plank-48x12", "plank-36x12"]
    )

    def __init__(self, size: str = "adjacent-48x33"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["families"]["pa_box_beam"]
        row = fam["sections"][size]
        kind, wd = size.split("-")
        width, depth = (float(v) for v in wd.split("x"))
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.published = row["published"]
        self.provenance = row.get("provenance", fam["provenance"])
        self.source_status = fam["source_status"]
        if kind == "spread":
            shell = [(-width / 2, 0.0), (width / 2, 0.0), (width / 2, depth), (-width / 2, depth)]
        else:
            key = fam["shear_key_in"]["12in" if depth == 12 else "other"]
            right = bc775_key_right_in(width, depth, key)
            right = [(width / 2, 0.0)] + right
            shell = [(-width / 2, 0.0)] + right + [(-x, y) for x, y in reversed(right)][:-1]
        self._shell_in = dedupe(shell)
        self._void_in = box_void_in(width, depth, t) if kind != "plank" else None
        self.dimensions = PaBoxBeamDimensions(
            size=size, kind=kind, width=width * INCH_TO_MM, depth=depth * INCH_TO_MM,
            has_void=kind != "plank", has_shear_keys=kind != "spread",
        )

    @property
    def polygon(self):
        """Gross concrete outline (mm) with the void as a clockwise interior."""
        holes = [to_mm(self._void_in)] if self._void_in else []
        return ccw_polygon(to_mm(self._shell_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "PaBeamDimensions", "PaIBeamSection", "PaAashtoIBeamSection", "PaBulbTeeSection",
    "PaBoxBeamDimensions", "PaBoxBeamSection",
]
