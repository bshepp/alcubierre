"""Exact (observer-robust) pointwise energy-condition minima.

Session 58 (2026-10-16). Companion to :mod:`energy_conditions`, which forms
the EC verdict from WarpFactory's *sampled* vector field (``num_angular``
Fibonacci directions x ``num_temporal`` speeds). A finite sample is an UPPER
bound on the true minimum over observers, so a sampled margin is optimistic;
the Session-58 probe measured a near-constant bias of ~0.13 % of the
rho c^2 scale at the canonical Fuchs cell (100x10 field), which moved the
S32 single-shell floor by +0.1 %. Le 2026a (arXiv:2602.18023) makes the same
point for warp spacetimes generally. This module removes the sampling.

All inputs are covariant components ``T_ab`` in the Eulerian orthonormal
frame, shape ``(4, 4, ...)``, with eta = diag(-1, 1, 1, 1). Conventions
match :func:`energy_conditions.evaluate_energy_conditions` so numbers are
comparable with the project's recorded margins:

* **null**: ``min_n T_ab V^a V^b`` over ``V = (1, n)/sqrt 2``, ``|n| = 1``.
  Exact: ``(T00 + 2 b.n + n^T A n)/2`` minimised on the unit sphere, where
  ``b_i = T_0i``, ``A = T_ij`` -- a trust-region subproblem solved through the
  secular equation in the eigenbasis of ``A`` (hard case included).
* **weak**: ``min_V T_ab V^a V^b / (V.V)_E`` over Euclidean-normalised
  ``V = (1, v)``, ``|v| <= 1`` -- the closure of the project's timelike family.
  This is the Euclidean Rayleigh quotient of the symmetric 4x4 matrix ``T``
  restricted to the cone ``|v| <= 1``: its interior critical points are the
  Euclidean eigenvectors of ``T`` lying inside the cone, and the boundary
  value is the null minimum, so the exact minimum is the smaller of the two.
* **strong**: same with the trace-reversed ``T_eff = T - 1/2 (eta^{ab}T_ab) eta``.
* **dominant**: the project's scalar ``-max_n sign(J.J) sqrt|J.J|`` with
  ``J^a = -T^a_b V^b``, ``V = (1, n)/sqrt 2`` null, i.e. ``J.J = V^T (T eta T) V``
  -- a second sphere trust-region problem (maximised). The future-directedness
  requirement ``J^0 >= 0`` (``T00 >= |b|``) is returned separately as
  ``dominant_future`` (negative = past-directed flux exists).
* **type_I**: Hawking-Ellis Type I mask (eta T has four real eigenvalues and a
  timelike eigenvector), reported for context; the minima above do NOT depend
  on the classification.

Negative = violation, as in WarpFactory and the rest of the project.
"""

from __future__ import annotations

import numpy as np

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])


# --------------------------------------------------------------------------
# Trust-region subproblem on the unit sphere:  min_{|n|=1} n^T A n + 2 b^T n
# --------------------------------------------------------------------------

