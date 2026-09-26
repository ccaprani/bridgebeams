"""Catalogue-wide invariants for every counted profile.

The counted profile set is exactly ``tools/build_coverage.py``
``implemented()``; this module mirrors its variant rules (to recover the
constructor arguments) and asserts that the mirror reproduces its labels.
Each test walks the whole catalogue and fails once, listing every
``Family:size`` that breaks the invariant.
"""
import importlib
import sys
from pathlib import Path

import pytest
from shapely.geometry import Polygon

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_coverage import implemented  # noqa: E402

ALLOWED = {"transcribed", "transcribed-with-convention",
           "fitted-reconstruction", "estimate"}


def _variants(cls):
    """Counted (label, args, kwargs), mirroring build_coverage.implemented()."""
    name = cls.__name__
    if name in ("FebeISection", "GrExtendedISection", "ThDOHIGirderSection"):
        return []
    if name == "SuperTGirderSection":
        return [(f"T{i}, subtype{s}", (i, s), {}) for s in (1, 2)
                for i in range(1, 6) if not (i == 5 and s == 1)]
    if name == "IGirderSection":
        return [(f"T{i}", (i,), {}) for i in range(1, 5)]
    if name == "IeTYBeamSection":
        return [(size + " " + variant, (size,), {"variant": variant})
                for variant in ("bs", "ss")
                for attr in ("SIZES_" + variant.upper(), "SIZES_EDGE_" + variant.upper())
                for size in getattr(cls, attr)]
    if name == "NzSuperTSection":
        return [("1025 x2490", (1025,), {}), ("1225 x2490", (1225,), {}),
                ("1225 x1990", (1225,), {"top_width": 1990})]
    if name == "NzHollowCoreSection":
        return [(f"{d} {u}", (d, u), {})
                for d, u in [(650, "inner"), (900, "inner"), (587, "inner"), (587, "outer")]]
    sizes = (getattr(cls, "STANDARD_SIZES", None) or getattr(cls, "SIZES", None)
             or getattr(cls, "TYPES", None))
    return [(str(size), (size,), {}) for size in sizes]


def _families():
    """Unique counted families (shared IE/GB aliases appear once)."""
    out = {}
    for families in implemented().values():
        for family in families:
            out.setdefault(family["id"], family)
    return list(out.values())


FAMILIES = _families()
PROFILES = []  # (family_name, label, cls, args, kwargs)
for _family in FAMILIES:
    _cls = getattr(importlib.import_module(_family["module"]), _family["name"])
    for _label, _args, _kwargs in _variants(_cls):
        PROFILES.append((_family["name"], _label, _cls, _args, _kwargs))

# Legacy profile set backfilled with provenance in September 2026: the
# counted variants of these families, plus the uncounted ThDOHIGirder IG-205.
LEGACY_FAMILIES = {
    "IGirderSection", "SuperTGirderSection", "CaMtoSolidSlabSection", "IeMBeamSection",
    "IeUMBBeamSection", "IeMYBeamSection", "IeMYEBeamSection", "IeSYBeamSection",
    "IeSYEBeamSection", "IeSolidBoxBeamSection", "IeTBeamSection", "IeTYBeamSection",
    "IeUBeamSection", "IeWBeamSection", "IeYBeamSection", "IeYEBeamSection",
    "Nh45aPscISection", "JisTGirderSection", "KhcISection", "SepsaIGirderSection",
    "NoNtbKtbSection", "NzHollowCoreSection", "NzIBeamSection", "NzSuperTSection",
    "MostostalTSection", "QaQBeamSection", "Su3503I33Section", "KGMISection",
    "TaiwanISection", "AashtoIBeamSection", "MnRectangularBeamSection", "WsdotWSection",
    "CivilconIBeamSection", "CivilconYBeamSection",
}


# Legacy outlines that are still stored clockwise (not an error for shapely or
# sectionproperties, but pinned so any orientation change is noticed).
KNOWN_CW = (
    {("IGirderSection", f"T{i}") for i in range(1, 5)}
    | {("SuperTGirderSection", f"T{i}, subtype{s}") for s in (1, 2)
       for i in range(1, 6) if not (i == 5 and s == 1)}
    | {("IeUBeamSection", s) for s in ("U600", "U700", "U1", "U3", "U5", "U7", "U8", "U9",
                                       "U10", "U11", "U12", "SU11", "SU12")}
    | {("Su3503I33Section", s) for s in ("B3300.174.153", "B3300.194.153",
                                         "B3300.174.173", "B3300.194.173")}
)


