"""Task 2D.5e (Session 42): closed-form FH principal pressures via axisymmetry.

The Session-14c Hard Fix (FELL_HEISENBERG_SWEEP_NOTES Sec. 12) built and
validated the symbolic FH stress tensor S_ij(X, Y, Z; params) but hit an
intractable wall at symbolic eigenvalue extraction: det(S) for the full 3x3
Cartesian matrix never terminates in SymPy (Sec. 12.2). Sub-tasks 4-6 were
cancelled and the Sec. 12.8 "Z-axis fallback" (eigenvalues on the axis only)
was left un-attempted.

This module implements something strictly stronger than the Sec. 12.8 plan,
from an observation the Cartesian attempt missed: **the concrete FH potential
is exactly axisymmetric about Z** -- phi depends on (X, Y) only through
X^2 + Y^2 (the m, n asymmetry functions depend on Z alone; they break
fore-aft z -> -z symmetry, not axial symmetry). Consequently:

  * On the half-plane Y = 0 (which covers all of space up to a rotation),
    the parity Y -> -Y forces S_xy = S_yz = 0, so S block-diagonalises into
    the azimuthal component S_yy and a 2x2 (x, z) block.
  * The principal pressures are therefore CLOSED FORM everywhere:

        lam_phi   = S_yy
        lam_pm    = (S_xx + S_zz)/2 +/- sqrt(((S_xx - S_zz)/2)^2 + S_xz^2)

    -- no 3x3 determinant is ever needed (det S = S_yy (S_xx S_zz - S_xz^2)
    factors trivially in the block basis). The Sec. 12.2 wall was an artifact
    of ignoring the symmetry, not a property of the ansatz.
  * The full WEC/DEC slack fields on the (R_cyl, Z) half-plane are then
    closed-form combinations of {rho_E, lam_phi, lam_+, lam_-}, and the
    Sec. 12.8 Z-axis reduction is the R_cyl -> 0 specialisation (where
    additionally S_xz -> 0 and S_xx -> S_yy).

Everything is built on the validated Session-14c symbolic pipeline
(hf_jobs/analysis/fell_heisenberg_symbolic.py, checkpoints A/B).
Verification gates live in verification/test_fh_axisym_closed_form.py.
"""
from __future__ import annotations

import numpy as np
import sympy as sp

from hf_jobs.analysis.fell_heisenberg_symbolic import (
    get_syms,
    symbolic_phi,
    symbolic_hessian,
    symbolic_K_and_rho_E,
    symbolic_S_ij,
)

_SYMS = get_syms()
X_s, Y_s, Z_s = _SYMS['X'], _SYMS['Y'], _SYMS['Z']
# NOTE: Pi is FIXED at Rational(1, 4) inside the Session-14c symbolic module
# (fell_heisenberg_symbolic.Pi_s is a number, not a Symbol), so it is not a
# lambdify argument here.
PARAM_ORDER = ('V', 'sigma', 'm0', 'a', 'ell', 'r')


def build_y0_closed_form(epsilon: float = 1e-30) -> dict:
    """Build the closed-form y=0-plane quantities from the validated pipeline.

    Returns a dict of SymPy expressions in (X, Z; V, sigma, m0, a, ell, r, Pi)
    -- X plays the role of the cylindrical radius R_cyl >= 0:

      rho_E, S_xx, S_yy, S_zz, S_xz    components on the y=0 plane
      S_xy, S_yz                       (retained for the zero-certificate)
      lam_phi, lam_plus, lam_minus     closed-form principal pressures

    epsilon > 0 gives the numerically-safe R^2 + eps regularisation used by
    the numerical pipeline (pass 0 for pure symbolic work).
    """
    phi = symbolic_phi(epsilon=epsilon)
    H = symbolic_hessian(phi)
    K, rho_E = symbolic_K_and_rho_E(H)
    S = symbolic_S_ij(phi, K, rho_E)

    sub0 = {Y_s: 0}
    S_xx = S[0, 0].subs(sub0)
    S_yy = S[1, 1].subs(sub0)
    S_zz = S[2, 2].subs(sub0)
    S_xz = S[0, 2].subs(sub0)
    S_xy = S[0, 1].subs(sub0)
    S_yz = S[1, 2].subs(sub0)
    rho0 = rho_E.subs(sub0)

    half_sum = (S_xx + S_zz) / 2
    half_diff = (S_xx - S_zz) / 2
    disc = sp.sqrt(half_diff ** 2 + S_xz ** 2)
    lam_plus = half_sum + disc
    lam_minus = half_sum - disc

    return {
        'phi': phi,
        'rho_E': rho0,
        'S_xx': S_xx, 'S_yy': S_yy, 'S_zz': S_zz, 'S_xz': S_xz,
        'S_xy': S_xy, 'S_yz': S_yz,
        'lam_phi': S_yy, 'lam_plus': lam_plus, 'lam_minus': lam_minus,
    }


