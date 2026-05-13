"""Finite-difference stencils.

Mirrors WarpFactory's `takeFiniteDifference1` (4th-order central, edge-copy at
boundaries). Independent NumPy implementation using slice-tuple indexing.
"""

from __future__ import annotations

import numpy as np


def fd1_4th_central(arr: np.ndarray, axis: int, dx: float) -> np.ndarray:
    """4th-order central first derivative along ``axis``.

    Stencil: ``( -f[i+2] + 8 f[i+1] - 8 f[i-1] + f[i-2] ) / (12 dx)``.

    Boundary policy: copy the nearest interior 4th-order value into the two
    boundary cells on each side. This matches WarpFactory's edge-handling and
    keeps shapes intact; the boundary cells are not 4th-order accurate and
    must be excluded from any in-mask region by the caller.
    """
    n = arr.shape[axis]
    # Singleton axis = "thin" / steady; derivative is identically zero.
    # Matches WarpFactory's handling for snapshot (Nt=1) or cartoon-thin (Nz=1) grids.
    if n == 1:
        return np.zeros_like(arr, dtype=np.float64)
    if n < 5:
        raise ValueError(
            f"fd1_4th_central needs 1 or >=5 samples along axis {axis}, got {n}"
        )

    out = np.empty_like(arr, dtype=np.float64)

    def sl(start: int, stop: int | None) -> tuple[slice, ...]:
        s = [slice(None)] * arr.ndim
        s[axis] = slice(start, stop)
        return tuple(s)

    # Interior (i = 2 .. n-3): 4th-order central
    fp2 = arr[sl(4, None)]
    fp1 = arr[sl(3, -1)]
    fm1 = arr[sl(1, -3)]
    fm2 = arr[sl(0, -4)]
    out[sl(2, -2)] = (-fp2 + 8.0 * fp1 - 8.0 * fm1 + fm2) / (12.0 * dx)

    # Edge-copy: cells 0,1 take cell 2; cells -2,-1 take cell -3.
    interior_lo = sl(2, 3)
    interior_hi = sl(-3, -2)
    out[sl(0, 1)] = out[interior_lo]
    out[sl(1, 2)] = out[interior_lo]
    out[sl(-2, -1)] = out[interior_hi]
    out[sl(-1, None)] = out[interior_hi]

    return out


def fd2_4th_central(arr: np.ndarray, axis: int, dx: float) -> np.ndarray:
    """4th-order central second derivative along ``axis``.

    Stencil: ``(-f[i-2] + 16 f[i-1] - 30 f[i] + 16 f[i+1] - f[i+2]) / (12 dx^2)``.
    Edge-copy boundaries to match ``fd1_4th_central``.

    Used by the WarpFactory-compat Ricci formula (``ricci_tensor_wf_compat``)
    which takes second derivatives of the metric directly rather than first
    derivatives of Christoffel symbols.
    """
    n = arr.shape[axis]
    if n == 1:
        return np.zeros_like(arr, dtype=np.float64)
    if n < 5:
        raise ValueError(
            f"fd2_4th_central needs 1 or >=5 samples along axis {axis}, got {n}"
        )

    out = np.empty_like(arr, dtype=np.float64)

    def sl(start: int, stop: int | None) -> tuple[slice, ...]:
        s = [slice(None)] * arr.ndim
        s[axis] = slice(start, stop)
        return tuple(s)

    fp2 = arr[sl(4, None)]
    fp1 = arr[sl(3, -1)]
    f0 = arr[sl(2, -2)]
    fm1 = arr[sl(1, -3)]
    fm2 = arr[sl(0, -4)]
    out[sl(2, -2)] = (-fp2 + 16.0 * fp1 - 30.0 * f0 + 16.0 * fm1 - fm2) / (12.0 * dx**2)

    interior_lo = sl(2, 3)
    interior_hi = sl(-3, -2)
    out[sl(0, 1)] = out[interior_lo]
    out[sl(1, 2)] = out[interior_lo]
    out[sl(-2, -1)] = out[interior_hi]
    out[sl(-1, None)] = out[interior_hi]
    return out


def fd2_mixed_4th_central(arr: np.ndarray, axis1: int, axis2: int,
                          dx1: float, dx2: float) -> np.ndarray:
    """Mixed second derivative ``d_{a1} d_{a2} arr`` via composed 1st derivatives.

    For ``axis1 == axis2``, delegates to :func:`fd2_4th_central` (more accurate
    than composing two 1st-derivative stencils).
    """
    if axis1 == axis2:
        return fd2_4th_central(arr, axis1, dx1)
    return fd1_4th_central(fd1_4th_central(arr, axis1, dx1), axis2, dx2)
