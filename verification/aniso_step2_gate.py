"""Phase 3.3+ Step 2 -- Fuchs-baseline correctness gate.

Must pass BEFORE optimizing: the Fuchs constant-density isotropic baseline
must be representable in the free (alpha, m, beta) family (single global C2
splines through the full-window knot grid) and reproduce the Step-1
isotropic in-shell min(EC). If it does, the free-alpha generalization is
sound, the boundary handling is correct (no kinks), and the optimizer's
search space provably CONTAINS the baseline (warm-start cost = 1 valid).

Shared parameterization lives in aniso_step2.py (used identically by the
optimizer).
"""

from __future__ import annotations

import numpy as np

from aniso_step2 import (
    R1, R2, fuchs_baseline_arrays, profiles_from_knots, eval_ec,
    KA_R, KM_R, KB_R,
)


def main():
    print("=" * 74)
    print("Phase 3.3+ Step 2 -- Fuchs-baseline correctness gate")
    print("=" * 74)
    r, Apos0, B0, F0, alpha0, m0, M_tot0 = fuchs_baseline_arrays()

    direct, direct_by, _, _ = eval_ec(r, Apos0, B0, F0)
    print(f"\n[direct baseline]  M_tot~{M_tot0:.4e}")
    print(f"  isotropic in-shell min(EC) = {direct:+.4e}  "
          f"({'PASS' if direct >= 0 else 'FAIL'})")
    for k, v in direct_by.items():
        print(f"    {k:8s} {v:+.4e}")

    alpha_knots = np.interp(KA_R, r, alpha0)
    m_knots = np.interp(KM_R, r, m0)
    beta_knots = np.interp(KB_R, r, F0)
    Apos_r, B_r, F_r, hmin = profiles_from_knots(
        r, alpha_knots, m_knots, beta_knots)
    recon, recon_by, _, _ = eval_ec(r, Apos_r, B_r, F_r)
    print(f"\n[knot reconstruction]  K_alpha={len(KA_R)} K_m={len(KM_R)} "
          f"K_beta={len(KB_R)} (full-window, single C2 spline each)  "
          f"horizon_min={hmin:.4f}")
    print(f"  in-shell min(EC) = {recon:+.4e}  "
          f"({'PASS' if recon >= 0 else 'FAIL'})")
    for k, v in recon_by.items():
        print(f"    {k:8s} {v:+.4e}")

    sign_ok = (direct >= 0) == (recon >= 0)
    rel = abs(recon - direct) / max(abs(direct), 1e-300)
    print(f"\n  sign match: {'YES' if sign_ok else 'NO'}   "
          f"relative min(EC) diff: {rel*100:.1f}%")
    print("=" * 74)
    if sign_ok and rel < 0.15:
        print("GATE PASS: Fuchs isotropic baseline representable + reproduces "
              "the Step-1\n  isotropic verdict. Parameterization sound; "
              "optimizer search space\n  contains the baseline. -> build "
              "optimizer.")
    else:
        print("GATE FAIL: parameterization does not round-trip the baseline "
              "within\n  tolerance -- investigate BEFORE optimizing.")


if __name__ == "__main__":
    main()