def lambdify_y0(cf: dict) -> dict:
    """Lambdify the y=0 closed-form set. Each callable takes
    (X, Z, V, sigma, m0, a, ell, r, Pi) with X, Z broadcastable arrays."""
    args = (X_s, Z_s) + tuple(_SYMS[p] for p in PARAM_ORDER)
    out = {}
    for name in ('rho_E', 'S_xx', 'S_yy', 'S_zz', 'S_xz', 'S_xy', 'S_yz',
                 'lam_phi', 'lam_plus', 'lam_minus'):
        # 'scipy' first so erf maps to scipy.special.erf (array-capable);
        # plain 'numpy' would fall back to math.erf and break on arrays
        out[name] = sp.lambdify(args, cf[name], modules=['scipy', 'numpy'])
    return out


def slack_fields_y0(fns: dict, Xg, Zg, params: dict):
    """Evaluate closed-form WEC/DEC slack fields on a (R_cyl, Z) mesh.

    wec_slack = rho_E + min(lam_i);  dec_slack = rho_E - max|lam_i|
    (identical definitions to fell_heisenberg.py evaluate()).
    """
    p = tuple(float(params[k]) for k in PARAM_ORDER)
    with np.errstate(all='ignore'):
        rho = fns['rho_E'](Xg, Zg, *p)
        lam1 = fns['lam_phi'](Xg, Zg, *p)
        lam2 = fns['lam_plus'](Xg, Zg, *p)
        lam3 = fns['lam_minus'](Xg, Zg, *p)
    lam_min = np.minimum(np.minimum(lam1, lam2), lam3)
    lam_absmax = np.maximum(np.maximum(np.abs(lam1), np.abs(lam2)), np.abs(lam3))
    return {
        'rho_E': rho,
        'wec_slack': rho + lam_min,
        'dec_slack': rho - lam_absmax,
        'lams': (lam1, lam2, lam3),
    }


def build_axis_closed_form(cf: dict) -> dict:
    """Sec. 12.8 deliverable: the Z-axis (R_cyl -> 0) specialisation.

    On the axis the block collapses further: S_xz -> 0 and S_xx -> S_yy by
    axisymmetric regularity, so the principal pressures are the diagonal
    entries {S_xx = S_yy (transverse, double), S_zz (longitudinal)} and the
    slack expressions are 1-D closed forms in Z.
    """
    sub_axis = {X_s: 0}
    return {
        'rho_E_axis': cf['rho_E'].subs(sub_axis),
        'p_perp_axis': cf['S_yy'].subs(sub_axis),
        'p_long_axis': cf['S_zz'].subs(sub_axis),
        'S_xz_axis': cf['S_xz'].subs(sub_axis),   # zero-certificate target
        'S_xx_axis': cf['S_xx'].subs(sub_axis),   # equality-certificate target
    }


def lambdify_axis(ax: dict) -> dict:
    args = (Z_s,) + tuple(_SYMS[p] for p in PARAM_ORDER)
    return {name: sp.lambdify(args, expr, modules=['scipy', 'numpy'])
            for name, expr in ax.items()}
