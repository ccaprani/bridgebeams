"""Provenance labels on families implemented before September 2026.

Every counted profile (same variant rules as ``tools/build_coverage.py``
``implemented()``) must expose one of the four provenance values and a
non-empty ``source_status``. Classes are imported from their modules.
"""
import importlib

import pytest

ALLOWED = {"transcribed", "transcribed-with-convention",
           "fitted-reconstruction", "estimate"}

FAMILIES = [
    ("aus.sections", "IGirderSection"),
    ("aus.sections", "SuperTGirderSection"),
    ("ca.mto_solid_slab", "CaMtoSolidSlabSection"),
    ("ie.ie_m_beam", "IeMBeamSection"),
    ("ie.ie_m_beam", "IeUMBBeamSection"),
    ("ie.ie_my_beam", "IeMYBeamSection"),
    ("ie.ie_my_beam", "IeMYEBeamSection"),
    ("ie.ie_sy_beam", "IeSYBeamSection"),
    ("ie.ie_sy_beam", "IeSYEBeamSection"),
    ("ie.ie_solid_box", "IeSolidBoxBeamSection"),
    ("ie.ie_t_beam", "IeTBeamSection"),
    ("ie.ie_ty_beam", "IeTYBeamSection"),
    ("ie.ie_u_beam", "IeUBeamSection"),
    ("ie.ie_w", "IeWBeamSection"),
    ("ie.ie_y_beam", "IeYBeamSection"),
    ("ie.ie_ye_beam", "IeYEBeamSection"),
    ("india.nhai_nh45a_psc_i", "Nh45aPscISection"),
    ("jp.jis_t_girders", "JisTGirderSection"),
    ("kr.kgm_i_section", "KhcISection"),
    ("mx.sepsa_i_girder", "SepsaIGirderSection"),
    ("no.ntb_ktb", "NoNtbKtbSection"),
    ("nz.hollow_core", "NzHollowCoreSection"),
    ("nz.i_beams", "NzIBeamSection"),
    ("nz.super_t", "NzSuperTSection"),
    ("pl.mostostal_t_girders", "MostostalTSection"),
    ("qa.q_beams", "QaQBeamSection"),
    ("ru.su3503_i33", "Su3503I33Section"),
    ("th.doh_igirder", "ThDOHIGirderSection"),
    ("tr.kgm_i_section", "KGMISection"),
    ("tw.i_section", "TaiwanISection"),
    ("us.aashto_i_beams", "AashtoIBeamSection"),
    ("us.other_state_mn_rectangular", "MnRectangularBeamSection"),
    ("us.wsdot_w_girders", "WsdotWSection"),
    ("za.civilcon_i_beam", "CivilconIBeamSection"),
    ("za.civilcon_y_beam", "CivilconYBeamSection"),
]


def _variants(cls):
    """Counted (label, args, kwargs), mirroring build_coverage.implemented()."""
    name = cls.__name__
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
    if name == "ThDOHIGirderSection":
        return [("IG-205", (), {})]
    sizes = (getattr(cls, "STANDARD_SIZES", None) or getattr(cls, "SIZES", None)
             or getattr(cls, "TYPES", None))
    assert sizes, name
    return [(str(size), (size,), {}) for size in sizes]


def _cases():
    for module, name in FAMILIES:
        cls = getattr(importlib.import_module("bridgebeams." + module), name)
        for label, args, kwargs in _variants(cls):
            yield pytest.param(cls, args, kwargs, id=f"{name}:{label}")


CASES = list(_cases())


def test_counted_profile_total():
    # 301 profiles were "unlabelled" before this backfill.
    assert len(CASES) == 301


@pytest.mark.parametrize("cls,args,kwargs", CASES)
def test_counted_profiles_have_provenance(cls, args, kwargs):
    beam = cls(*args, **kwargs)
    assert beam.provenance in ALLOWED
    assert isinstance(beam.source_status, str) and beam.source_status.strip()


def test_khc_extrapolations_are_estimates():
    from bridgebeams.kr.kgm_i_section import KhcISection
    assert KhcISection("KHC-20").provenance == "estimate"
    assert KhcISection("KHC-40").provenance == "estimate"


def test_parametric_templates_labelled():
    from bridgebeams.be.febe_i_beams import FebeISection
    from bridgebeams.gr.egnatia_extended_i import GrExtendedISection
    beams = [
        FebeISection("900/620", top_flange_thickness=150, bottom_flange_thickness=150),
        GrExtendedISection(span_m=35.0, weff_m=2.5, top_flange_thickness=200,
                           bottom_flange_thickness=300),
    ]
    for beam in beams:
        assert beam.provenance in ALLOWED
        assert beam.source_status.strip()
