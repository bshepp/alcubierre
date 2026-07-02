"""Task 3.10 gate + convergence battery for the minimal-mass map.

Run with the repo root on PYTHONPATH:

    $env:PYTHONPATH="."; C:\\Python313\\python.exe verification/test_mmin_map_gate.py

Three stages, in the project's adversarial-verification idiom:

GATE 1 -- canonical regression anchor. The Session-31 Kill-Test-B row must
  reproduce through the new module's code path: constant-density at nominal
  M = 2.7e27 on (R1, R2, v) = (10, 20, 0.02c) passes all four ECs at
  RES_FULL with ADM mass 2.786e27 (+/- 0.5%). Guards against any silent
  divergence between this harness and the certified S31 setup.

GATE 2 -- canonical threshold location. Bisect M_min at the canonical cell.
  Consistency requirement: M_min_nominal <= 2.7e27 (Sessions 29-31 showed
  2.7e27 passes; the floor must not sit above a mass already shown to pass).

GATE 3 -- threshold resolution-convergence (the S31 lesson applied to the
  bisection): evaluate M_min * (1 -/+ 2*rel_tol) at RES_FULL and at the
  escalated RES_CONF tier. The pass/fail classification on both sides must
  be identical across tiers, i.e. the located threshold is not a mesh
  artifact. Any flip -> the map's accept/reject tier is NOT converged and
  the sweep must not be trusted (exit code 1).
"""

from __future__ import annotations

import sys
import time

import numpy as np

from hf_jobs.sweeps.mmin_map import (
    RES_CONF, RES_FULL, find_mmin, min_ec,
)

R1C, R2C, VC = 10.0, 20.0, 0.02
S31_NOMINAL = 2.7e27
S31_ADM = 2.786e27


def main() -> int:
    failures = 0

    print("=" * 78)
    print("Task 3.10 gate battery -- certified minimal-mass map")
    print("=" * 78)

    # --- GATE 1: canonical regression anchor -------------------------------
    t0 = time.time()
    mn, by, M_adm, hmin = min_ec(R1C, R2C, S31_NOMINAL, VC, RES_FULL)
    ok_pass = np.isfinite(mn) and mn >= 0.0
    ok_adm = abs(M_adm - S31_ADM) / S31_ADM < 0.005
    print(f"\nGATE 1 (S31 anchor): nominal M={S31_NOMINAL:.3e}")
    print(f"  min(EC) = {mn:+.3e}  ({'PASS' if ok_pass else 'FAIL'})  "
          f"worst={min(by, key=by.get) if by else '?'}")
    print(f"  ADM     = {M_adm:.4e} vs S31 {S31_ADM:.4e} "
          f"({'OK' if ok_adm else 'MISMATCH'})   [{time.time()-t0:.0f}s]")
    if not (ok_pass and ok_adm):
        failures += 1
        print("  >>> GATE 1 FAILED")

    # --- GATE 2: canonical threshold ---------------------------------------
    t0 = time.time()
    rec = find_mmin(R1C, R2C, VC, rel_tol=0.005)
    print(f"\nGATE 2 (canonical threshold): [{time.time()-t0:.0f}s, "
          f"{rec['n_eval_scout']} scout + {rec['n_eval_full']} full evals]")
    if rec.get("no_pass"):
        print("  >>> GATE 2 FAILED: no passing mass found at canonical cell")
        failures += 1
        print(f"\nRESULT: {failures} gate failure(s)")
        return 1
    mmin_nom = rec["M_min_nominal"]
    print(f"  M_min nominal = {mmin_nom:.4e}  (ADM {rec['M_min_adm']:.4e})")
    print(f"  vs canonical Fuchs 4.49e27: {mmin_nom/4.49e27:.3f}x  "
          f"(uniform over-provisioning factor {4.49e27/mmin_nom:.2f})")
    print(f"  kappa_nominal = {rec['kappa_nominal']:.3f}  "
          f"kappa_adm = {rec['kappa_adm']:.3f}  "
          f"(2A.9b Cartesian-era bracket (4.17, 5.83])")
    print(f"  binding condition at threshold: {rec['binding_cond']}")
    print(f"  minec just above/below: {rec['minec_above']:+.2e} / "
          f"{rec['minec_below']:+.2e}")
    ok_floor = mmin_nom <= S31_NOMINAL * 1.001
    if not ok_floor:
        failures += 1
        print(f"  >>> GATE 2 FAILED: M_min {mmin_nom:.3e} sits ABOVE the "
              f"mass 2.7e27 already shown to pass (S29-31)")

    # --- GATE 3: threshold convergence across tiers ------------------------
    print("\nGATE 3 (threshold resolution-convergence):")
    eps = 2 * 0.005
    flips = 0
    for side, M in (("below", mmin_nom * (1 - eps)),
                    ("above", mmin_nom * (1 + eps))):
        t0 = time.time()
        mn_f, _, _, _ = min_ec(R1C, R2C, M, VC, RES_FULL)
        mn_c, _, _, _ = min_ec(R1C, R2C, M, VC, RES_CONF)
        cls_f = "PASS" if mn_f >= 0 else "FAIL"
        cls_c = "PASS" if mn_c >= 0 else "FAIL"
        agree = cls_f == cls_c
        flips += (not agree)
        print(f"  M_min*{'(1-eps)' if side == 'below' else '(1+eps)'} "
              f"= {M:.4e}: RES_FULL {mn_f:+.3e} [{cls_f}]  "
              f"RES_CONF {mn_c:+.3e} [{cls_c}]  "
              f"{'consistent' if agree else '*** FLIP ***'}  "
              f"[{time.time()-t0:.0f}s]")
    if flips:
        failures += 1
        print("  >>> GATE 3 FAILED: threshold classification flips under mesh "
              "escalation -- accept/reject tier NOT converged; do not trust "
              "the map")

    print("\n" + "=" * 78)
    print(f"RESULT: {'ALL GATES PASS' if failures == 0 else str(failures) + ' gate failure(s)'}")
    print("=" * 78)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
