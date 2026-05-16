"""Task 21 -- adversarial end cross-check of the radial-frame optimum.

The Step-1 radial-frame optimizer found M_opt = 3.505e27 (-21.9% vs the
4.49e27 constant-density baseline), all four ECs passing on the exact-
symbolic axisymmetric evaluator. That is NOT a result until it survives:

  KILL TEST A -- INDEPENDENT REPRESENTATION + REFINEMENT.
    Evaluate the SAME optimum metric on the Cartesian eval_metric pipeline
    at dx in {0.40,0.30,0.20,0.15,0.12} (the Session-28 kill-test grid
    family, axis-offset so no cell is singular). Session 28's Cartesian-
    objective optimum FAILED exactly here (negative min(EC) at every
    resolution). A real result must pass on BOTH representations and stay
    passing / converge under refinement.

  KILL TEST B -- IS IT JUST FUCHS-MASS OVER-PROVISIONING?
    In the TRUSTED radial evaluator, scan a plain constant-density shell
    (flat rho + sigmoid beta, the original Fuchs design) downward in mass.
    Find the lowest mass M_cd that still passes all four ECs. If
    M_cd <= ~M_opt, the 21.9% "profile optimization" is largely just
    "the Fuchs canonical mass was over-provisioned" -- a real but weaker,
    non-profile-specific statement. The profile result only stands if the
    optimized profile passes at a mass where constant-density FAILS, by a
    meaningful margin.

Objective verdict: SURVIVES only if (A) passes both representations
convergently AND (B) M_opt is meaningfully below the constant-density
floor.
"""

from __future__ import annotations

import json
import time
import numpy as np
from scipy.interpolate import CubicSpline

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell, _compact_sigmoid,
)
from warp_factory_py.solvers.evaluator import eval_metric
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

OPT = json.load(open("F:/science-projects/alcubierre/agent-tools/_radial_opt_knots.json"))
R1, R2, V, SF = OPT["R1"], OPT["R2"], OPT["v"], OPT["SF"]
M_REF = OPT["M_ref"]
M_OPT = OPT["M_opt"]
RKR = np.array(OPT["rho_knot_r"])
BKR = np.array(OPT["beta_knot_r"])
RHO_K = np.array(OPT["rho_knots"])
BETA_K = np.array(OPT["beta_knots"])
RHO_0 = M_REF / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))


def rho_opt():
    cs = CubicSpline(RKR, RHO_K, bc_type="natural")
    return lambda r: np.where((r >= R1) & (r <= R2), np.maximum(cs(r), 0.0), 0.0)


def shift_opt():
    cs = CubicSpline(BKR, BETA_K, bc_type="natural")
    return lambda r: np.where(r <= R1, 1.0,
                              np.where(r >= R2, 0.0, np.clip(cs(r), 0.0, 1.0)))


def rho_flat(M):
    rho0 = M / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
    return lambda r: np.where((r >= R1) & (r <= R2), rho0, 0.0)


def shift_sig():
    return lambda r: _compact_sigmoid(r, R1, R2, 0.0, 0.0)


def grid_for_dx(dx):
    N = int(round(52.0 / dx))
    if N % 2:
        N += 1
    off = 0.37 * dx
    return ((1, N, N, 5), (1.0, dx, dx, dx),
            (0.0, N * dx / 2 + off, N * dx / 2 + off, 2.5 * dx + off))


def cart_inshell(grid, gs, wc):
    Nx, Ny, Nz = grid[1:]
    XC = np.arange(Nx) * gs[1] - wc[1]
    YC = np.arange(Ny) * gs[2] - wc[2]
    ZC = np.arange(Nz) * gs[3] - wc[3]
    Rr = np.sqrt(XC[:, None, None]**2 + YC[None, :, None]**2 + ZC[None, None, :]**2)
    ish = (Rr >= R1) & (Rr <= R2)
    bd = np.zeros_like(Rr, dtype=bool)
    bd[2:-2, 2:-2, 1:-1] = True
    return (ish & bd)[None, :, :, :]


def cart_minEC(rho_cb, shift_cb, dx, na=100, nt=10):
    grid, gs, wc = grid_for_dx(dx)
    g, _ = metric_profile_warp_shell(
        grid, wc, rho_of_r=rho_cb, shift_of_r=shift_cb, R1=R1, R2=R2,
        smooth_factor=SF, v_warp=V, do_warp=True, grid_scale=gs,
        r_sample_res=100_000)
    res = eval_metric(g, num_angular=na, num_temporal=nt, wf_compat=False)
    m = cart_inshell(grid, gs, wc)
    return min(float(res.ec[c][m].min())
               for c in ("null", "weak", "dominant", "strong")), grid[1]


