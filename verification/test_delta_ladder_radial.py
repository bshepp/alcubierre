"""Session-41 kill-test (Session-35 audit queue item (f)): the Session-18/19
thickness (Delta) ladder re-run through the certified radial evaluator.

The Session-18 kappa bracket (4.17, 5.83] at the anchor cell and the
Session-19 27-cell kappa surface (mean 5.3, median 6, std 1.0; nulls at
beta=0.05 / C=1/6; kappa rising with beta and R2, the R2 trend flagged
"may be partially a wall-resolution effect") were measured on MATLAB
WarpFactory's Cartesian pipeline -- the convention later demoted for sharp
profiles (Session 30) and implicated in the Session-39 nested-shell
reversal.  This harness re-runs the Delta-direction ladder through
`hf_jobs.sweeps.mmin_map.min_ec` (the certified radial path used by Task
3.10, which measured the same kappa from the MASS direction: 4.64 +/- 0.57
over 14 thresholds).

Protocol per cell (C, R2, beta), M = C R2 c^2 / 2G (nominal, matching the
recorded sweep's mass column):
  1. scout ladder over Delta rungs (RES_SCOUT -- bracket proposal only,
     never accepts; the recorded rungs {1, 1.5, 2, 3, 5, 7, 10} extended
     to the geometric cap Delta <= R2 - 0.6),
  2. RES_FULL verification of the proposed bracket endpoints (expand one
     rung on disagreement),
  3. RES_FULL bisection to rel(Delta) <= 3%,
  4. kappa bracket = (Delta/R2)(C/beta) at the certified crossing; binding
     condition recorded; the DEC-only crossing is derived from the same
     evaluation set (the recorded MATLAB gate was DEC; the certified gate
     is min over all four ECs -- NEC binds in practice, cf. 3.10).
Null cells are declared only after RES_FULL verification AT THE SCOUT-LADDER
MAXIMUM (not the cap -- the first run of this harness verified the cap and
thereby manufactured two false nulls, caught by the fine re-scan; the S32
false-negative lesson applies recursively to kill-tests themselves). Cells
that pass at the 0.5 m floor are reported NO-BOUND (kappa upper limit), not
as a bracket.

CERTIFIED RESULTS (2026-07-06 runs; RES_FULL, rel <= 3% where bracketed):
  12 genuine crossings: kappa = 4.93 +/- 0.44, range [4.36, 5.87], rising
    with R2 (matching the 3.10 mass-direction trend; 3.10: 4.64 +/- 0.57).
    Anchor cell (C=1/3, R2=20, beta=0.02): kappa in (4.479, 4.583] --
    inside the Session-18 MATLAB bracket (4.17, 5.83], ~20% below the
    Session-19 sweep-resolution values. Binding: NEC (19 cells), SEC (3).
  3 nulls confirmed (beta=0.05, C=1/6; RES_FULL at the scout peak:
    -6.4e39 / -6.8e39 / -4.7e39) -- matches Session 19.
  Cells (1/3, 15, 0.05) and (1/3, 20, 0.05): genuine WINDOWS -- pass for
    Delta in (10.0, ~13) and (14.5, ~19) resp.; kappa_lower crossings
    (4.44, 4.67] and (4.67, 4.83].
  12 NO-BOUND cells (all nine beta=0.005 rows + beta=0.02 at (1/3, 15),
    (1/2, 15), (1/2, 20)): EC-pass persists down to the 0.5 m floor with
    healthy margins (e.g. +1.8e39) where the recorded MATLAB sweep reported
    failures. Caveat: at smooth_factor 4000 the profile smoothing width
    (~5 m) exceeds these Delta values, so nominal "thin walls" are smoothed
    into wide low-amplitude bumps -- Delta is not the physical wall
    thickness below ~5 m in this convention.

Usage (one invocation evaluates the given cell indices, ~2 min/cell):
  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_delta_ladder_radial.py 0 1 2
Cell index = itertools.product order over C in (1/6, 1/3, 1/2) x
R2 in (15, 20, 30) x beta in (0.005, 0.02, 0.05), matching
warp_factory_repro/kappa_surface_sweep.csv row order.
"""
from __future__ import annotations

import sys
import time
from itertools import product

import numpy as np

sys.path.insert(0, '.')

from hf_jobs.sweeps.mmin_map import (  # noqa: E402
    min_ec, RES_SCOUT, RES_FULL,
)
from warp_factory_py.utils.constants import G, c  # noqa: E402

CS = (1.0 / 6.0, 1.0 / 3.0, 0.5)
R2S = (15.0, 20.0, 30.0)
BETAS = (0.005, 0.02, 0.05)
CELLS = list(product(CS, R2S, BETAS))
RUNGS = [1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 14.0]
REL_TOL = 0.03


def evaluate(C, R2, beta, Delta, res):
    """min over the four ECs + the DEC-only minimum at one Delta."""
    M = C * R2 * c**2 / (2.0 * G)
    R1 = R2 - Delta
    mn, by, M_adm, hmin = min_ec(R1, R2, M, beta, res=res)
    dec = by.get("dominant", float("nan")) if by else float("nan")
    return mn, dec, by


