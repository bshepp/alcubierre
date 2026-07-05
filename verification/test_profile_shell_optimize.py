"""Phase 3.3+ Step 1: isotropic radial-profile optimization (Fuchs Sec. 6).

Question (Fuchs et al. 2024 Sec. 6): can replacing the constant-density
top-hat rho(r) and the compact-sigmoid shift form factor beta(r) with freely
optimized radial profiles reduce the required shell mass -- "possibly by
orders of magnitude" -- while all four energy conditions still pass strictly
in-shell, at the SAME warp performance (same v_warp, same warp band, full
shift delivered to the passenger volume r < R1)?

Construction
------------
* rho(r): cubic spline through K_RHO knots at fixed radii in [R1, R2], knot
  values bounded [0, RHO_MAX]; clamped >= 0 and supported on [R1, R2] by the
  builder. M_tot = integral 4 pi rho r^2 dr is the *objective* (minimize).
* beta(r): warp performance is PINNED -- beta = 1 for r <= R1 (passenger sees
  full v_warp), beta = 0 for r >= R2 (compact support), and the RAMP across
  [R1, R2] is a cubic spline through K_BETA knots bounded [0, 1]. Only the
  wall-ramp shape is free; the delivered shift is not.
* P(r): TOV-pinned (isotropic perfect fluid, P(R2)=0) by the builder. Not a
  free DOF -- this is the *isotropic* Step 1. Anisotropic P_r != P_t is the
  separate Step 2.

Objective (scalarized, gradient-free Powell)
--------------------------------------------
    cost = M_tot / M_REF  +  PENALTY * relu( -min_EC / EC_SCALE )
where min_EC is the worst of {NEC,WEC,DEC,SEC} over the FD-trimmed in-shell
mask. Feasible baseline (flat rho + sigmoid) has cost = 1 by construction;
any EC-passing mass reduction drives cost < 1; any EC violation is dominated
by the large PENALTY. M_REF / EC_SCALE are measured on the SAME coarse grid
through the SAME builder (apples-to-apples with the optimizer pipeline).

Compute discipline
------------------
Optimizer loop runs on a coarse Cartesian grid (fast eval_metric) but the
1-D radial pipeline keeps r_sample_res=100_000 and smooth_factor=4000 so the
PHYSICAL smoothing length (window * rsample-spacing) is unchanged from the
canonical builder -- coarsening only the Cartesian grid, never the radial
profile resolution. The best point is then re-verified on the canonical
(1, 300, 300, 5) grid at dx=0.2 (identical to the Sessions 26-27 sweeps).
"""

from __future__ import annotations

import time
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell,
    _compact_sigmoid,
)
from warp_factory_py.solvers.evaluator import eval_metric

# --- canonical Fuchs config (identical to Sessions 26-27) -------------------
M_TOT = 4.49e27
R1 = 10.0
R2 = 20.0
SF = 4000.0
V = 0.02
RSAMP = 100_000
RHO_0 = M_TOT / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))

# --- parameterization -------------------------------------------------------
K_RHO = 6
K_BETA = 6
RHO_MAX = 4.0 * RHO_0
RHO_KNOTS_R = np.linspace(R1, R2, K_RHO)
BETA_KNOTS_R = np.linspace(R1, R2, K_BETA)

# --- objective weights ------------------------------------------------------
PENALTY = 1.0e3

# --- grids ------------------------------------------------------------------
# Optimizer loop: dx=0.4 (132^2x5). A resolution scan with an axis-avoiding
# center offset confirmed the flat baseline is FEASIBLE at every dx in
# [0.2, 0.4] (min(EC) +3.5e38..+6.2e38, pass=1.0); dx=0.4 is the cheapest
# (~2.8 s/eval) and still feasible. The +0.37*dx offset keeps every grid
# point off the z-axis / origin (an exact axis hit makes the spherical
# metric singular -> np.linalg.inv raises).
_CDX = 0.4
_CN = 132
_COFF = 0.37 * _CDX
COARSE_GRID = (1, _CN, _CN, 5)
COARSE_GS = (1.0, _CDX, _CDX, _CDX)
COARSE_WC = (0.0, _CN * _CDX / 2 + _COFF, _CN * _CDX / 2 + _COFF, 2.5 * _CDX + _COFF)
# Canonical verification grid: identical to the Sessions 26-27 sweeps.
CANON_GRID = (1, 300, 300, 5)
CANON_GS = (1.0, 0.2, 0.2, 0.2)
CANON_WC = (0.0, 30.0, 30.0, 0.5)