def rad_minEC(rho_cb, shift_cb):
    g_grid = (1, 1, 1, 1)
    _, p = metric_profile_warp_shell(
        g_grid, (0.0, 35.0, 35.0, 35.0), rho_of_r=rho_cb, shift_of_r=shift_cb,
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=100_000)
    rf = p["r"]
    win = (rf >= 0.5) & (rf <= 1.5 * R2)
    idx = np.where(win)[0]
    sub = idx[:: max(1, idx.size // 1500)]
    r = rf[sub]
    res = evaluate_axisym_ec(
        r, (-p["A"])[sub], p["B"][sub], p["shift"][sub], v=V,
        theta=np.linspace(0.01, np.pi - 0.01, 160),
        in_shell_mask_1d=(r >= R1) & (r <= R2),
        num_angular=120, num_temporal=12)
    return res["min"], float(p["M_total"])


def main():
    print("=" * 80)
    print("TASK 21 -- adversarial end cross-check of the radial-frame optimum")
    print(f"M_opt={M_OPT:.4e}  M_ref={M_REF:.4e}  (-{(1-M_OPT/M_REF)*100:.1f}%)  "
          f"radial min(EC)={OPT['min_EC_radial']:+.2e}")
    print("=" * 80)

    print("\n" + "-" * 80)
    print("KILL TEST A -- independent Cartesian representation + refinement")
    print("  (Session-28 Cartesian-objective optimum FAILED this at every dx)")
    print("-" * 80)
    rows = []
    for dx in (0.40, 0.30, 0.20, 0.15, 0.12):
        t0 = time.time()
        mc, N = cart_minEC(rho_opt(), shift_opt(), dx)
        mb, _ = cart_minEC(rho_flat(M_REF), shift_sig(), dx)
        rows.append((dx, N, mc, mb))
        print(f"  dx={dx:.2f} N={N:4d}  opt min(EC)={mc:+.3e} "
              f"{'PASS' if mc >= 0 else 'FAIL'}   baseline={mb:+.3e}  "
              f"({time.time()-t0:.0f}s)")
    opt_cart = [r[2] for r in rows]
    finest = opt_cart[-1]
    all_pass = all(m >= 0 for m in opt_cart)
    if finest < 0 or not all_pass:
        testA = "KILL"
        print(f"\n  >>> KILL: optimum FAILS Cartesian EC at "
              f"{'every' if not any(m>=0 for m in opt_cart) else 'the finest'} "
              f"resolution -> not invariant across representations "
              f"(radial-evaluator-specific feature, not physics).")
    else:
        testA = "SURVIVES"
        print(f"\n  >>> SURVIVES: optimum passes Cartesian EC at ALL "
              f"resolutions dx in [0.12,0.40] (finest min(EC)={finest:+.2e}) "
              f"-> invariant across BOTH independent representations.")

    print("\n" + "-" * 80)
    print("KILL TEST B -- constant-density mass floor in the TRUSTED radial "
          "evaluator")
    print("  (is the 21.9% just Fuchs-mass over-provisioning, not profiling?)")
    print("-" * 80)
    cd_floor = None
    for M in (4.49e27, 4.0e27, 3.7e27, 3.505e27, 3.3e27, 3.0e27, 2.7e27):
        t0 = time.time()
        mn, Mt = rad_minEC(rho_flat(M), shift_sig())
        ok = mn >= 0
        if ok:
            cd_floor = M
        print(f"  const-rho M={M:.3e}  radial min(EC)={mn:+.3e}  "
              f"{'PASS' if ok else 'FAIL'}  ({time.time()-t0:.0f}s)")
    print()
    if cd_floor is not None and cd_floor <= M_OPT * 1.02:
        testB = "KILL"
        print(f"  >>> KILL: constant-density passes down to "
              f"{cd_floor:.3e} <= M_opt={M_OPT:.3e}. The 21.9% is "
              f"essentially Fuchs-mass over-provisioning, NOT a "
              f"profile-shaping effect.")
    else:
        floor_txt = f"{cd_floor:.3e}" if cd_floor else ">4.49e27"
        testB = "SURVIVES"
        print(f"  >>> SURVIVES: constant-density floor is {floor_txt} "
              f"(> M_opt={M_OPT:.3e}). The optimized PROFILE passes at a "
              f"mass where constant-density FAILS -> genuine profile effect.")

    print("\n" + "=" * 80)
    print("OBJECTIVE DISPOSITION")
    print("=" * 80)
    print(f"  Test A (cross-representation + refinement): {testA}")
    print(f"  Test B (vs constant-density mass floor)   : {testB}")
    if testA == "SURVIVES" and testB == "SURVIVES":
        print("\n  VERDICT: SURVIVES both. A genuine, slice-bounded, "
              "representation-invariant\n  profile-optimization mass "
              "reduction. Record with full scope + the\n  exact margin "
              "over the constant-density floor. Still NOT order-of-"
              "magnitude.")
    else:
        print("\n  VERDICT: KILLED / WEAKENED. Do not record as a positive "
              "profile result;\n  report the killing mechanism (and any "
              "real but weaker over-provisioning\n  sub-finding) honestly.")


if __name__ == "__main__":
    main()
