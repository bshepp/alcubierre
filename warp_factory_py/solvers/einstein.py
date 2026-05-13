"""Einstein tensor and stress-energy via Einstein equations.

G_{mu nu} = R_{mu nu} - 1/2 g_{mu nu} R
T_{mu nu} = (c^4 / 8 pi G) G_{mu nu}    [SI units, J/m^3 for T^{tt}]

Mirrors WarpFactory ``einT`` / ``met2den`` (independent NumPy rewrite).
"""

from __future__ import annotations

import numpy as np

from ..utils.constants import EINSTEIN_PREFACTOR


def einstein_tensor(
    g: np.ndarray, R_munu: np.ndarray, R_scalar: np.ndarray
) -> np.ndarray:
    """``G_{mu nu}``, shape ``(4, 4, ...)``."""
    return R_munu - 0.5 * g * R_scalar  # broadcasting: R_scalar shape (...)


def stress_energy(G_munu: np.ndarray) -> np.ndarray:
    """``T_{mu nu} = (c^4 / 8 pi G) G_{mu nu}`` (covariant indices, SI)."""
    return EINSTEIN_PREFACTOR * G_munu
