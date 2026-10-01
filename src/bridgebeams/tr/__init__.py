"""Turkish standard precast bridge beam sections (KGM)."""

from .kgm_i_section import KGMIDimensions, KGMISection

__all__ = ["KGMIDimensions", "KGMISection"]

from .r2_itu_tip import (ItuTipBeamDimensions, ItuTipBeamSection)
__all__ += ['ItuTipBeamDimensions', 'ItuTipBeamSection']
