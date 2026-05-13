"""Ricci tensor and scalar.

Standard Christoffel-form (default):

    R_{mu nu} = d_lambda Gamma^lambda_{mu nu} - d_nu Gamma^lambda_{mu lambda}
                + Gamma^lambda_{lambda rho} Gamma^rho_{mu nu}
                - Gamma^lambda_{nu rho}    Gamma^rho_{mu lambda}

This is the standard textbook formula. Convergence test against analytic
SymPy Ricci on the Alcubierre metric (see
``agent-tools/diag_ricci_alcubierre_convergence.py``) confirms it converges
at 4th order in dx (rel. err. 0.18% at dx = 0.025).

WarpFactory-compat form (``ricci_tensor_wf_compat``):

    Direct second-derivative formula transcribed from WarpFactory's
    ``Solver/ricciT.m`` (commit 6c4d34e). The same convergence test reveals
    a non-vanishing plateau (~2.5% rel. err. as dx -> 0), traced to a
    duplicated term ``diff_1_gl{b,d,a} + diff_1_gl{b,d,a}`` in ricciT.m
    line ~62, which appears to be a typo for ``+ diff_1_gl{a,d,b}``. Kept
    here only for byte-level reproduction of WarpFactory's published
    Alcubierre stress-energy anchor (``warp_factory_repro/alcubierre_textbook.mat``).
    Do NOT use for production results.
"""

from __future__ import annotations

import numpy as np

from ..utils.fd_stencils import (
    fd1_4th_central,
    fd2_4th_central,
    fd2_mixed_4th_central,
)


def ricci_tensor(
    gamma: np.ndarray,
    grid_scale: tuple[float, float, float, float],
) -> np.ndarray:
    """Ricci tensor ``R_{mu nu}``, shape ``(4, 4, ...)``.

    ``gamma`` is indexed ``[sigma, mu, nu, t, x, y, z]``.
    """
    # Partials d_alpha Gamma^sigma_{mu nu} -> shape (4, 4, 4, 4, ...)
    # axis order: alpha, sigma, mu, nu. The grid axes start at position 4.
    # gamma's grid axes start at 3.
    dgam = np.empty((4,) + gamma.shape, dtype=np.float64)
    for alpha in range(4):
        dgam[alpha] = fd1_4th_central(gamma, axis=3 + alpha, dx=grid_scale[alpha])
    # dgam shape: (alpha, sigma, mu, nu, ...)

    # Term A: d_lambda Gamma^lambda_{mu nu}  -> contract alpha=sigma=lambda
    termA = np.einsum("llmn...->mn...", dgam)

    # Term B: d_nu Gamma^lambda_{mu lambda}
    # = sum_lambda  dgam[alpha=nu_index, sigma=lambda, mu, nu=lambda]
    # Need: contract sigma with nu-of-Gamma (4th index), and let alpha = output's nu.
    # dgam indexed (alpha, sigma, mu, nu) -> set sigma=nu (Gamma trace) gives
    # G_trace[alpha, mu] = sum_lambda dgam[alpha, lambda, mu, lambda]
    # then result_{mu nu} = G_trace[nu, mu]   (since alpha is differentiation index = 'nu' of output)
    G_trace = np.einsum("almb...->ab...", np.einsum("almb...->almb...", dgam) if False else
                        # direct trace of dgam over sigma & last index:
                        np.einsum("aLmL...->am...", dgam))  # noqa: E501
    # Simpler: do it directly
    G_trace = np.einsum("aLmL...->am...", dgam)  # shape (alpha, mu, ...)
    # output_{mu nu} = G_trace[nu, mu]  -> swap axes 0,1
    termB = np.swapaxes(G_trace, 0, 1)

    # Term C: Gamma^lambda_{lambda rho} Gamma^rho_{mu nu}
    # gamma_trace[rho] = sum_lambda gamma[lambda, lambda, rho]
    gamma_trace = np.einsum("LLr...->r...", gamma)  # shape (rho, ...)
    termC = np.einsum("r...,rmn...->mn...", gamma_trace, gamma)

    # Term D: Gamma^lambda_{nu rho} Gamma^rho_{mu lambda}
    termD = np.einsum("Lnr...,rmL...->mn...", gamma, gamma)

    R = termA - termB + termC - termD
    # Manifest symmetrisation: continuum R is symmetric, but compounded FD on
    # FD on metric leaves residual asymmetry; symmetrise to recover this.
    return 0.5 * (R + np.swapaxes(R, 0, 1))


