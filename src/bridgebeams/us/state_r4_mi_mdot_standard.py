"""MDOT standard prestressed concrete beams (PC special details + BDG 6.60).

Sources (SHA-256 and page locators in data/state_r4_mi_mdot_standard.json):

* ``MiMdotISection``: PC-1Q "Prestressed Concrete I-Beam Details"
  (12-22-2025) Types I-IV, 28/36/45/54 in deep, with BDG 6.60.01
  "BEAM PROPERTIES" (issued 02/14/11) as the property cross-check
  (4 profiles, ``I28``..``I54``).
* ``MiMdot70ISection``: PC-2L 70 in Prestressed Concrete I-Beam Details
  (12-22-2025) (1 profile, ``I70``).
* ``MiMdot1800Section``: PC-4J Prestressed Concrete 1800 Beam Details
  (12-22-2025) with BDG 6.60.02 Michigan 1800 Girder properties
  (1 profile, ``1800``). Web-flange junctions use the printed R7 7/8 in
  and R2 in radii; the sharp-corner area is about 5 % under the printed
  875 sq in, the filleted model about 1.4 %.
* ``MiMdotBulbTeeSection``: PC-5D Prestressed Concrete Bulb-Tee Beam
  Details (12-22-2025) with BDG 6.60.03: 49 in top flange series,
  depths 36-72 in (7 profiles, ``BT36``..``BT72``). The outline is the
  same template as the OR15-182 BT36-BT48 recommendations
  (``bridgebeams.us.state_r3_mi_beams.MiBulbTeeSection``); it reproduces
  the BDG printed A, Ybot and Ixx for every depth to 0.1 %. The 61 in top
  flange variant is not yet transcribed.

Gross midspan concrete: strands, end blocks, diaphragms and haunches are
omitted. Millimetres, origin at soffit centre, y up.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    dedupe,
    filleted_path,
    load_json,
    mirror_half,
    to_mm,
)

DATA_FILE = "state_r4_mi_mdot_standard.json"


def _data() -> dict:
    return load_json(DATA_FILE)


def i_beam_half_in(depth, d):
    """Right half (in) of an MDOT I-beam section, from (0, 0) to (0, depth).

    ``d`` carries the printed vertical chain (tip, taper, web height,
    splay and bulb measured down from the top), the flange widths, the
    web thickness and the soffit chamfer.
    """
    tw, bw, ww = d["top_width"] / 2, d["bottom_width"] / 2, d["web"] / 2
    ch = d["soffit_chamfer"]
    y_tip = depth - d["tip"]
    y_taper = y_tip - d["taper"]
    y_splay = d["bulb"]
    return [
        (0.0, 0.0),
        (bw - ch, 0.0),
        (bw, ch),
        (bw, y_splay),
        (ww, y_splay + d["splay"]),
        (ww, y_taper),
        (tw, y_tip),
        (tw, depth),
        (0.0, depth),
    ]


def i70_half_in(depth, d):
    """Right half (in) of the PC-2L 70 in I-beam.

    Chain (top to bottom): 6 in tip, 2 in taper, 1 1/2 in step, 49 1/2 in
    web, 3 1/2 in splay, 7 1/2 in bulb.
    """
    tw, bw, ww = d["top_width"] / 2, d["bottom_width"] / 2, d["web"] / 2
    ch = d["soffit_chamfer"]
    y_taper = depth - d["tip"]
    y_slope = y_taper - d["taper"]
    y_web = y_slope - d["step"]
    y_web_bot = y_web - d["web_height"]
    y_splay = d["bulb"]
    return dedupe([
        (0.0, 0.0),
        (bw - ch, 0.0),
        (bw, ch),
        (bw, y_splay),
        (ww, y_splay + d["splay"]),
        (ww, y_web_bot),
        (ww, y_web),
        (tw, y_slope),
        (tw, y_taper),
        (tw, depth),
        (0.0, depth),
    ])


def beam1800_half_in(depth, d):
    """Right half (in) of the PC-4J 1800 beam, with printed fillet radii.

    Chain (top to bottom): 3 in tip face, 2 in slope drop, 4'-6 1/2 in
    long slope/web zone, 5 1/2 in splay, 5 7/8 in bulb. Fillets R7 7/8 at
    both web junctions, R2 at the tip corner and the bulb-splay corner,
    R2 at the soffit corners.
    """
    tw, bw, ww = d["top_width"] / 2, d["bottom_width"] / 2, d["web"] / 2
    ch = d["soffit_chamfer"]
    y_slope_top = depth - d["tip"]
    y_slope_end = y_slope_top - d["slope_drop"]
    y_web_bot = y_slope_end - d["slope_web"]
    y_splay = d["bulb"]
    path = dedupe([
        (0.0, 0.0),
        (bw - ch, 0.0),
        (bw, ch),
        (bw, y_splay),
        (ww, y_splay + d["splay"]),
        (ww, y_web_bot),
        (ww, y_slope_end),
        (tw, y_slope_top),
        (tw, depth),
        (0.0, depth),
    ])
    radii = {3: d["r_bulb"], 4: d["r_web_bot"], 5: d["r_web_top"], 6: d["r_tip"]}
    return filleted_path(path, radii)


def bulb_tee_half_in(depth, t):
    """Right half (in) of the BDG 6.60.03 49 in top-flange bulb tee."""
    bw, tw, wb = t["bottom_width"] / 2, t["top_width"] / 2, t["web"] / 2
    y1 = t["bottom_edge"]
    y2 = y1 + t["bottom_taper_rise"]
    y3 = y2 + t["bottom_fillet_rise"]
    yt1 = depth - t["top_edge"]
    yt2 = yt1 - t["top_taper_rise"]
    yt3 = yt2 - t["top_fillet_rise"]
    return [
        (0.0, 0.0),
        (bw - t["bottom_bevel"], 0.0),
        (bw, t["bottom_bevel"]),
        (bw, y1),
        (bw - t["bottom_taper_run"], y2),
        (wb, y3),
        (wb, yt3),
        (wb + t["top_fillet_run"], yt2),
        (tw, yt1),
        (tw, depth),
        (0.0, depth),
    ]


@dataclass(frozen=True)
class MiMdotIBeamDimensions:
    """MDOT I-beam dimensions in millimetres (``source_in`` in inches)."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web: float
    right_half: tuple[tuple[float, float], ...]