def _polygon(beam):
    poly = getattr(beam, "polygon", None)
    return beam.geometry.geom if poly is None else poly


def _walk(check):
    """Run ``check(beam, key)`` over every counted profile; fail once with all failures."""
    failures = []
    for family, label, cls, args, kwargs in PROFILES:
        try:
            check(cls(*args, **kwargs), (family, label))
        except Exception as exc:  # noqa: BLE001 - report every family/size
            first = (str(exc).strip().splitlines() or [""])[0]
            failures.append(f"{family}:{label}: {type(exc).__name__}: {first}")
    if failures:
        pytest.fail(f"{len(failures)} of {len(PROFILES)} profiles failed:\n  - "
                    + "\n  - ".join(failures), pytrace=False)


def test_variant_mirror_matches_build_coverage():
    mirror = {}
    for family, label, *_ in PROFILES:
        mirror.setdefault(family, []).append(label)
    counted = {f["name"]: f["profiles"] for f in FAMILIES if f["count"]}
    assert mirror == counted
    assert len({f["name"] for f in FAMILIES}) == len(FAMILIES)


def test_legacy_backfill_profile_total():
    # 301 profiles were "unlabelled" before the September 2026 backfill.
    total = sum(1 for family, *_ in PROFILES if family in LEGACY_FAMILIES)
    assert total + 1 == 301  # + ThDOHIGirderSection IG-205


def test_polygon_valid_ccw_nonempty():
    def check(beam, key):
        poly = _polygon(beam)
        assert isinstance(poly, Polygon), type(poly).__name__
        assert not poly.is_empty, "empty"
        assert poly.is_valid, "invalid polygon"
        if key in KNOWN_CW:
            assert not poly.exterior.is_ccw, "pinned clockwise legacy outline is now CCW"
        else:
            assert poly.exterior.is_ccw, "exterior not counter-clockwise"
        assert poly.area > 0, f"area {poly.area}"
        outer = Polygon(poly.exterior)
        for i, ring in enumerate(poly.interiors):
            assert outer.contains(Polygon(ring)), f"void {i} not inside exterior"
    _walk(check)


def test_provenance_and_source_status():
    def check(beam, key):
        assert beam.provenance in ALLOWED, f"provenance {beam.provenance!r}"
        assert isinstance(beam.source_status, str) and beam.source_status.strip(), \
            "empty source_status"
    _walk(check)


def test_geometry_wrapper_matches_polygon():
    def check(beam, key):
        poly = _polygon(beam)
        geom = beam.geometry.geom
        diff = geom.symmetric_difference(poly).area
        assert diff <= 1e-6 * poly.area, f"geometry differs from polygon by {diff:.3g}"
    _walk(check)


def test_legacy_uncounted_and_parametric_profiles_labelled():
    from bridgebeams.be.febe_i_beams import FebeISection
    from bridgebeams.gr.egnatia_extended_i import GrExtendedISection
    from bridgebeams.kr.kgm_i_section import KhcISection
    from bridgebeams.th.doh_igirder import ThDOHIGirderSection
    assert KhcISection("KHC-20").provenance == "estimate"
    assert KhcISection("KHC-40").provenance == "estimate"
    beams = [
        ThDOHIGirderSection(),
        FebeISection("900/620", top_flange_thickness=150, bottom_flange_thickness=150),
        GrExtendedISection(span_m=35.0, weff_m=2.5, top_flange_thickness=200,
                           bottom_flange_thickness=300),
    ]
    for beam in beams:
        assert beam.provenance in ALLOWED
        assert beam.source_status.strip()


def test_unknown_size_rejected():
    """Every counted family rejects a size outside its table with ValueError."""
    failures = []
    seen = set()
    for family, label, cls, args, kwargs in PROFILES:
        if family in seen:
            continue
        seen.add(family)
        bad = ("__no_such_size__",) if isinstance(args[0], str) else (-1,) + tuple(args[1:])
        try:
            cls(*bad, **kwargs)
        except ValueError:
            continue
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{family}{bad}: raised {type(exc).__name__}: {exc}")
        else:
            failures.append(f"{family}{bad}: accepted")
    if failures:
        pytest.fail("\n".join(failures), pytrace=False)
