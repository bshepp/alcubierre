"""Phase 3.3+ Step 1, RADIAL-FRAME redo: isotropic (rho,beta) optimization
scored against the exact-symbolic axisymmetric EC evaluator.

This replaces the Session-28 attempt that scored the optimizer against the
Cartesian eval_metric and was KILLED (the optimizer mined Cartesian
staircasing). Here the objective is warp_factory_py.solvers.axisymmetric_ec
-- exact symbolic curvature on an (r,theta) mesh, validated against flat /
Schwarzschild / Alcubierre limits and cross-checked against the Cartesian
pipeline on the constant-density baseline (both agree it is strictly
EC-feasible). There is no Cartesian grid, hence no staircasing, in the
optimization loop.

Parameterization (identical to Session 28 so results are comparable):
  * rho(r): cubic spline through 6 knots in [R1,R2], values in [0,RHO_MAX],
    clamped >=0 and supported on [R1,R2] by the builder. M_tot = the
    objective (minimize).
  * beta(r): warp performance PINNED -- beta=1 for r<=R1, beta=0 for
    r>=R2, ramp = cubic spline through 6 knots in [0,1]. Only the wall
    ramp shape is free; the delivered shift is not.
  * P(r): TOV-pinned (isotropic Step 1).
Warm start = constant-density Fuchs baseline (flat rho + sigmoid beta);
cost = 1 there by construction.

The optimum found here is NOT a result by itself -- it must then survive
the independent Cartesian high-resolution + refinement cross-check
(Task 21). Invariance across both representations is the bar.
"""

from __future__ import annotations

import json
import time
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

from warp_factory_py.metrics.warp_shell import metric_profile_warp_shell, _compact_sigmoid
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

M_TOT = 4.49e27
R1, R2, SF, V = 10.0, 20.0, 4000.0, 0.02
RHO_0 = M_TOT / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))

K_RHO = K_BETA = 6
RHO_MAX = 4.0 * RHO_0
RKR = np.linspace(R1, R2, K_RHO)
BKR = np.linspace(R1, R2, K_BETA)
PENALTY = 1.0e3

# Profile builder grid: single cell + large WC -> only the radial profiles
# in `params` are used (no Cartesian eval anywhere in the loop).
PB_GRID = (1, 1, 1, 1)
PB_WC = (0.0, 35.0, 35.0, 35.0)
PB_GS = (1.0, 1.0, 1.0, 1.0)
RSAMP = 100_000

# (r,theta) objective mesh: context window [0.5, 1.5 R2] (excludes the
# r~0 spherical-coordinate singularity), subsampled for a fast per-eval
# while keeping spline-derivative accuracy (profile smoothing length ~4 m
# >> dr ~ 7e-3 m). theta avoids the exact poles.
# Curvature is EXACT symbolic at every mesh point (no FD truncation), so
# mesh density only affects spline-derivative accuracy (profile smoothing
# length ~5 m >> dr) and how finely the min(EC) is localised -- NOT the
# correctness of the values. A coarse loop mesh is therefore safe; the
# optimum is re-evaluated at high (r,theta) resolution and then independently
# cross-checked on Cartesian (Task 21). Loop: 500 r x 40 theta ~ 1 s/eval.
R_WIN_LO, R_WIN_HI = 0.5, 1.5 * R2
N_R_EVAL = 500
THETA = np.linspace(0.02, np.pi - 0.02, 40)
THETA_FINE = np.linspace(0.01, np.pi - 0.01, 160)


def make_rho(knots):
    cs = CubicSpline(RKR, knots, bc_type="natural")
    return lambda r: np.where((r >= R1) & (r <= R2), np.maximum(cs(r), 0.0), 0.0)


def make_shift(knots):
    cs = CubicSpline(BKR, knots, bc_type="natural")
    return lambda r: np.where(r <= R1, 1.0,
                              np.where(r >= R2, 0.0, np.clip(cs(r), 0.0, 1.0)))