class _MiMdotBeamBase:
    SIZES: tuple[str, ...] = ()
    DEFAULT = ""

    def __init__(self, size: str | None = None):
        size = self.DEFAULT if size is None else size
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _data()
        grp = data[self._GROUP]
        tpl = grp.get("template_in", {})
        self.size = size
        self.row = {**grp.get("common_in", {}), **grp["sections"][size]}
        self.provenance = self.row.get("provenance", grp["provenance"])
        self.source_status = data["source_status"]
        self.published = self.row.get("printed_properties")
        self._ring_in = mirror_half(self._half_in(data, self.row))
        self.dimensions = MiMdotIBeamDimensions(
            size=size,
            depth=self.row["depth"] * INCH_TO_MM,
            top_width=self.row.get("top_width", tpl.get("top_width", 0.0)) * INCH_TO_MM,
            bottom_width=self.row.get("bottom_width", tpl.get("bottom_width", 0.0)) * INCH_TO_MM,
            web=self.row.get("web", tpl.get("web", 0.0)) * INCH_TO_MM,
            right_half=tuple(to_mm(self._ring_in[0 : len(self._ring_in) // 2 + 1])),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class MiMdotISection(_MiMdotBeamBase):
    """MDOT PC-1Q prestressed I-beam, Types I-IV (28 to 54 in deep)."""

    _GROUP = "i_beam"
    SIZES = ("I28", "I36", "I45", "I54")
    DEFAULT = "I36"

    def _half_in(self, data, row):
        return i_beam_half_in(row["depth"], row)


class MiMdot70ISection(_MiMdotBeamBase):
    """MDOT PC-2L 70 in prestressed I-beam."""

    _GROUP = "i70"
    SIZES = ("I70",)
    DEFAULT = "I70"

    def _half_in(self, data, row):
        return i70_half_in(row["depth"], row)


class MiMdot1800Section(_MiMdotBeamBase):
    """MDOT PC-4J prestressed concrete 1800 beam."""

    _GROUP = "beam_1800"
    SIZES = ("1800",)
    DEFAULT = "1800"

    def _half_in(self, data, row):
        return beam1800_half_in(row["depth"], row)


class MiMdotBulbTeeSection(_MiMdotBeamBase):
    """MDOT PC-5D / BDG 6.60.03 bulb tee, 49 in top flange, 36-72 in deep.

    Same outline as the OR15-182 BT36-BT48 recommendations
    (``MiBulbTeeSection``), extended with the BDG's deeper sizes. The 61 in
    top flange variant of BDG 6.60.03 is not yet transcribed.
    """

    _GROUP = "bulb_tee"
    SIZES = ("BT36", "BT42", "BT48", "BT54", "BT60", "BT66", "BT72")
    DEFAULT = "BT48"

    def _half_in(self, data, row):
        return bulb_tee_half_in(row["depth"], data[self._GROUP]["template_in"])


__all__ = [
    "MiMdotIBeamDimensions",
    "MiMdotISection",
    "MiMdot70ISection",
    "MiMdot1800Section",
    "MiMdotBulbTeeSection",
]
