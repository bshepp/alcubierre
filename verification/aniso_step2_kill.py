"""Phase 3.3+ Step 2 -- adversarial battery for the anisotropic optimum.

The optimizer plateaued at a 3.7% reduction (M_opt=4.463e27 vs baseline
4.634e27) whose full-res min(EC) = -3.72e39 (DEC FAIL) while the coarse
loop mesh reported it passing. Before any disposition:

KILL TEST A -- radial-resolution convergence of the optimum. Evaluate the
  saved optimum at an escalating (r, theta, na) ladder via the certified
  evaluator. If min(EC) stays negative / converges negative, the DEC
  violation is genuine and the coarse-loop "pass" was an under-sampling
  mirage (the optimizer mined the discrete minimization grid, not the
  curvature -- which is exact-certified).

KILL TEST B -- constant-density floor in the same certified radial
  evaluator. Sweep a plain constant-density Fuchs shell down in mass.
  If const-density passes all four ECs at masses <= M_opt while the
  anisotropic optimum FAILS at M_opt, anisotropy is counterproductive
  and the "3.7%" is (worse than) over-provisioning -- Fuchs Sec.6
  unsupported, Step 2 NEGATIVE.
"""

from __future__ import annotations

import json
import time
import numpy as np

from aniso_step2 import (
    R1, R2, V, RHO_0, profiles_from_knots, eval_ec, fuchs_baseline_arrays,
)
from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell, _compact_sigmoid,
)

OPT = json.load(open("F:/science-projects/alcubierre/agent-tools/"
                     "_aniso_step2_opt.json"))
AK = np.array(OPT["alpha_knots"])
MK = np.array(OPT["m_knots"])
BK = np.array(OPT["beta_knots"])
M_OPT = OPT["M_opt"]
M_REF = OPT["M_ref"]


