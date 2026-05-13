"""Eulerian-observer transformation matrix.

Builds the 4x4 matrix ``M`` at each grid point such that

    eta_{a b} = M^mu_a M^nu_b g_{mu nu}

where ``eta = diag(-1, +1, +1, +1)``. ``M`` is the inverse tetrad: it takes
local-orthonormal-frame indices to coordinate indices. Any tensor expressed
on the coordinate basis is converted to the Eulerian (locally Lorentzian)
frame by contracting both indices with ``M``.

The construction uses a Cholesky-like factorisation of the spatial 3-metric
plus the lapse/shift decomposition (ADM form), implemented via NumPy's
``np.linalg.cholesky`` on the spatial block.

Mirrors WarpFactory ``getEulerianTransformationMatrix`` (independent NumPy
rewrite).
"""

from __future__ import annotations

import numpy as np


def eulerian_transformation(g: np.ndarray, wf_compat: bool = False) -> np.ndarray:
    """Returns ``M`` of shape ``(4, 4, ...)`` such that
    ``M[mu, a] g_{mu nu} M[nu, b] = eta_{a b}``.

    Parameters
    ----------
    g : ndarray
        Covariant metric, shape ``(4, 4, ...)``.
    wf_compat : bool, default False
        If True, flip the sign of the time column ``M[:, 0]`` to match
        WarpFactory's ``getEulerianTransformationMatrix.m`` convention
        (past-directed timelike normal). Required for byte-level reproduction
        of the WarpFactory stress-energy anchor; physically irrelevant for
        energy condition evaluation since the diagonalised eigenvalues
        ``(rho, p_i)`` are the same.

    Decomposition: write ``g`` in ADM form with lapse ``alpha``, shift
    ``beta^i``, and spatial metric ``gamma_{ij}``:

        g_{tt} = -alpha^2 + beta_i beta^i
        g_{ti} = beta_i
        g_{ij} = gamma_{ij}

    Then a valid choice for ``M`` is

        M^t_0 = 1/alpha
        M^i_0 = -beta^i / alpha
        M^t_a = 0  for a in {1,2,3}
        M^i_a = (L^{-T})^i_a  where L L^T = gamma

    so that the time column maps to the future-directed unit normal ``n^mu``
    and the spatial columns are orthonormal and orthogonal to ``n^mu``.
    """
    # Spatial 3-metric and shift
    gamma = np.empty(g.shape[2:] + (3, 3), dtype=np.float64)
    for i in range(3):
        for j in range(3):
            gamma[..., i, j] = g[1 + i, 1 + j]
    beta_lower = np.stack([g[0, 1], g[0, 2], g[0, 3]], axis=-1)  # (..., 3)

    # Invert gamma to get gamma^{ij} -> beta^i = gamma^{ij} beta_j
    gamma_inv = np.linalg.inv(gamma)
    beta_upper = np.einsum("...ij,...j->...i", gamma_inv, beta_lower)

    # Lapse: g_{tt} = -alpha^2 + beta_i beta^i  =>  alpha^2 = beta_i beta^i - g_{tt}
    alpha2 = np.einsum("...i,...i->...", beta_lower, beta_upper) - g[0, 0]
    alpha = np.sqrt(alpha2)

    # Cholesky of spatial 3-metric: gamma = L L^T
    L = np.linalg.cholesky(gamma)
    # We need M^i_a such that g_ij M^i_a M^j_b = delta_{ab}, i.e. M = L^{-T}
    Linv = np.linalg.inv(L)
    M_spatial = np.swapaxes(Linv, -1, -2)  # L^{-T}, shape (..., 3, 3)

    # Assemble M: shape (4, 4, ...)
    M = np.zeros((4, 4) + g.shape[2:], dtype=np.float64)
    M[0, 0] = 1.0 / alpha
    for i in range(3):
        M[1 + i, 0] = -beta_upper[..., i] / alpha
        for a in range(3):
            M[1 + i, 1 + a] = M_spatial[..., i, a]
    if wf_compat:
        M[:, 0] *= -1.0
    return M


def to_eulerian(T_lower: np.ndarray, M: np.ndarray) -> np.ndarray:
    """Convert a covariant rank-2 tensor ``T_{mu nu}`` to the Eulerian frame:

        T^{(E)}_{ab} = M^mu_a M^nu_b T_{mu nu}.

    Note: indices ``a, b`` are local-Lorentz indices (frame components).
    """
    return np.einsum("ma...,nb...,mn...->ab...", M, M, T_lower)
