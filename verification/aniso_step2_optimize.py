"""Phase 3.3+ Step 2 -- anisotropic radial-profile optimizer.

Free params: cavity-alpha level (1), interior alpha knots (10), interior
mass-function increments (9, monotone 0->M_tot), M_tot (1, the OBJECTIVE),
interior beta-ramp knots (7). alpha(r) and m(r) are INDEPENDENT -> the
sourced fluid is generically ANISOTROPIC (P_r != P_t); that decoupling is
the entire point of Step 2.

Objective: minimize M_tot subject to strict all-four-EC in-shell (via the
Prong-B-certified radial `axisymmetric_ec`, the only trustworthy
sharp-profile oracle) + no horizon + fixed warp performance. Warm start =
the Fuchs isotropic baseline (gate-proven representable; cost ~ 1).
Cartesian eval_metric is NOT used (Prong-B-demoted to smooth-only).

Loop on a coarse (r, theta) mesh for speed (exact symbolic curvature =>
mesh density affects only min-localization, not correctness); the optimum
is re-verified at full resolution, then goes to the Task-28 adversarial
battery. The optimum is NOT a result on its own.

Anisotropy note: |Pt-Pr| is reported in the EULERIAN frame, which mixes
intrinsic matter anisotropy with shift-induced (l=1 dipole) anisotropy --
even the isotropic-fluid baseline shows a large value. It is descriptive
color, NOT a correctness gate; the headline is M_opt/M_ref + strict-EC +
adversarial verification.
"""

from __future__ import annotations

import json
import time
import numpy as np
from scipy.optimize import minimize

from aniso_step2 import (
    R1, R2, V, KA_R, KM_R, KB_R,
    CAV_A, INT_A, EXT_A, CAV_M, INT_M, EXT_M, CAV_B, INT_B, EXT_B,
    profiles_from_knots, eval_ec, warm_start_knots,
)
from warp_factory_py.utils.constants import G, c

NA_INT = int(INT_A.sum())
NM_INT = int(INT_M.sum())
NB_INT = int(INT_B.sum())
PEN_EC, PEN_HZ = 1.0e3, 1.0e2

