"""Greek standard bridge beam sections (Egnatia extended-I proposal)."""

from .egnatia_extended_i import (
    EgnatiaIDimensions,
    GrExtendedISection,
    depth_law,
    standard_depth,
    web_width,
)

__all__ = [
    "EgnatiaIDimensions",
    "GrExtendedISection",
    "depth_law",
    "standard_depth",
    "web_width",
]
