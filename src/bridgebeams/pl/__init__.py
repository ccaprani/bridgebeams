"""Polish standard bridge beam sections (Mosty-Łódź T-girders)."""

from .mostostal_t_girders import MostostalTDimensions, MostostalTSection

__all__ = ["MostostalTDimensions", "MostostalTSection"]

from .r2_pekabex_mg_t import (PekabexMgtDimensions, PekabexMgtSection)
__all__ += ['PekabexMgtDimensions', 'PekabexMgtSection']