AK0, MK0, BK0, M_REF, R_FULL = warm_start_knots()
R_LOOP = R_FULL[:: max(1, len(R_FULL) // 500)]      # ~500-pt loop mesh
THETA_LOOP = np.linspace(0.02, np.pi - 0.02, 32)    # coarse loop theta
M_REF_EC = 1.0e39                                   # set from baseline in main


def schwarzschild_alpha(rk, M_tot):
    fac = np.clip(1.0 - 2.0 * G * M_tot / (np.maximum(rk, 1e-9) * c**2),
                  1e-12, None)
    return 0.5 * np.log(fac)


def unpack(x):
    a_cav = x[0]
    a_int = x[1:1 + NA_INT]
    d = np.clip(x[1 + NA_INT:1 + NA_INT + (NM_INT - 1)], 0.0, None)
    M_tot = x[1 + NA_INT + (NM_INT - 1)]
    b_int = np.clip(x[2 + NA_INT + (NM_INT - 1):], 0.0, 1.0)

    alpha_knots = np.empty(len(KA_R))
    alpha_knots[CAV_A] = a_cav
    alpha_knots[INT_A] = a_int
    alpha_knots[EXT_A] = schwarzschild_alpha(KA_R[EXT_A], M_tot)

    s = d.sum()
    m_int_frac = np.concatenate([[0.0], np.cumsum(d) / (s if s > 0 else 1.0)])
    m_knots = np.empty(len(KM_R))
    m_knots[CAV_M] = 0.0
    m_knots[INT_M] = M_tot * m_int_frac
    m_knots[EXT_M] = M_tot

    beta_knots = np.empty(len(KB_R))
    beta_knots[CAV_B] = 1.0
    beta_knots[INT_B] = b_int
    beta_knots[EXT_B] = 0.0
    return alpha_knots, m_knots, beta_knots, M_tot


def warm_x():
    a_cav = float(np.mean(AK0[CAV_A]))
    a_int = AK0[INT_A].copy()
    m_int = MK0[INT_M].copy()
    M_tot = float(MK0[EXT_M].mean()) if EXT_M.any() else float(MK0[-1])
    M_tot = max(M_tot, float(m_int[-1]), 1e25)
    base = np.maximum(np.diff(m_int / M_tot), 0.0)
    if base.sum() <= 0:
        base = np.ones(NM_INT - 1)
    b_int = BK0[INT_B].copy()
    return np.concatenate([[a_cav], a_int, base, [M_tot], b_int]), M_tot


def anisotropy_report(r, T, theta):
    """In-shell radial vs tangential ORTHONORMAL Eulerian pressures at the
    theta-row nearest pi/2. Descriptive only (see module docstring)."""
    jth = int(np.argmin(np.abs(theta - np.pi / 2)))
    ish = (r >= R1) & (r <= R2)
    Pr = T[1, 1, :, jth][ish]
    Pt = T[2, 2, :, jth][ish]
    rho = T[0, 0, :, jth][ish]
    denom = np.maximum(np.abs(Pr) + np.abs(Pt), 1e-300)
    return (float(np.mean(np.abs(Pt - Pr) / denom)), float(np.mean(rho)),
            float(np.mean(Pr)), float(np.mean(Pt)))


def cost_of(x, r, theta, na, nt):
    ak, mk, bk, M_tot = unpack(x)
    Apos, B, F, hmin = profiles_from_knots(r, ak, mk, bk)
    mn, by, T, _ = eval_ec(r, Apos, B, F, na=na, nt=nt, theta=theta)
    pen = (PEN_EC * max(0.0, -mn / abs(M_REF_EC))
           + PEN_HZ * max(0.0, (0.05 - hmin) / 0.05))
    return M_tot / M_REF + pen, M_tot, mn, hmin, by, T


_n = 0
_best = {"cost": np.inf, "x": None}


def main():
    global _n, M_REF_EC
    ndim = 1 + NA_INT + (NM_INT - 1) + 1 + NB_INT
    print("=" * 78)
    print("Phase 3.3+ Step 2 -- anisotropic radial-profile optimizer")
    print(f"  free dims = {ndim}  (1 a_cav + {NA_INT} a_int + {NM_INT-1} "
          f"m incr + 1 M_tot + {NB_INT} b_int)")
    print(f"  loop mesh: {len(R_LOOP)} r x {len(THETA_LOOP)} theta, na=32 nt=4")
    print("=" * 78)

    x0, M0 = warm_x()
    ak, mk, bk, _ = unpack(x0)
    Ap, Bp, Fp, h0 = profiles_from_knots(R_LOOP, ak, mk, bk)
    mn0, by0, T0, th0 = eval_ec(R_LOOP, Ap, Bp, Fp, na=100, nt=10,
                                theta=THETA_LOOP)
    M_REF_EC = abs(mn0) if abs(mn0) > 0 else 1e39
    fr0, rho0, Pr0, Pt0 = anisotropy_report(R_LOOP, T0, th0)
    c0 = M0 / M_REF + PEN_EC * max(0.0, -mn0 / M_REF_EC)
    print(f"\n[warm start = Fuchs baseline]  M_tot={M0:.4e}  "
          f"min(EC)={mn0:+.3e} {'PASS' if mn0>=0 else 'FAIL'}  "
          f"hmin={h0:.4f}  cost={c0:.4f} (~1 expected)")
    print(f"  Eulerian |Pt-Pr|/(|Pr|+|Pt|)={fr0:.2e} (descriptive; baseline "
          f"already anisotropic via the shift dipole)")

    lo = ([-1.5] + [-1.5] * NA_INT + [0.0] * (NM_INT - 1)
          + [0.30 * M_REF] + [0.0] * NB_INT)
    hi = ([0.1] + [0.1] * NA_INT + [1.0] * (NM_INT - 1)
          + [1.20 * M_REF] + [1.0] * NB_INT)
    bounds = list(zip(lo, hi))

    def obj(x):
        global _n
        _n += 1
        cst, M_tot, mn, hmin, _, _ = cost_of(x, R_LOOP, THETA_LOOP, 32, 4)
        if cst < _best["cost"]:
            _best["cost"] = cst
            _best["x"] = x.copy()
        if _n % 25 == 0 or cst < 0.999:
            print(f"  eval {_n:4d}  M/M_ref={M_tot/M_REF:.4f}  "
                  f"min(EC)={mn:+.2e}  hmin={hmin:.3f}  cost={cst:.4f}"
                  f"{'  <-- best' if cst==_best['cost'] else ''}")
        return cst

    print(f"\n[optimizing]  Powell, M_REF={M_REF:.3e}")
    t0 = time.time()
    res = minimize(obj, x0, method="Powell", bounds=bounds,
                   options={"maxiter": 12, "maxfev": 700,
                            "xtol": 1e-4, "ftol": 1e-5})
    print(f"\n[done] {time.time()-t0:.0f}s, {_n} evals; {res.message}")
    print(f"  best loop cost = {_best['cost']:.5f}  (baseline ~ 1.0)")

    ak, mk, bk, M_opt = unpack(_best["x"])
    ApF, BpF, FpF, hF = profiles_from_knots(R_FULL, ak, mk, bk)
    mnF, byF, TF, thF = eval_ec(R_FULL, ApF, BpF, FpF, na=120, nt=12)
    frac, rho_m, Pr_m, Pt_m = anisotropy_report(R_FULL, TF, thF)
    print(f"\n[optimum @ full res: {len(R_FULL)} r x {len(thF)} theta na=120]")
    print(f"  M_opt = {M_opt:.4e}   M_opt/M_ref = {M_opt/M_REF:.4f}  "
          f"({(1-M_opt/M_REF)*100:+.1f}% vs Fuchs baseline)")
    print(f"  min(EC) = {mnF:+.3e}  ({'PASS' if mnF>=0 else 'FAIL'})  "
          f"horizon_min = {hF:.4f}")
    for k, v in byF.items():
        print(f"    {k:8s} {v:+.3e}")
    print(f"  Eulerian anisotropy |Pt-Pr|/(|Pr|+|Pt|)={frac:.2e}  "
          f"rho~{rho_m:+.2e} Pr~{Pr_m:+.2e} Pt~{Pt_m:+.2e}  (descriptive)")

    out = {"alpha_knots": ak.tolist(), "m_knots": mk.tolist(),
           "beta_knots": bk.tolist(), "KA_R": KA_R.tolist(),
           "KM_R": KM_R.tolist(), "KB_R": KB_R.tolist(),
           "M_opt": M_opt, "M_ref": M_REF, "min_EC_radial": mnF,
           "horizon_min": hF, "anisotropy_frac_eulerian": frac,
           "R1": R1, "R2": R2, "v": V}
    with open("F:/science-projects/alcubierre/agent-tools/"
              "_aniso_step2_opt.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n  saved optimum -> agent-tools/_aniso_step2_opt.json")
    print("  NEXT: Task 28 adversarial battery (const-density-floor "
          "control, radial-resolution convergence, smooth Cartesian sign "
          "cross-check) BEFORE any disposition.")


if __name__ == "__main__":
    main()
