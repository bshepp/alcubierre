"""Jordan-frame matter tensor + energy conditions for f(R) = R + alpha R^2
on the axisymmetric warp-shell ansatz (Session 51, Task 2E.2 / Slice 6b).

The f(R) field equations rearranged for the REQUIRED matter stress:

    8 pi T_mat = f'(R) R_munu - (1/2) f(R) g_munu - (grad grad - g box) f'(R)

which for quadratic f splits exactly as

    T_mat = G_munu + alpha * C_munu,
    C_munu = 2 R Ric_munu - (1/2) R^2 g_munu - 2 (HessR_munu - g_munu boxR).

The alpha^0 part reuses the CERTIFIED GR lambdas
(:func:`axisymmetric_ec._build_lambdas`); the correction C and the Ricci
scalar come from the generated module
(:mod:`fr_correction_generated` -- per-component exact-cancelled, Session-51
one-time build; Schwarzschild max|C| ~ 7e-16, de Sitter ~ 6e-15).

Energy conditions are evaluated on T_mat through the SAME Eulerian
orthonormalisation + EC machinery as the GR path, so alpha = 0 reproduces
:func:`axisymmetric_ec.evaluate_axisym_ec` exactly and any difference is
purely the f(R) correction.

Slice scope: Jordan-frame ECs on the matter tensor (the claimed
modified-gravity loophole tested on its own terms; the Einstein-frame
conformal reading dissolves it -- see MODIFIED_GRAVITY_LIT.md). Theory
viability is reported alongside: f'(R) = 1 + 2 alpha R > 0 pointwise
(graviton not ghost) and f''(R) = 2 alpha >= 0 (scalaron non-tachyonic).
Static ansatz; radial representation; quadratic f only. alpha in m^2
(geometrized; R is 1/m^2).

Profile derivatives to 4th order come from k=5 interpolating splines on the
dense smooth profile grid; the battery's convergence gate
(verification/test_fr_matter.py) certifies the 4th-derivative accuracy on
the canonical profiles.
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

from ..utils.constants import EINSTEIN_PREFACTOR
from . import fr_correction_generated as _gen
from .axisymmetric_ec import _assemble, _build_lambdas
from .energy_conditions import evaluate_energy_conditions
from .frame import eulerian_transformation, to_eulerian


def evaluate_axisym_ec_fr(
    r_1d: np.ndarray,
    Apos_1d: np.ndarray,
    B_1d: np.ndarray,
    F_1d: np.ndarray,
    *,
    v: float,
    alpha: float,
    theta: np.ndarray,
    in_shell_mask_1d: np.ndarray | None = None,
    num_angular: int = 100,
    num_temporal: int = 10,
):
    """Jordan-frame matter ECs for one (configuration, alpha) snapshot.

    Same contract as :func:`axisymmetric_ec.evaluate_axisym_ec` plus
    ``alpha`` (m^2). Returns the usual EC dict plus:

      ``R_scalar``      (Nr, Nth) Ricci scalar field
      ``fprime_min``    min over the mesh of f'(R) = 1 + 2 alpha R
      ``viable``        bool: f' > 0 everywhere AND alpha >= 0
    """
    args_syms, idx, g_comps, _ = _build_lambdas()

    r_1d = np.asarray(r_1d, dtype=np.float64)
    theta = np.asarray(theta, dtype=np.float64)
    Nr, Nth = r_1d.size, theta.size

    def derivs(y, kmax):
        sp5 = InterpolatedUnivariateSpline(r_1d, y, k=5)
        return [y] + [sp5.derivative(k)(r_1d) for k in range(1, kmax + 1)]

    Ap = derivs(Apos_1d, 4)
    Bp = derivs(B_1d, 4)
    Fp = derivs(F_1d, 4)

    def b(a1):
        return np.broadcast_to(np.asarray(a1)[:, None], (Nr, Nth))

    R2d = np.broadcast_to(r_1d[:, None], (Nr, Nth))
    TH2d = np.broadcast_to(theta[None, :], (Nr, Nth))
    grid_shape = (Nr, Nth)

    # GR part: certified lambdas (2nd-order args only)
    mesh_gr = (
        b(Ap[0]), b(Ap[1]), b(Ap[2]), b(Bp[0]), b(Bp[1]), b(Bp[2]),
        b(Fp[0]), b(Fp[1]), b(Fp[2]), R2d, TH2d, float(v),
    )
    g_cov = _assemble(g_comps, mesh_gr, grid_shape)
    _, _, _, T_comps = _build_lambdas()
    G_cov = _assemble(T_comps, mesh_gr, grid_shape)

    # f(R) correction + Ricci scalar from the generated module
    args_gen = tuple(b(Ap[k]) for k in range(5)) + tuple(b(Bp[k]) for k in range(5)) \
        + tuple(b(Fp[k]) for k in range(5)) + (R2d, TH2d, float(v))
    R_scalar, comps = _gen.evaluate_all(*args_gen)
    R_scalar = np.broadcast_to(np.asarray(R_scalar, dtype=np.float64), grid_shape)
    C_cov = np.zeros((4, 4) + grid_shape, dtype=np.float64)
    for (i, j), val in comps.items():
        val = np.broadcast_to(np.asarray(val, dtype=np.float64), grid_shape)
        C_cov[i, j] = val
        if i != j:
            C_cov[j, i] = val

    T_cov = EINSTEIN_PREFACTOR * (G_cov + float(alpha) * C_cov)

    M = eulerian_transformation(g_cov, wf_compat=False)
    T_eul = to_eulerian(T_cov, M)
    ec = evaluate_energy_conditions(
        T_eul, num_angular=num_angular, num_temporal=num_temporal
    )

    if in_shell_mask_1d is not None:
        m2 = np.broadcast_to(
            np.asarray(in_shell_mask_1d, dtype=bool)[:, None], (Nr, Nth)
        )
    else:
        m2 = np.ones((Nr, Nth), dtype=bool)

    overall = np.inf
    summary = {}
    for cond in ("null", "weak", "dominant", "strong"):
        vals = ec[cond][m2]
        mn = float(vals.min()) if vals.size else np.nan
        summary[cond] = mn
        overall = min(overall, mn)

    fprime = 1.0 + 2.0 * float(alpha) * R_scalar
    fprime_min = float(fprime.min())
    return {
        "null": ec["null"], "weak": ec["weak"],
        "dominant": ec["dominant"], "strong": ec["strong"],
        "min_by_cond": summary, "min": float(overall),
        "R_scalar": R_scalar,
        "fprime_min": fprime_min,
        "viable": bool(fprime_min > 0.0 and float(alpha) >= 0.0),
    }