def radial_profiles(rho_knots, beta_knots):
    _, p = metric_profile_warp_shell(
        PB_GRID, PB_WC, rho_of_r=make_rho(rho_knots),
        shift_of_r=make_shift(beta_knots), R1=R1, R2=R2,
        smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=PB_GS, r_sample_res=RSAMP,
    )
    r_full = p["r"]
    win = (r_full >= R_WIN_LO) & (r_full <= R_WIN_HI)
    idx = np.where(win)[0]
    sub = idx[:: max(1, idx.size // N_R_EVAL)]
    r = r_full[sub]
    return (r, (-p["A"])[sub], p["B"][sub], p["shift"][sub],
            float(p["M_total"]))


def ec_min(rho_knots, beta_knots, na=40, nt=5, theta=None):
    r, Apos, B, F, M = radial_profiles(rho_knots, beta_knots)
    in_shell = (r >= R1) & (r <= R2)
    res = evaluate_axisym_ec(
        r, Apos, B, F, v=V, theta=THETA if theta is None else theta,
        in_shell_mask_1d=in_shell, num_angular=na, num_temporal=nt,
    )
    return M, res["min"], res["min_by_cond"]


_n = 0
_best = {"cost": np.inf, "x": None}


def main():
    print("=" * 80)
    print("Phase 3.3+ Step 1 RADIAL-FRAME redo (exact-symbolic objective)")
    print(f"canonical R1={R1} R2={R2} M_TOT={M_TOT:.3e} v={V}c sf={SF}")
    print("=" * 80)

    rho_flat = np.full(K_RHO, RHO_0)
    beta_sig = _compact_sigmoid(BKR, R1, R2, 0.0, 0.0)

    t0 = time.time()
    M_REF, ec_ref, ecd_ref = ec_min(rho_flat, beta_sig, na=100, nt=10)
    EC_SCALE = abs(ec_ref) if abs(ec_ref) > 0 else 1.0e39
    print(f"\n[baseline]  ({time.time()-t0:.1f}s)")
    print(f"  M_ref   = {M_REF:.4e} kg")
    print(f"  min(EC) = {ec_ref:+.3e}  ({'PASS' if ec_ref>=0 else 'FAIL'})")
    for k, vv in ecd_ref.items():
        print(f"    {k:8s} {vv:+.3e}")

    x0 = np.concatenate([rho_flat, beta_sig])
    bounds = [(0.0, RHO_MAX)] * K_RHO + [(0.0, 1.0)] * K_BETA

    def obj(x):
        global _n
        _n += 1
        M, mn, _ = ec_min(x[:K_RHO], x[K_RHO:])
        pen = PENALTY * max(0.0, -mn / EC_SCALE)
        cost = M / M_REF + pen
        if cost < _best["cost"]:
            _best["cost"] = cost
            _best["x"] = x.copy()
        if _n % 20 == 0 or cost < 0.999:
            print(f"  eval {_n:4d}  M/M_ref={M/M_REF:.4f}  min(EC)={mn:+.2e}  "
                  f"pen={pen:.3f}  cost={cost:.4f}"
                  f"{'  <-- best' if cost==_best['cost'] else ''}")
        return cost

    print(f"\n[optimizing]  Powell (radial objective; warm start cost=1)")
    t0 = time.time()
    rr = [b[1] - b[0] for b in bounds]
    res = minimize(obj, x0, method="Powell", bounds=bounds,
                   options={"maxiter": 20, "maxfev": 800,
                            "xtol": 1e-4, "ftol": 1e-5,
                            "direc": np.diag(rr) * 0.25})
    print(f"\n[done]  {time.time()-t0:.1f}s, {_n} evals; {res.message}")
    print(f"  best radial cost = {_best['cost']:.5f}  (baseline = 1.0)")

    xb = _best["x"]
    rk, bk = xb[:K_RHO], xb[K_RHO:]
    Mb, mnb, ecdb = ec_min(rk, bk, na=120, nt=12, theta=THETA_FINE)
    print(f"\n[optimum, radial re-eval @ na=120, theta x160 fine]")
    print(f"  M_opt        = {Mb:.4e} kg")
    print(f"  M_opt/M_ref  = {Mb/M_REF:.4f}  ({(1-Mb/M_REF)*100:+.2f}% mass)")
    print(f"  min(EC)      = {mnb:+.3e}  ({'PASS' if mnb>=0 else 'FAIL'})")
    for k, vv in ecdb.items():
        print(f"    {k:8s} {vv:+.3e}")
    print(f"  rho knots  = {np.array2string(rk, precision=3, max_line_width=120)}")
    print(f"  beta knots = {np.array2string(bk, precision=4, max_line_width=120)}")
    with open("agent-tools/_radial_opt_knots.json", "w") as fh:
        json.dump({"rho_knots": rk.tolist(), "beta_knots": bk.tolist(),
                   "rho_knot_r": RKR.tolist(), "beta_knot_r": BKR.tolist(),
                   "M_opt": Mb, "M_ref": M_REF, "min_EC_radial": mnb,
                   "R1": R1, "R2": R2, "v": V, "SF": SF}, fh, indent=2)
    print("\n  saved optimum -> agent-tools/_radial_opt_knots.json")
    print("  NEXT: Task 21 -- independent Cartesian high-res + refinement "
          "cross-check of this optimum (invariance across BOTH "
          "representations is the bar).")


if __name__ == "__main__":
    main()