def opt_min_ec(n_r, n_th, na, nt):
    r0, *_ = fuchs_baseline_arrays()           # canonical windowed r grid
    r = r0[:: max(1, len(r0) // n_r)]
    Ap, Bp, Fp, hmin = profiles_from_knots(r, AK, MK, BK)
    th = np.linspace(0.02, np.pi - 0.02, n_th)
    mn, by, _, _ = eval_ec(r, Ap, Bp, Fp, na=na, nt=nt, theta=th)
    return mn, by, hmin, len(r)


def const_density_min_ec(M, n_r=4000, n_th=80, na=100, nt=10):
    rho0 = M / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, 35.0, 35.0, 35.0),
        rho_of_r=lambda r: np.where((r >= R1) & (r <= R2), rho0, 0.0),
        shift_of_r=lambda r: _compact_sigmoid(r, R1, R2, 0.0, 0.0),
        R1=R1, R2=R2, smooth_factor=4000.0, v_warp=V, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=100_000,
    )
    rf = p["r"]
    idx = np.where((rf >= 0.5) & (rf <= 1.5 * R2))[0]
    sub = idx[:: max(1, idx.size // n_r)]
    r = rf[sub]
    th = np.linspace(0.02, np.pi - 0.02, n_th)
    mn, by, _, _ = eval_ec(r, (-p["A"])[sub], p["B"][sub], p["shift"][sub],
                           na=na, nt=nt, theta=th)
    from warp_factory_py.utils.constants import G, c
    M_adm = float(np.interp(1.3 * R2, r,
                  (r * c**2 / (2 * G)) * (1 - 1 / np.maximum(p["B"][sub], 1e-300))))
    return mn, by, M_adm


def main():
    print("=" * 80)
    print("Phase 3.3+ Step 2 -- adversarial battery")
    print(f"  optimum: M_opt={M_OPT:.4e}  M_ref={M_REF:.4e}  "
          f"ratio={M_OPT/M_REF:.4f} ({(1-M_OPT/M_REF)*100:+.1f}%)")
    print("=" * 80)

    print("\n--- KILL TEST A: radial-resolution convergence of the optimum ---")
    print(f"  {'n_r':>6s} {'n_th':>5s} {'na':>4s} {'min(EC)':>13s} "
          f"{'worst cond':>11s} {'pass?':>6s}   dt")
    ladder = [(500, 32, 32, 4), (1500, 60, 60, 6), (4000, 80, 120, 12),
              (8000, 120, 160, 16)]
    last = None
    for n_r, n_th, na, nt in ladder:
        t0 = time.time()
        mn, by, hmin, nr_act = opt_min_ec(n_r, n_th, na, nt)
        worst = min(by, key=by.get)
        last = mn
        print(f"  {nr_act:>6d} {n_th:>5d} {na:>4d} {mn:>+13.3e} "
              f"{worst:>11s} {'PASS' if mn >= 0 else 'FAIL':>6s}   "
              f"{time.time()-t0:.0f}s")
    print()
    if last is not None and last < 0:
        print("  >>> KILL: optimum stays NEGATIVE (DEC) as the mesh refines "
              "-> the\n      coarse-loop 'pass' was a discrete-minimization-"
              "grid under-sampling\n      mirage; the DEC violation is "
              "genuine. (Curvature is exact-certified;\n      the optimizer "
              "mined the objective MESH density, not the physics.)")
        testA = "KILL"
    else:
        print("  >>> SURVIVES A: optimum stays EC-feasible under refinement.")
        testA = "SURVIVES"

    print("\n--- KILL TEST B: constant-density floor (certified radial) ---")
    print(f"  is plain constant-density at <= M_opt EC-feasible while the "
          f"anisotropic\n  optimum FAILS at M_opt? (Step-1 Kill-B analogue, "
          f"now Step-2)")
    cd_floor = None
    for M in (M_OPT, 4.0e27, 3.5e27, 3.0e27, 2.7e27):
        t0 = time.time()
        mn, by, M_adm = const_density_min_ec(M)
        ok = mn >= 0
        if ok:
            cd_floor = M
        worst = min(by, key=by.get)
        print(f"  const-rho nominal M={M:.3e} (ADM~{M_adm:.3e})  "
              f"min(EC)={mn:+.3e} [{worst}]  "
              f"{'PASS' if ok else 'FAIL':>4s}  ({time.time()-t0:.0f}s)")
    print()
    if cd_floor is not None and cd_floor <= M_OPT * 1.001:
        print(f"  >>> KILL: constant-density passes at M={cd_floor:.3e} "
              f"<= M_opt={M_OPT:.3e},\n      while the anisotropic optimum "
              f"FAILS (DEC) at M_opt. Anisotropy is\n      COUNTERPRODUCTIVE; "
              f"the 3.7% is worse than over-provisioning.")
        testB = "KILL"
    else:
        print(f"  >>> SURVIVES B: no constant-density config <= M_opt is "
              f"EC-feasible.")
        testB = "SURVIVES"

    print("\n" + "=" * 80)
    print(f"  Test A (resolution convergence): {testA}")
    print(f"  Test B (const-density floor)   : {testB}")
    if "KILL" in (testA, testB):
        print("\n  VERDICT: Phase 3.3+ Step 2 (anisotropic) NEGATIVE. Free "
              "alpha-m\n  decoupling did not unlock a defensible mass "
              "reduction; the apparent\n  3.7% is a coarse-mesh mirage that "
              "fails DEC at converged resolution\n  and is beaten by trivial "
              "constant-density. Fuchs Sec.6 'orders of\n  magnitude' "
              "unsupported in the anisotropic slice too. Methodological\n  "
              "refinement: an optimizer mines the discrete-minimization mesh "
              "even\n  with an exact-certified curvature engine -- the loop "
              "objective must\n  be evaluated at converged (r,theta,"
              "direction) resolution.")
    else:
        print("\n  VERDICT: survives both -- escalate scrutiny (independent "
              "cross-check)\n  before any positive claim.")


if __name__ == "__main__":
    main()
