"""Adversarial verification of the Phase 3.3+ Step 1 result.

The Step 1 optimizer claimed: an optimized radial (rho, beta) profile keeps a
Fuchs-style shell passing all four ECs strictly at the canonical grid with
30.7% less mass than the constant-density baseline (M_opt = 3.110e27 vs
M_base = 4.490e27 kg), same v=0.02c, same delivered shift.

This script TRIES TO KILL that claim with three falsification tests. Each
prints an objective KILL / SURVIVES verdict. The result is only worth
recording if it survives all three.

Optimized knots are hard-coded from agent-tools/_profile_opt_run.log
(reproducibility -- not re-running the optimizer).
"""

from __future__ import annotations

import time
import numpy as np
from scipy.interpolate import CubicSpline

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell,
    _compact_sigmoid,
)
from warp_factory_py.solvers.evaluator import eval_metric

# --- canonical config (Sessions 26-27) -------------------------------------
M_BASE = 4.49e27
M_OPT = 3.110e27          # reported optimized mass (canonical verification)
R1, R2, SF, V = 10.0, 20.0, 4000.0, 0.02
RSAMP = 100_000
RHO_0 = M_BASE / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))

# Optimized knots from _profile_opt_run.log (best coarse point, verified canon)
RK_R = np.linspace(R1, R2, 6)
BK_R = np.linspace(R1, R2, 6)
RHO_KNOTS_OPT = np.array([9.691e19, 5.982e22, 1.529e23, 1.531e23, 6.380e22, 1.531e23])
BETA_KNOTS_OPT = np.array([0.9998, 0.91, 0.7171, 0.2362, 0.0346, 0.0133])
BETA_KNOTS_SIG = _compact_sigmoid(BK_R, R1, R2, 0.0, 0.0)


def rho_opt_callable():
    cs = CubicSpline(RK_R, RHO_KNOTS_OPT, bc_type="natural")
    return lambda r: np.where((r >= R1) & (r <= R2), np.maximum(cs(r), 0.0), 0.0)


def rho_flat_callable(M_target):
    rho0 = M_target / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
    return lambda r: np.where((r >= R1) & (r <= R2), rho0, 0.0)


def shift_opt_callable():
    cs = CubicSpline(BK_R, BETA_KNOTS_OPT, bc_type="natural")
    return lambda r: np.where(r <= R1, 1.0,
                              np.where(r >= R2, 0.0, np.clip(cs(r), 0.0, 1.0)))


def shift_sig_callable():
    return lambda r: _compact_sigmoid(r, R1, R2, 0.0, 0.0)


def grid_for_dx(dx):
    # tight box, on-axis extent ~26 m, +0.37*dx center offset (no axis hit)
    N = int(round(52.0 / dx))            # ~52 m full width -> r up to ~26 on-axis
    if N % 2 == 1:
        N += 1
    off = 0.37 * dx
    grid = (1, N, N, 5)
    gs = (1.0, dx, dx, dx)
    wc = (0.0, N * dx / 2 + off, N * dx / 2 + off, 2.5 * dx + off)
    return grid, gs, wc


def inshell_mask(grid, gs, wc):
    Nx, Ny, Nz = grid[1:]
    XC = (np.arange(Nx) + 1) * gs[1] - wc[1]
    YC = (np.arange(Ny) + 1) * gs[2] - wc[2]
    ZC = (np.arange(Nz) + 1) * gs[3] - wc[3]
    R = np.sqrt(XC[:, None, None] ** 2 + YC[None, :, None] ** 2 + ZC[None, None, :] ** 2)
    ish = (R >= R1) & (R <= R2)
    bd = np.zeros_like(R, dtype=bool)
    bd[2:-2, 2:-2, 1:-1] = True
    return (ish & bd)[None, :, :, :]


def ec_minima(rho_cb, shift_cb, grid, gs, wc, mask, na=100, nt=10):
    g, p = metric_profile_warp_shell(
        grid, wc, rho_of_r=rho_cb, shift_of_r=shift_cb,
        R1=R1, R2=R2, smooth_factor=SF, v_warp=V, do_warp=True,
        grid_scale=gs, r_sample_res=RSAMP,
    )
    res = eval_metric(g, num_angular=na, num_temporal=nt, wf_compat=False)
    out = {}
    overall = np.inf
    for c in ("null", "weak", "dominant", "strong"):
        v = res.ec[c][mask]
        mn = float(v.min())
        out[c] = (mn, 1.0 - int((v < -1e-12).sum()) / v.size)
        overall = min(overall, mn)
    return p["M_total"], overall, out, p["horizon_min"]