def run_cell(idx):
    C, R2, beta = CELLS[idx]
    cap = R2 - 0.6
    rungs = [d for d in RUNGS if d <= cap] + [cap]
    t0 = time.time()
    print(f"--- cell {idx}: C = {C:.4f}, R2 = {R2}, beta = {beta} "
          f"(M = {C * R2 * c**2 / (2.0 * G):.4e} kg) ---")

    # 1. scout ladder
    scout = {}
    for d in rungs:
        mn, dec, _ = evaluate(C, R2, beta, d, RES_SCOUT)
        scout[d] = mn
        print(f"    scout Delta = {d:6.2f}: min(EC) = {mn:+.3e}", flush=True)
    passing = [d for d in rungs if np.isfinite(scout[d]) and scout[d] >= 0]
    if not passing:
        # Verify the null at RES_FULL at the SCOUT-LADDER MAXIMUM and its
        # inter-rung neighbourhood -- a coarse ladder can straddle a narrow
        # passing window (this manufactured two false nulls in the first
        # run of this harness).
        d_peak = max(scout, key=lambda d: scout[d]
                     if np.isfinite(scout[d]) else -np.inf)
        i_pk = rungs.index(d_peak)
        probes = sorted({d_peak,
                         0.5 * (d_peak + rungs[max(i_pk - 1, 0)]),
                         0.5 * (d_peak + rungs[min(i_pk + 1, len(rungs) - 1)])})
        best = -np.inf
        best_d = d_peak
        for d in probes:
            mn_p, _, _ = evaluate(C, R2, beta, d, RES_FULL)
            print(f"    null-check Delta = {d:6.2f}: min(EC) = {mn_p:+.3e}",
                  flush=True)
            if np.isfinite(mn_p) and mn_p > best:
                best, best_d = mn_p, d
        if best < 0:
            print(f"    NULL cell: no EC pass at/around the scout peak "
                  f"(best RES_FULL min = {best:+.3e} at Delta = {best_d:.2f}) "
                  f"[{time.time()-t0:.0f}s]")
            print(f"RESULT {idx} C={C:.4f} R2={R2} beta={beta} NULL "
                  f"kappa_lo=nan kappa_hi=nan")
            return
        # a hidden window exists: bracket its lower crossing
        below = [d for d in rungs if d < best_d]
        lo = max(below) if below else 0.5 * best_d
        hi = best_d
    else:
        hi = min(passing)
        below = [d for d in rungs if d < hi]
        lo = max(below) if below else None

    # 2. verify endpoints at RES_FULL
    if lo is not None:
        mn_lo, _, _ = evaluate(C, R2, beta, lo, RES_FULL)
        if np.isfinite(mn_lo) and mn_lo >= 0:
            # scout-fail passes at full: walk down
            while lo is not None and np.isfinite(mn_lo) and mn_lo >= 0:
                hi = lo
                below = [d for d in rungs if d < lo]
                lo = max(below) if below else None
                if lo is not None:
                    mn_lo, _, _ = evaluate(C, R2, beta, lo, RES_FULL)
    mn_hi, dec_hi, by_hi = evaluate(C, R2, beta, hi, RES_FULL)
    while not (np.isfinite(mn_hi) and mn_hi >= 0):
        # scout-pass fails at full: walk up
        above = [d for d in rungs if d > hi]
        if not above:
            print(f"    NULL cell after RES_FULL verification "
                  f"[{time.time()-t0:.0f}s]")
            print(f"RESULT {idx} C={C:.4f} R2={R2} beta={beta} NULL "
                  f"kappa_lo=nan kappa_hi=nan")
            return
        lo, hi = hi, min(above)
        mn_hi, dec_hi, by_hi = evaluate(C, R2, beta, hi, RES_FULL)
    if lo is None:
        # pass at the smallest rung: probe the 0.5 m floor; if it still
        # passes there, the cell has NO thickness bound in range -- report
        # an upper limit, not a bracket
        floor = 0.5
        mn_fl, _, _ = evaluate(C, R2, beta, floor, RES_FULL)
        if np.isfinite(mn_fl) and mn_fl >= 0:
            kap_ub = (floor / R2) * (C / beta)
            print(f"    NO-BOUND: EC pass persists to the {floor} m floor "
                  f"(min = {mn_fl:+.3e}); kappa < {kap_ub:.3f} (upper limit) "
                  f"[{time.time()-t0:.0f}s]")
            print(f"RESULT {idx} C={C:.4f} R2={R2} beta={beta} NOBOUND "
                  f"kappa_lo=nan kappa_hi={kap_ub:.4f}")
            return
        lo = floor

    # 3. bisection at RES_FULL
    dec_records = {hi: dec_hi}
    while (hi - lo) / hi > REL_TOL:
        mid = 0.5 * (lo + hi)
        mn_mid, dec_mid, by_mid = evaluate(C, R2, beta, mid, RES_FULL)
        dec_records[mid] = dec_mid
        print(f"    full Delta = {mid:7.3f}: min(EC) = {mn_mid:+.3e}",
              flush=True)
        if np.isfinite(mn_mid) and mn_mid >= 0:
            hi, mn_hi, by_hi = mid, mn_mid, by_mid
        else:
            lo = mid

    kap_lo = (lo / R2) * (C / beta)
    kap_hi = (hi / R2) * (C / beta)
    binding = min(by_hi, key=by_hi.get) if by_hi else ""
    # DEC-only crossing from the same evaluation set (coarser; the recorded
    # MATLAB gate was DEC)
    dec_pass = [d for d, v in dec_records.items()
                if np.isfinite(v) and v >= 0]
    dec_hi_val = min(dec_pass) if dec_pass else float("nan")
    print(f"    Delta_min in ({lo:.3f}, {hi:.3f}]  =>  kappa in "
          f"({kap_lo:.3f}, {kap_hi:.3f}]  binding = {binding}  "
          f"(DEC-only first-pass Delta <= {dec_hi_val:.3f})  "
          f"[{time.time()-t0:.0f}s]")
    print(f"RESULT {idx} C={C:.4f} R2={R2} beta={beta} OK "
          f"kappa_lo={kap_lo:.4f} kappa_hi={kap_hi:.4f} binding={binding}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        run_cell(int(arg))