def make_rho_callable(rho_knots):
    cs = CubicSpline(RHO_KNOTS_R, rho_knots, bc_type="natural")

    def rho_of_r(r):
        out = cs(r)
        return np.where((r >= R1) & (r <= R2), np.maximum(out, 0.0), 0.0)

    return rho_of_r


def make_shift_callable(beta_knots):
    cs = CubicSpline(BETA_KNOTS_R, beta_knots, bc_type="natural")

    def shift_of_r(r):
        ramp = np.clip(cs(r), 0.0, 1.0)
        out = np.where(r <= R1, 1.0, np.where(r >= R2, 0.0, ramp))
        return out

    return shift_of_r


def _inshell_mask(grid, gs, wc):
    Nx, Ny, Nz = grid[1:]
    XC = (np.arange(Nx) + 1) * gs[1] - wc[1]
    YC = (np.arange(Ny) + 1) * gs[2] - wc[2]
    ZC = (np.arange(Nz) + 1) * gs[3] - wc[3]
    R = np.sqrt(XC[:, None, None] ** 2 + YC[None, :, None] ** 2 + ZC[None, None, :] ** 2)
    ish = (R >= R1) & (R <= R2)
    bd = np.zeros_like(R, dtype=bool)
    bd[2:-2, 2:-2, 1:-1] = True
    return (ish & bd)[None, :, :, :]


def evaluate(rho_knots, beta_knots, grid, gs, wc, mask, num_ang=60, num_temp=6):
    g, p = metric_profile_warp_shell(
        grid, wc,
        rho_of_r=make_rho_callable(rho_knots),
        shift_of_r=make_shift_callable(beta_knots),
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=gs, r_sample_res=RSAMP,
    )
    res = eval_metric(g, num_angular=num_ang, num_temporal=num_temp, wf_compat=False)
    ec_min = {}
    overall = np.inf
    for cond in ("null", "weak", "dominant", "strong"):
        v = res.ec[cond][mask]
        m = float(v.min())
        ec_min[cond] = (m, 1.0 - int((v < -1e-12).sum()) / v.size)
        overall = min(overall, m)
    return p["M_total"], overall, ec_min, p["horizon_min"]


_neval = 0
_best = {"cost": np.inf, "x": None}


