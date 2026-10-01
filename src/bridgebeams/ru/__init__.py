"""Russian/CIS standard bridge beam sections (Soyuzdorproekt series)."""

from .su3503_i33 import Su3503I33Dimensions, Su3503I33Section

__all__ = ["Su3503I33Dimensions", "Su3503I33Section"]

from .r2_su3503_b12 import (Su3503B12Dimensions, Su3503B12Section)
__all__ += ['Su3503B12Dimensions', 'Su3503B12Section']