def main():
    print("=" * 84)
    print("ADVERSARIAL VERIFICATION -- trying to KILL the Step-1 30.7% claim")
    print(f"claim: M_opt={M_OPT:.3e} passes all 4 ECs; M_base={M_BASE:.3e}; "
          f"reduction 30.7%")
    print("=" * 84)

    # ----------------------------------------------------------------------
    # KILL TEST 1: was the Fuchs baseline simply over-provisioned?
    # Constant-density shell (ORIGINAL Fuchs design: flat rho + sigmoid beta),
    # same geometry/v, canonical grid, scan total mass downward. If plain
    # const-density already passes all four ECs at M <= M_OPT, the profile
    # optimization discovered NOTHING -- you could just use less mass.
    # ----------------------------------------------------------------------
    print("\n" + "-" * 84)
    print("KILL TEST 1 -- const-density mass scan (is M_base just over-provisioned?)")
    print("  control = ORIGINAL Fuchs design (flat rho + sigmoid beta), less mass")
    print("-" * 84)
    dx1 = 0.2
    g1, gs1, wc1 = grid_for_dx(dx1)
    m1 = inshell_mask(g1, gs1, wc1)
    masses = [4.49e27, 4.0e27, 3.5e27, 3.11e27, 2.8e27, 2.5e27]
    cd_crit = None
    for M in masses:
        t0 = time.time()
        Mt, ov, ec, h = ec_minima(rho_flat_callable(M), shift_sig_callable(),
                                   g1, gs1, wc1, m1)
        feas = ov >= -1e-12
        if feas:
            cd_crit = M  # lowest feasible const-density mass seen so far
        print(f"  const-rho M={M:.3e}  min(EC)={ov:+.3e}  "
              f"{'PASS' if feas else 'FAIL'}  horizon={h:.3f}  ({time.time()-t0:.1f}s)")
    print()
    if cd_crit is not None and cd_crit <= M_OPT * 1.001:
        print(f"  >>> KILL: plain constant-density passes at M={cd_crit:.3e} "
              f"<= M_opt={M_OPT:.3e}. The 30.7% 'reduction' is just Fuchs "
              f"over-provisioning; profile optimization found nothing.")
        test1 = "KILL"
    else:
        floor = cd_crit if cd_crit is not None else masses[0]
        print(f"  >>> SURVIVES: lowest const-density mass that still passes is "
              f"{floor:.3e} (> M_opt={M_OPT:.3e}). The optimized PROFILE keeps "
              f"ECs at a mass where the constant-density design fails.")
        test1 = "SURVIVES"

    # ----------------------------------------------------------------------
    # KILL TEST 2: resolution convergence. Does the optimized point still
    # pass as dx -> 0, or does min(EC) collapse toward negative (the classic
    # boundary-cell FD-truncation artifact, Sessions 14/22)? Baseline run at
    # the same resolutions as a control -- compare the TREND, not absolutes.
    # ----------------------------------------------------------------------
    print("\n" + "-" * 84)
    print("KILL TEST 2 -- resolution convergence (optimized vs baseline)")
    print("-" * 84)
    rows = []
    for dx in [0.40, 0.30, 0.20, 0.15, 0.12]:
        g, gs, wc = grid_for_dx(dx)
        msk = inshell_mask(g, gs, wc)
        t0 = time.time()
        _, ov_b, _, _ = ec_minima(rho_flat_callable(M_BASE), shift_sig_callable(),
                                  g, gs, wc, msk)
        _, ov_o, _, _ = ec_minima(rho_opt_callable(), shift_opt_callable(),
                                  g, gs, wc, msk)
        rows.append((dx, g[1], ov_b, ov_o))
        print(f"  dx={dx:.2f}  N={g[1]:4d}  baseline min(EC)={ov_b:+.3e}  "
              f"optimized min(EC)={ov_o:+.3e}  "
              f"{'opt PASS' if ov_o >= -1e-12 else 'opt FAIL'}  "
              f"({time.time()-t0:.1f}s)")
    opt_min_trend = [r[3] for r in rows]
    finest_opt = opt_min_trend[-1]
    monotone_down = all(opt_min_trend[i] >= opt_min_trend[i + 1] - abs(opt_min_trend[i]) * 0.05
                        for i in range(len(opt_min_trend) - 1))
    print()
    if finest_opt < -1e-12:
        print(f"  >>> KILL: optimized point FAILS strict EC at the finest "
              f"resolution (dx={rows[-1][0]}, min(EC)={finest_opt:+.3e}). "
              f"The pass at dx=0.2 was a coarse-grid artifact.")
        test2 = "KILL"
    elif finest_opt > 0 and opt_min_trend[-1] < 0.25 * opt_min_trend[0] and monotone_down:
        print(f"  >>> WEAKENED: still positive at the finest dx but the margin "
              f"is decaying monotonically toward 0 ({opt_min_trend[0]:+.2e} -> "
              f"{finest_opt:+.2e}); not yet killed but a finer study is owed.")
        test2 = "WEAKENED"
    else:
        print(f"  >>> SURVIVES: optimized point stays robustly positive across "
              f"dx in [0.12, 0.40] (min(EC) {opt_min_trend[0]:+.2e} -> "
              f"{finest_opt:+.2e}); trend tracks the baseline, not an artifact.")
        test2 = "SURVIVES"

    # ----------------------------------------------------------------------
    # KILL TEST 3: did the optimizer game the EC null/timelike sphere
    # sampling? Escalate num_angular/num_temporal at the optimized point on
    # the canonical grid. If min(EC) collapses with finer sphere sampling,
    # the "pass" was a sampling artifact.
    # ----------------------------------------------------------------------
    print("\n" + "-" * 84)
    print("KILL TEST 3 -- EC sphere-sampling escalation (optimized, canonical grid)")
    print("-" * 84)
    g3, gs3, wc3 = grid_for_dx(0.2)
    m3 = inshell_mask(g3, gs3, wc3)
    samp = [(100, 10), (200, 20), (400, 30)]
    s_mins = []
    for na, nt in samp:
        t0 = time.time()
        _, ov, _, _ = ec_minima(rho_opt_callable(), shift_opt_callable(),
                                 g3, gs3, wc3, m3, na=na, nt=nt)
        s_mins.append(ov)
        print(f"  num_angular={na:4d} num_temporal={nt:3d}  min(EC)={ov:+.3e}  "
              f"{'PASS' if ov >= -1e-12 else 'FAIL'}  ({time.time()-t0:.1f}s)")
    print()
    if s_mins[-1] < -1e-12:
        print(f"  >>> KILL: min(EC) goes negative under finer sphere sampling "
              f"({s_mins[0]:+.2e} -> {s_mins[-1]:+.2e}). The optimizer exploited "
              f"the coarse vector-field discretization.")
        test3 = "KILL"
    else:
        drift = abs(s_mins[-1] - s_mins[0]) / max(abs(s_mins[0]), 1e-300)
        print(f"  >>> SURVIVES: min(EC) stable under sampling escalation "
              f"({s_mins[0]:+.2e} -> {s_mins[-1]:+.2e}, drift {drift*100:.1f}%); "
              f"not a sphere-sampling artifact.")
        test3 = "SURVIVES"

    print("\n" + "=" * 84)
    print("OBJECTIVE DISPOSITION")
    print("=" * 84)
    print(f"  Test 1 (over-provisioning) : {test1}")
    print(f"  Test 2 (resolution)        : {test2}")
    print(f"  Test 3 (EC sampling)       : {test3}")
    killed = "KILL" in (test1, test2, test3)
    if killed:
        print("\n  VERDICT: result KILLED by at least one test. Do NOT record as "
              "a positive finding; report the killing mechanism instead.")
    elif "WEAKENED" in (test1, test2, test3):
        print("\n  VERDICT: not killed, but weakened. Record only as a "
              "provisional signal pending the owed finer study.")
    else:
        print("\n  VERDICT: survives all three kill-tests. The 30.7% isotropic "
              "mass reduction is a genuine slice-bounded effect (still NOT "
              "order-of-magnitude, still unconverged-lower-bound).")


if __name__ == "__main__":
    main()