def sphere_quadratic_min(A: np.ndarray, b: np.ndarray, *, iters: int = 80):
    """Exact global minimum of ``n^T A n + 2 b^T n`` on the unit sphere.

    ``A``: (P, 3, 3) symmetric; ``b``: (P, 3). Returns ``(value, n_star)``
    with shapes (P,), (P, 3).

    Theory (Gander-Golub-von Matt / More-Sorensen): the global minimiser is
    ``n = -(A - lam I)^{-1} b`` with ``lam`` the smallest root of the secular
    equation ``sum_i beta_i^2/(lam_i - lam)^2 = 1`` (``beta = Q^T b`` in the
    eigenbasis ``A = Q diag(lam_i) Q^T``), which lies in ``(-inf, lam_1]``.
    On that interval ``phi(lam) = sum beta_i^2/(lam_i-lam)^2 - 1`` is
    increasing from -1 to +inf (if ``beta_1 != 0``), so bisection is safe.
    Hard case (``beta_1 ~ 0``): if ``phi(lam_1^-) < 0`` the root is
    ``lam = lam_1`` with a free component along ``e_1`` fixing ``|n| = 1``.
    """
    A = np.asarray(A, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    P = A.shape[0]
    lam, Q = np.linalg.eigh(A)                       # (P,3) ascending, (P,3,3)
    beta = np.einsum("pij,pi->pj", Q, b)             # Q^T b   (P,3)
    scale = np.maximum(np.abs(lam).max(axis=1), np.linalg.norm(beta, axis=1))
    scale = np.where(scale > 0, scale, 1.0)
    lam1 = lam[:, 0]
    # hard-case detection: beta_1 negligible AND the remaining components
    # cannot reach the sphere at lam = lam_1.
    eps = 1e-13 * scale
    beta1_small = np.abs(beta[:, 0]) <= eps
    with np.errstate(divide="ignore", invalid="ignore"):
        rest = (beta[:, 1:] ** 2 / np.maximum(lam[:, 1:] - lam1[:, None], 1e-300) ** 2).sum(axis=1)
    hard = beta1_small & (rest < 1.0)

    # --- regular case: bisection for lam in (lo, hi) with hi -> lam1^-
    hi = lam1 - 1e-14 * scale
    # lower bracket: phi(lo) < 0 guaranteed when |beta|/(lam_i - lo) < 1/sqrt3 for all i
    lo = lam1 - np.sqrt(3.0) * np.linalg.norm(beta, axis=1) - 1e-12 * scale
    lo = np.minimum(lo, hi - 1e-12 * scale)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        phi = (beta ** 2 / (lam - mid[:, None]) ** 2).sum(axis=1) - 1.0
        go_up = phi < 0.0
        lo = np.where(go_up, mid, lo)
        hi = np.where(go_up, hi, mid)
    lam_star = 0.5 * (lo + hi)
    n_eig = -beta / (lam - lam_star[:, None])        # components in eigenbasis
    # --- hard case: lam = lam1, n = -(beta_i/(lam_i - lam1)) e_i (i>1) + t e_1
    if hard.any():
        nh = np.zeros_like(n_eig)
        with np.errstate(divide="ignore", invalid="ignore"):
            nh[:, 1:] = -beta[:, 1:] / np.maximum(lam[:, 1:] - lam1[:, None], 1e-300)
        t = np.sqrt(np.maximum(1.0 - (nh[:, 1:] ** 2).sum(axis=1), 0.0))
        nh[:, 0] = t
        # the two signs of t give the same value when beta_1 = 0; pick +
        n_eig = np.where(hard[:, None], nh, n_eig)
    # renormalise to kill bisection residue, rotate back
    n_eig /= np.maximum(np.linalg.norm(n_eig, axis=1, keepdims=True), 1e-300)
    n_star = np.einsum("pij,pj->pi", Q, n_eig)
    value = np.einsum("pi,pij,pj->p", n_star, A, n_star) + 2.0 * np.einsum("pi,pi->p", b, n_star)
    return value, n_star


# --------------------------------------------------------------------------
# Cone-restricted Rayleigh quotient:  min_{|v|<=1} (T00 + 2 b.v + v^T A v)/(1+|v|^2)
# --------------------------------------------------------------------------

def _cone_rayleigh_min(T4: np.ndarray, null_half: np.ndarray):
    """``T4``: (P,4,4) symmetric (Euclidean matrix of the quadratic form in
    V=(1,v)). ``null_half``: (P,) the exact null minimum in the (1,n)/sqrt2
    normalisation (= boundary value of the Rayleigh quotient).
    Interior critical points are Euclidean eigenvectors with |v| < |V0|."""
    w, U = np.linalg.eigh(T4)                        # ascending
    V0 = U[:, 0, :]                                  # (P,4): time components of eigenvectors
    vs = np.linalg.norm(U[:, 1:, :], axis=1)         # (P,4): spatial norms
    inside = vs < np.abs(V0) * (1.0 - 1e-12)
    w_in = np.where(inside, w, np.inf)
    interior_min = w_in.min(axis=1)
    return np.minimum(interior_min, null_half)


# --------------------------------------------------------------------------
# Public evaluator
# --------------------------------------------------------------------------

def evaluate_energy_conditions_exact(T_eul: np.ndarray) -> dict[str, np.ndarray]:
    """Exact per-point EC minima for Eulerian-frame covariant ``T_ab``.

    ``T_eul`` shape ``(4, 4, ...)``. Returns a dict with keys
    ``null, weak, dominant, strong`` (same conventions as the sampled
    evaluator, negative = violation), ``dominant_future`` (``T00 - |b|``,
    negative = a past-directed energy flux exists for some null observer),
    ``type_I`` (bool mask) and ``n_null`` (the minimising null direction,
    shape ``(3, ...)``).
    """
    T = np.asarray(T_eul, dtype=np.float64)
    shp = T.shape[2:]
    Tp = np.moveaxis(T.reshape(4, 4, -1), -1, 0)     # (P,4,4)
    P = Tp.shape[0]
    T00 = Tp[:, 0, 0]
    b = Tp[:, 0, 1:]
    A = Tp[:, 1:, 1:]

    # NEC: exact sphere minimum, project normalisation (1,n)/sqrt2 -> /2
    q, n_star = sphere_quadratic_min(A, b)
    null = 0.5 * (T00 + q)

    # WEC: cone-restricted Rayleigh quotient of the Euclidean matrix T
    weak = _cone_rayleigh_min(Tp, null)

    # SEC: trace-reversed
    trace = -T00 + A[:, 0, 0] + A[:, 1, 1] + A[:, 2, 2]
    Teff = Tp - 0.5 * trace[:, None, None] * ETA[None]
    qe, _ = sphere_quadratic_min(Teff[:, 1:, 1:], Teff[:, 0, 1:])
    null_eff = 0.5 * (Teff[:, 0, 0] + qe)
    strong = _cone_rayleigh_min(Teff, null_eff)

    # DEC (project scalar): J.J = V^T (T eta T) V maximised over null V
    Qm = np.einsum("pab,bc,pcd->pad", Tp, ETA, Tp)   # T eta T  (P,4,4)
    qneg, _ = sphere_quadratic_min(-Qm[:, 1:, 1:], -Qm[:, 0, 1:])
    jj_max = 0.5 * (Qm[:, 0, 0] - qneg)
    dominant = -np.sign(jj_max) * np.sqrt(np.abs(jj_max))
    dominant_future = T00 - np.linalg.norm(b, axis=1)

    # Hawking-Ellis Type I mask (context only)
    Tm = np.einsum("ac,pcb->pab", ETA, Tp)
    w, v = np.linalg.eig(Tm)
    wscale = np.maximum(np.abs(w).max(axis=1), 1e-300)
    real = np.all(np.abs(w.imag) <= 1e-7 * wscale[:, None], axis=1)
    vn = np.einsum("pai,ab,pbi->pi", v.real, ETA, v.real)
    type_I = real & ((vn < 0).sum(axis=1) == 1)

    def back(x):
        return x.reshape(shp)

    return {
        "null": back(null), "weak": back(weak), "dominant": back(dominant),
        "strong": back(strong), "dominant_future": back(dominant_future),
        "type_I": back(type_I),
        "n_null": np.moveaxis(n_star, 0, -1).reshape((3,) + shp),
    }
