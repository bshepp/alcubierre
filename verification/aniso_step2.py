"""Phase 3.3+ Step 2 -- shared anisotropic free-profile parameterization.

Metric-first (Bobrick-Martire / Fuchs-Sec.6) formulation: alpha(r) and the
mass function m(r) are INDEPENDENTLY free in the shell; a generic static
spherically-symmetric metric then sources a generically ANISOTROPIC fluid
(P_r != P_t), automatically and in Bianchi-equilibrium. No anisotropic-TOV
solver -- the Prong-B-certified `axisymmetric_ec` evaluator computes the
exact (generically anisotropic) Einstein tensor of any (Apos,B,F) metric.

Parameterization = ONE global natural CubicSpline per quantity through a
full-window knot grid (cavity + interior + exterior). Cavity/exterior
knots are fixed to shell-appropriate values by the caller; interior knots
are free. Single C2 spline => globally smooth, NO boundary kinks (the
piecewise-splice kink at R1/R2 was the bug that produced a spurious
-5.9e42 in the gate's first cut). The Fuchs isotropic baseline is
representable in this family and reproduces the Step-1 isotropic verdict
(see aniso_step2_gate.py: 5.7% min(EC) match, sign-consistent).
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell, _compact_sigmoid,
)
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
from warp_factory_py.utils.constants import G, c

R1, R2 = 10.0, 20.0
M_TOT = 4.49e27
V, SF = 0.02, 4000.0
RHO_0 = M_TOT / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
R_LO, R_HI = 0.5, 1.5 * R2
THETA = np.linspace(0.02, np.pi - 0.02, 80)

# Full-window knot grids. Index partition: cavity (<R1) | interior [R1,R2]
# | exterior (>R2). The optimizer fixes cavity/exterior knots and frees
# the interior block.
KA_R = np.concatenate([np.linspace(R_LO, R1, 4, endpoint=False),
                       np.linspace(R1, R2, 10),
                       np.linspace(R2, R_HI, 5)[1:]])
KM_R = KA_R.copy()
KB_R = np.concatenate([np.linspace(R_LO, R1, 3, endpoint=False),
                       np.linspace(R1, R2, 7),
                       np.linspace(R2, R_HI, 3)[1:]])

CAV_A = KA_R < R1 - 1e-9                 # cavity alpha-knot mask
INT_A = (KA_R >= R1 - 1e-9) & (KA_R <= R2 + 1e-9)
EXT_A = KA_R > R2 + 1e-9
CAV_M, INT_M, EXT_M = CAV_A.copy(), INT_A.copy(), EXT_A.copy()  # KM_R==KA_R
CAV_B = KB_R < R1 - 1e-9
INT_B = (KB_R >= R1 - 1e-9) & (KB_R <= R2 + 1e-9)
EXT_B = KB_R > R2 + 1e-9


def fuchs_baseline_arrays(n_r_cap=4000):
    """Constant-density isotropic Fuchs shell -> (r, Apos, B, F, alpha, m,
    M_tot) windowed to a shell-spanning range. M_tot read from g_rr in the
    clean exterior (the builder's *smoothed* ADM mass, not nominal 4.49).

    n_r_cap sets the subsampling target of the windowed radial mesh
    (default 4000 -> ~4175 points, the historical behaviour). Callers that
    need a genuinely finer radial mesh (e.g. the kill-test top rung) must
    raise it explicitly -- subsampling the default return cannot exceed it."""
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, 35.0, 35.0, 35.0),
        rho_of_r=lambda r: np.where((r >= R1) & (r <= R2), RHO_0, 0.0),
        shift_of_r=lambda r: _compact_sigmoid(r, R1, R2, 0.0, 0.0),
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=100_000,
    )
    rf = p["r"]
    idx = np.where((rf >= R_LO) & (rf <= R_HI))[0]
    sub = idx[:: max(1, idx.size // n_r_cap)]
    r = rf[sub]
    Apos = (-p["A"])[sub]
    B = p["B"][sub]
    F = p["shift"][sub]
    alpha = 0.5 * np.log(np.maximum(Apos, 1e-300))
    m = (r * c**2 / (2.0 * G)) * (1.0 - 1.0 / np.maximum(B, 1e-300))
    M_tot = float(np.interp(1.3 * R2, r, m))
    return r, Apos, B, F, alpha, m, M_tot


def profiles_from_knots(r, alpha_knots, m_knots, beta_knots):
    """(Apos, B, F) from full-window knot vectors via single C2 splines.

    m clamped >= 0; B from g_rr with a horizon guard (returns also the
    minimum horizon factor so the caller can penalise 2Gm/rc^2 -> 1)."""
    a_cs = CubicSpline(KA_R, np.asarray(alpha_knots, float), bc_type="natural")
    m_cs = CubicSpline(KM_R, np.asarray(m_knots, float), bc_type="natural")
    b_cs = CubicSpline(KB_R, np.clip(beta_knots, 0.0, 1.0), bc_type="natural")
    mm = np.clip(m_cs(r), 0.0, None)
    raw = 1.0 - 2.0 * G * mm / (np.maximum(r, 1e-9) * c**2)
    horizon_min = float(raw.min())
    fac = np.clip(raw, 1e-12, None)
    Apos = np.exp(2.0 * a_cs(r))
    B = 1.0 / fac
    F = np.clip(b_cs(r), 0.0, 1.0)
    return Apos, B, F, horizon_min


def eval_ec(r, Apos, B, F, na=100, nt=10, theta=None):
    """Certified radial evaluator -> (min, by_cond dict, T_eul, theta_used).

    `theta` defaults to the module THETA (80 pts, for full-res
    verification); the optimizer loop passes a coarser theta for speed.
    Exact symbolic curvature => mesh density affects only min-localization
    / spline-deriv resolution, never correctness."""
    th = THETA if theta is None else theta
    res = evaluate_axisym_ec(
        r, Apos, B, F, v=V, theta=th,
        in_shell_mask_1d=(r >= R1) & (r <= R2),
        num_angular=na, num_temporal=nt,
    )
    return res["min"], res["min_by_cond"], res["T_eul"], th


def warm_start_knots():
    """Baseline knot vector + its M_tot (the cost=1 warm start)."""
    r, _, _, F0, alpha0, m0, M_tot0 = fuchs_baseline_arrays()
    ak = np.interp(KA_R, r, alpha0)
    mk = np.interp(KM_R, r, m0)
    bk = np.interp(KB_R, r, F0)
    return ak, mk, bk, M_tot0, r