def ricci_scalar(g_inv: np.ndarray, R_munu: np.ndarray) -> np.ndarray:
    """``R = g^{mu nu} R_{mu nu}``."""
    return np.einsum("mn...,mn...->...", g_inv, R_munu)


def ricci_tensor_wf_compat(
    g: np.ndarray,
    dg: np.ndarray,
    g_inv: np.ndarray,
    grid_scale: tuple[float, float, float, float],
) -> np.ndarray:
    """WarpFactory ``ricciT.m`` direct-second-derivative formula (NumPy port).

    Reproduces the (slightly buggy — see module docstring) Ricci tensor that
    WarpFactory uses to compute its published Alcubierre anchor. Only call
    this when explicitly reproducing the WarpFactory anchor for validation.

    Parameters
    ----------
    g : ndarray
        Covariant metric, shape ``(4, 4, ...)``.
    dg : ndarray
        First metric partials with axis layout ``(alpha, mu, nu, ...)`` where
        ``dg[alpha, mu, nu] = d_alpha g_{mu nu}``.
    g_inv : ndarray
        Inverse metric, shape ``(4, 4, ...)``.
    grid_scale : 4-tuple of float
        Spacings along (t, x, y, z).
    """
    grid_shape = g.shape[2:]
    # Build d2g[a, b, i, j] = d_a d_b g_{ij}, exploiting symmetries.
    d2g = np.zeros((4, 4, 4, 4) + grid_shape, dtype=np.float64)
    for a in range(4):
        for b in range(a, 4):
            for i in range(4):
                for j in range(i, 4):
                    val = fd2_mixed_4th_central(
                        g[i, j], axis1=a, axis2=b,
                        dx1=grid_scale[a], dx2=grid_scale[b],
                    )
                    d2g[a, b, i, j] = val
                    d2g[b, a, i, j] = val
                    d2g[a, b, j, i] = val
                    d2g[b, a, j, i] = val

    # WarpFactory indexing: diff_1_gl{i,j,k} = d_k g_{ij}  -> dg[k, i, j]
    #                       diff_2_gl{i,j,k,n} = d_k d_n g_{ij}  -> d2g[k, n, i, j]
    def D1(i, j, k):
        return dg[k, i, j]

    def D2(i, j, k, n):
        return d2g[k, n, i, j]

    R = np.zeros((4, 4) + grid_shape, dtype=np.float64)
    for i in range(4):
        for j in range(i, 4):
            R_temp = np.zeros(grid_shape, dtype=np.float64)
            for a in range(4):
                for b in range(4):
                    R_temp_2 = -(D2(i, j, a, b) + D2(a, b, i, j)
                                 - D2(i, b, j, a) - D2(j, b, i, a))
                    for r in range(4):
                        T3 = np.zeros(grid_shape)
                        T4 = np.zeros(grid_shape)
                        T5 = np.zeros(grid_shape)
                        for d_ in range(4):
                            T3 += D1(b, d_, j) * g_inv[r, d_]
                            T4 += (D1(j, d_, b) - D1(j, b, d_)) * g_inv[r, d_]
                            # NOTE: WarpFactory ricciT.m has duplicated D1(b,d_,a)
                            # here; preserved verbatim for anchor reproduction.
                            T5 += -(D1(b, d_, a) + D1(b, d_, a)
                                    - D1(a, b, d_)) * g_inv[r, d_]
                        R_temp_2 = R_temp_2 + T4 * D1(i, r, a) + 0.5 * (
                            T3 * D1(a, r, i)
                            + T5 * (D1(j, r, i) + D1(i, r, j) - D1(j, i, r))
                        )
                    R_temp = R_temp + g_inv[a, b] * R_temp_2
            R[i, j] = 0.5 * R_temp
            if i != j:
                R[j, i] = R[i, j]
    return R
