"""UK availability aliases for Banagher's shared Ireland/UK beam catalogue.

These names refer to the same geometry classes as :mod:`bridgebeams.ie`.
They represent documented producer availability in both jurisdictions, not
separate UK-standard designs or additional unique profiles.
"""

from ..ie import (
    IeMBeamSection as UkMBeamSection,
    IeMYBeamSection as UkMYBeamSection,
    IeMYEBeamSection as UkMYEBeamSection,
    IeSYBeamSection as UkSYBeamSection,
    IeSYEBeamSection as UkSYEBeamSection,
    IeSolidBoxBeamSection as UkSolidBoxBeamSection,
    IeTBeamSection as UkTBeamSection,
    IeTYBeamSection as UkTYBeamSection,
    IeUBeamSection as UkUBeamSection,
    IeUMBBeamSection as UkUMBBeamSection,
    IeWBeamSection as UkWBeamSection,
    IeYBeamSection as UkYBeamSection,
    IeYEBeamSection as UkYEBeamSection,
)

__all__ = [
    "UkMBeamSection", "UkMYBeamSection", "UkMYEBeamSection",
    "UkSYBeamSection", "UkSYEBeamSection", "UkSolidBoxBeamSection",
    "UkTBeamSection", "UkTYBeamSection", "UkUBeamSection",
    "UkUMBBeamSection", "UkWBeamSection", "UkYBeamSection",
    "UkYEBeamSection",
]

from .r2_fpmccann import (FpMcCannBoxBeamDimensions, FpMcCannBoxBeamSection, FpMcCannMyBeamDimensions, FpMcCannMyBeamSection, FpMcCannMyeBeamSection, FpMcCannSyBeamDimensions, FpMcCannSyBeamSection, FpMcCannTyBeamDimensions, FpMcCannTyBeamSection, FpMcCannTyeBeamSection, FpMcCannWBeamDimensions, FpMcCannWBeamSection, FpMcCannYBeamDimensions, FpMcCannYBeamSection, FpMcCannYeBeamSection)
__all__ += ['FpMcCannBoxBeamDimensions', 'FpMcCannBoxBeamSection', 'FpMcCannMyBeamDimensions', 'FpMcCannMyBeamSection', 'FpMcCannMyeBeamSection', 'FpMcCannSyBeamDimensions', 'FpMcCannSyBeamSection', 'FpMcCannTyBeamDimensions', 'FpMcCannTyBeamSection', 'FpMcCannTyeBeamSection', 'FpMcCannWBeamDimensions', 'FpMcCannWBeamSection', 'FpMcCannYBeamDimensions', 'FpMcCannYBeamSection', 'FpMcCannYeBeamSection']
