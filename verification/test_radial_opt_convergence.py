"""Radial-resolution convergence of the radial-frame optimum.

The optimum passes the radial evaluator (the one it was optimized against,
on a COARSE 500-point subsampled mesh) but fails the Cartesian pipeline.
Two hypotheses:

  H1  the radial evaluator is genuinely wrong on this config (would be
      alarming -- it was validated exactly on smooth limits).
  H2  the radial evaluator is correct, but the optimizer drove rho into a
      near-step shape (knots ~[3.7e13, 3.2e22, 1.1e23, ...]) OUTSIDE the
      smooth regime the validation covered; on a coarse objective mesh +
      quintic-spline 2nd-derivative of a near-cliff the evaluator
      UNDER-RESOLVES the curvature spike. Properly resolved, the radial
      evaluator should ALSO go negative -- agreeing with Cartesian, i.e.
      the converged truth is FAIL and the 21.9% was mined numerical slack.

Test: re-evaluate the SAME optimum profile in the radial evaluator at
increasing radial mesh density (no subsampling artefacts), theta fixed
fine. If min(EC) collapses toward / through zero as N_r grows, H2 is
confirmed and the result is a clean NEGATIVE consistent across both
representations once each is converged.
"""

from __future__ import annotations

import json
import time
import numpy as np
from scipy.interpolate import CubicSpline

from warp_factory_py.metrics.warp_shell import metric_profile_warp_shell
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

OPT = json.load(open("F:/science-projects/alcubierre/agent-tools/_radial_opt_knots.json"))
R1, R2, V, SF = OPT["R1"], OPT["R2"], OPT["v"], OPT["SF"]
RKR = np.array(OPT["rho_knot_r"]); BKR = np.array(OPT["beta_knot_r"])
RHO_K = np.array(OPT["rho_knots"]); BETA_K = np.array(OPT["beta_knots"])


def rho_opt():
    cs = CubicSpline(RKR, RHO_K, bc_type="natural")
    return lambda r: np.where((r >= R1) & (r <= R2), np.maximum(cs(r), 0.0), 0.0)


def shift_opt():
    cs = CubicSpline(BKR, BETA_K, bc_type="natural")
    return lambda r: np.where(r <= R1, 1.0,
                              np.where(r >= R2, 0.0, np.clip(cs(r), 0.0, 1.0)))


def main():
    print("=" * 78)
    print("RADIAL-RESOLUTION CONVERGENCE of the radial-frame optimum")
    print(f"  optimizer reported (coarse 500-pt mesh): min(EC) = "
          f"{OPT['min_EC_radial']:+.3e}  (PASS)")
    print("=" * 78)
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, 35.0, 35.0, 35.0), rho_of_r=rho_opt(),
        shift_of_r=shift_opt(), R1=R1, R2=R2, smooth_factor=SF, v_warp=V,
        do_warp=True, grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=100_000)
    rf = p["r"]; Af = -p["A"]; Bf = p["B"]; Ff = p["shift"]
    win = (rf >= 0.5) & (rf <= 1.5 * R2)
    idx = np.where(win)[0]
    theta = np.linspace(0.01, np.pi - 0.01, 160)
    print(f"\n  {'N_r':>7s}  {'min(EC)':>13s}  {'pass?':>6s}   dt")
    prev = None
    for target in (500, 1500, 5000, 15000, idx.size):
        sub = idx[:: max(1, idx.size // target)]
        r = rf[sub]
        t0 = time.time()
        res = evaluate_axisym_ec(
            r, Af[sub], Bf[sub], Ff[sub], v=V, theta=theta,
            in_shell_mask_1d=(r >= R1) & (r <= R2),
            num_angular=120, num_temporal=12)
        mn = res["min"]
        print(f"  {r.size:>7d}  {mn:>+13.3e}  {'PASS' if mn >= 0 else 'FAIL':>6s}"
              f"   {time.time()-t0:.0f}s")
        prev = mn
    print()
    print("=" * 78)
    if prev is not None and prev < 0:
        print("VERDICT: H2 CONFIRMED. The radial evaluator itself goes "
              "NEGATIVE once the\n  radial mesh resolves the optimizer's "
              "near-step rho. The 21.9% was mined\n  numerical slack (coarse "
              "objective mesh / spline-derivative of a near-\n  cliff), NOT "
              "physics. Converged truth = FAIL, consistent across BOTH\n  "
              "representations. Clean NEGATIVE -- same lesson as Session 28, "
              "deeper:\n  ANY numerical objective gets mined wherever the "
              "optimizer can find slack.")
    else:
        print("VERDICT: H1 / inconclusive. Radial evaluator stays POSITIVE "
              "under radial\n  refinement while Cartesian says FAIL -> a "
              "genuine cross-representation\n  conflict that must be resolved "
              "before any disposition.")


if __name__ == "__main__":
    main()
