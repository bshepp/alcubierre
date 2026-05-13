"""Christoffel symbols of the second kind.

Gamma^sigma_{mu nu} = 1/2 g^{sigma rho} (d_mu g_{rho nu} + d_nu g_{rho mu}
                                        - d_rho g_{mu nu})

Mirrors WarpFactory ``getChristoffelSym`` (independent NumPy rewrite using
einsum).
"""

from __future__ import annotations

import numpy as np


def christoffel(g_inv: np.ndarray, dg: np.ndarray) -> np.ndarray:
    """Returns ``Gamma`` of shape ``(4, 4, 4, ...)`` indexed
    ``[sigma, mu, nu, ...grid]``.

    Parameters
    ----------
    g_inv : (4, 4, ...) inverse metric
    dg    : (4, 4, 4, ...) partials, ``dg[alpha, mu, nu] = d_alpha g_{mu nu}``
    """
    # term1[mu, rho, nu] = d_mu g_{rho nu}  -> permute (alpha, mu, nu) -> (mu, rho=alpha-renamed, nu)
    # We need:
    #   T_{mu nu rho}^{(1)} = d_mu g_{rho nu}  = dg[mu, rho, nu]
    #   T_{mu nu rho}^{(2)} = d_nu g_{rho mu}  = dg[nu, rho, mu]
    #   T_{mu nu rho}^{(3)} = d_rho g_{mu nu}  = dg[rho, mu, nu]
    t1 = np.transpose(dg, (0, 1, 2) + tuple(range(3, dg.ndim)))  # = dg, indices (alpha, mu, nu)
    # Build (mu, nu, rho)-indexed combination directly via einsum-like swaps:
    # We index dg as dg[a, m, n]. Map:
    #   t1[mu, nu, rho] := dg[mu, rho, nu]   -> swap (a, m, n) so a->mu, m->rho, n->nu
    t1 = np.einsum("amn...->man...", dg)  # produce dg[mu, rho, nu] with axes (mu, rho, nu, ...)
    # Need (mu, nu, rho); transpose (mu, rho, nu) -> (mu, nu, rho)
    t1 = np.swapaxes(t1, 1, 2)  # now (mu, nu, rho, ...)

    #   t2[mu, nu, rho] := dg[nu, rho, mu]
    t2 = np.einsum("amn...->nam...", dg)  # produce dg[a=mu? let's just do indexing]
    # Cleaner: build by direct transpose
    # dg has axes (alpha, mu, nu). We want result axes (Mu, Nu, Rho) with values dg[Nu, Rho, Mu].
    # So Mu corresponds to dg axis 2, Nu to axis 0, Rho to axis 1.
    t2 = np.transpose(dg, (2, 0, 1) + tuple(range(3, dg.ndim)))

    #   t3[mu, nu, rho] := dg[rho, mu, nu]
    # Mu->axis1, Nu->axis2, Rho->axis0
    t3 = np.transpose(dg, (1, 2, 0) + tuple(range(3, dg.ndim)))

    # Recompute t1 cleanly via transpose:
    #   t1[mu, nu, rho] := dg[mu, rho, nu]
    # Mu->axis0, Nu->axis2, Rho->axis1
    t1 = np.transpose(dg, (0, 2, 1) + tuple(range(3, dg.ndim)))

    bracket = t1 + t2 - t3  # shape (4, 4, 4, ...) indexed (mu, nu, rho, ...)

    # Gamma^sigma_{mu nu} = 1/2 g^{sigma rho} bracket_{mu nu rho}
    gamma = 0.5 * np.einsum("sr...,mnr...->smn...", g_inv, bracket)
    return gamma
