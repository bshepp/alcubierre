"""Inverse metric and partial derivatives of g_{mu nu}.

Mirrors WarpFactory ``c4Inv`` / ``diffgmunu`` (independent NumPy rewrite).
"""

from __future__ import annotations

import numpy as np

from ..metrics.alcubierre import Metric
from ..utils.fd_stencils import fd1_4th_central


def inverse_metric(g: np.ndarray) -> np.ndarray:
    """Inverse of ``g`` (shape ``(4, 4, ...)``); returns same shape.

    Uses ``np.linalg.inv`` with the matrix axes moved to the trailing
    positions (its native layout).
    """
    # Move (4,4) to trailing -> (..., 4, 4); invert; move back.
    g_mat = np.moveaxis(g, (0, 1), (-2, -1))
    inv = np.linalg.inv(g_mat)
    return np.moveaxis(inv, (-2, -1), (0, 1))


def metric_partials(metric: Metric) -> np.ndarray:
    """Compute ``d_alpha g_{mu nu}`` -> shape ``(4, 4, 4, Nt, Nx, Ny, Nz)``.

    Index 0 (``alpha``) is the differentiation index: 0=t, 1=x, 2=y, 3=z.
    Time and any cartoon-thin axis use the singleton-axis policy in
    ``fd1_4th_central`` (derivative = 0).
    """
    g = metric.g
    dt, dx, dy, dz = metric.grid_scale
    spacings = (dt, dx, dy, dz)
    # Component grid axes are at positions 2,3,4,5 of g (after the (mu, nu) axes).
    # axis arg to fd1 should target the spatial/temporal axis 2+alpha.
    out = np.empty((4,) + g.shape, dtype=np.float64)
    for alpha in range(4):
        out[alpha] = fd1_4th_central(g, axis=2 + alpha, dx=spacings[alpha])
    return out