def main():
    print("=" * 80)
    print("Phase 3.3+ Step 1 -- isotropic radial-profile optimization (Fuchs Sec. 6)")
    print(f"canonical: R1={R1} R2={R2} M_TOT={M_TOT:.3e} v={V}c sf={SF}")
    print(f"params: {K_RHO} rho knots in [0,{RHO_MAX:.2e}] + {K_BETA} beta knots in [0,1]")
    print("=" * 80)

    cmask = _inshell_mask(COARSE_GRID, COARSE_GS, COARSE_WC)

    # --- coarse-grid baseline (flat rho + sigmoid, same builder pipeline) ---
    t0 = time.time()
    rho_flat = np.full(K_RHO, RHO_0)
    beta_sig = _compact_sigmoid(BETA_KNOTS_R, R1, R2, 0.0, 0.0)
    M_REF, ec_ref, ecmin_ref, h_ref = evaluate(
        rho_flat, beta_sig, COARSE_GRID, COARSE_GS, COARSE_WC, cmask)
    EC_SCALE = abs(ec_ref) if abs(ec_ref) > 0 else 1.0e39
    print(f"\n[coarse baseline]  ({time.time()-t0:.1f}s)")
    print(f"  M_ref      = {M_REF:.4e} kg")
    print(f"  min(EC)    = {ec_ref:+.3e}   (scale for penalty normalisation)")
    print(f"  horizon    = {h_ref:.4f}")
    for c, (mn, pf) in ecmin_ref.items():
        print(f"    {c:8s} min={mn:+.3e}  pass={pf:.5f}")

    x0 = np.concatenate([rho_flat, beta_sig])
    bounds = [(0.0, RHO_MAX)] * K_RHO + [(0.0, 1.0)] * K_BETA

    def objective(x):
        global _neval
        _neval += 1
        rk = x[:K_RHO]
        bk = x[K_RHO:]
        M, ecmn, _, _ = evaluate(rk, bk, COARSE_GRID, COARSE_GS, COARSE_WC, cmask)
        pen = PENALTY * max(0.0, -ecmn / EC_SCALE)
        cost = M / M_REF + pen
        if cost < _best["cost"]:
            _best["cost"] = cost
            _best["x"] = x.copy()
        if _neval % 10 == 0 or cost < 0.999:
            print(f"  eval {_neval:4d}  M/M_ref={M/M_REF:.4f}  "
                  f"min(EC)={ecmn:+.2e}  pen={pen:.3f}  cost={cost:.4f}"
                  f"{'  <-- best' if cost == _best['cost'] else ''}")
        return cost

    print(f"\n[optimizing]  Powell, warm start = flat rho + sigmoid (cost=1 by constr.)")
    t0 = time.time()
    rranges = [b[1] - b[0] for b in bounds]
    res = minimize(
        objective, x0, method="Powell", bounds=bounds,
        options={"maxiter": 8, "maxfev": 300, "xtol": 1e-3, "ftol": 1e-4,
                 "direc": np.diag(rranges) * 0.25},
    )
    print(f"\n[optimizer done]  ({time.time()-t0:.1f}s, {_neval} evals)")
    print(f"  scipy status: {res.message}")
    print(f"  best coarse cost = {_best['cost']:.5f}  (baseline = 1.0)")

    xb = _best["x"]
    rk_b, bk_b = xb[:K_RHO], xb[K_RHO:]
    print(f"  rho knots  = {np.array2string(rk_b, precision=3, max_line_width=120)}")
    print(f"  beta knots = {np.array2string(bk_b, precision=4, max_line_width=120)}")

    # --- canonical-grid verification of the best point ---------------------
    print(f"\n[canonical verification]  grid={CANON_GRID} dx={CANON_GS[1]}")
    vmask = _inshell_mask(CANON_GRID, CANON_GS, CANON_WC)
    t0 = time.time()
    M_canon_ref, ec_canon_ref, ecm_cref, h_cref = evaluate(
        rho_flat, beta_sig, CANON_GRID, CANON_GS, CANON_WC, vmask,
        num_ang=100, num_temp=10)
    print(f"  baseline (flat+sigmoid) ({time.time()-t0:.1f}s): "
          f"M={M_canon_ref:.4e}  min(EC)={ec_canon_ref:+.3e}  horizon={h_cref:.4f}")
    for c, (mn, pf) in ecm_cref.items():
        print(f"    {c:8s} min={mn:+.3e}  pass={pf:.6f}")

    t0 = time.time()
    M_opt, ec_opt, ecm_opt, h_opt = evaluate(
        rk_b, bk_b, CANON_GRID, CANON_GS, CANON_WC, vmask,
        num_ang=100, num_temp=10)
    print(f"  optimized               ({time.time()-t0:.1f}s): "
          f"M={M_opt:.4e}  min(EC)={ec_opt:+.3e}  horizon={h_opt:.4f}")
    for c, (mn, pf) in ecm_opt.items():
        print(f"    {c:8s} min={mn:+.3e}  pass={pf:.6f}")

    print()
    print("=" * 80)
    print("DISPOSITION (canonical grid, strict in-shell EC)")
    print("=" * 80)
    mass_ratio = M_opt / M_canon_ref
    feasible = ec_opt >= -1e-12
    print(f"  M_opt / M_baseline      = {mass_ratio:.4f}  "
          f"({(1-mass_ratio)*100:+.2f}% mass change)")
    print(f"  optimized min(EC)       = {ec_opt:+.3e}  "
          f"({'PASSES' if feasible else 'VIOLATES'} strict in-shell)")
    if feasible and mass_ratio < 0.999:
        print(f"  RESULT: isotropic radial-profile optimization REDUCES required "
              f"mass by {(1-mass_ratio)*100:.1f}% at fixed warp performance with "
              f"all four ECs still passing. (Fuchs Sec. 6 partially validated; "
              f"OoM-scale only if {mass_ratio:.3f} << 1.)")
    elif feasible:
        print(f"  RESULT: optimizer found no mass reduction beyond ~0.1%; the "
              f"constant-density spherical shell is at/near the isotropic "
              f"optimum. (Stronger NEGATIVE than Sessions 26-27 -- even Fuchs's "
              f"own Sec. 6 1-D optimization does not help within isotropic GR.)")
    else:
        print(f"  RESULT: best coarse point fails strict EC at canonical "
              f"resolution -> coarse-grid optimum is a resolution artifact; "
              f"no feasible mass reduction demonstrated. Report as inconclusive "
              f"pending finer optimizer grid.")


if __name__ == "__main__":
    main()
