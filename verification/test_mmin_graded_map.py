"""Session-48 verification: graded-wall minimal-mass map + S47-interpretation adjudication.

Certifies the Session-48 sweep (hf_jobs/sweeps/mmin_map_graded.py) and makes
the two Session-48 kill-tests reproducible:

1. MASK equivalence (S47 robustness): the S47 nested winner's EC minimum is
   IDENTICAL under the S47 union mask ([7,9.5] u [10,20]) and the contiguous
   mask ([7,20]) -- the standoff sliver hides nothing (worst point sits
   mid-wall at r ~ 12.5 m, equator). Kills the "S47 reduction is a mask
   blind-spot artifact" hypothesis.
2. CROSS-BUILDER discriminator (interpretation): at the IDENTICAL nominal
   density shape (extension [7,10] at 1.5x wall density, canonical cell),
   the per-shell-TOV nested builder's floor is BELOW the S32 single-shell
   floor while the single-TOV graded builder's floor is ABOVE it
   (measured 2026-07-11: 2.26606e27 = 0.8824x vs 2.92989e27 = 1.1409x).
   The S47 optimum therefore works through the TWO-BODY PRESSURE ansatz
   (P = 0 reset at each component's outer surface shaping the lapse), NOT
   through density grading; both configurations are honestly evaluated
   because the EC verdict derives T_munu from the metric via the Einstein
   tensor -- the TOV step only shapes the ansatz.

Gates
-----
  audit mode (seconds, no EC evals):
    GATE 1  d=0 baselines match the S32 single-shell floors (expect EXACT).
    GATE 2  bracket honesty on every pass row.
    GATE 3  no_pass discipline (explicit basis).
  certify mode (RES_CONF, ~7 min/eval on jaga):
    GATE 4  escalation of the N best rows (walk-up correction; if the map is
            negative -- no row below its cell's S32 floor -- certify instead
            confirms the BEST row's floor and that it stays >= the S32 floor
            at RES_CONF).
  adjudicate mode (~15 min local):
    GATE M  mask equivalence at the S47 winner (union == contiguous, both
            positive at the RES_CONF-corrected floor 2.22558e27).
    GATE D  cross-builder floors straddle the S32 floor (nested-g0 below,
            graded same-shape above; graded side read from the S48 parquet).

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_mmin_graded_map.py audit <parquet>
      ... adjudicate <parquet>
      ... certify <parquet> [N]
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, '.')

from hf_jobs.sweeps.mmin_map import RES_CONF, RES_FULL, find_mmin  # noqa: E402
from hf_jobs.sweeps.mmin_map_graded import make_min_ec_graded  # noqa: E402
from hf_jobs.sweeps.mmin_map_nested import (  # noqa: E402
    make_min_ec_nested,
    nested_shell_profiles,
)

S32_REFERENCE = "sweeps/mmin_map_full_concat.parquet"
S47_WINNER = dict(R1=10.0, R2=20.0, v=0.02, R1_in=7.0, R2_in=9.5,
                  f_inner=0.10, M_conf=2.22558e27)

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def _ref_floor(ref, R2, dfrac, v):
    row = ref[(ref.R2 == R2) & (ref.dfrac == dfrac) & (ref.v == v)]
    return float(row.iloc[0].M_min_nominal) if len(row) == 1 else np.nan


def mode_audit(nested_path):
    df = pd.read_parquet(nested_path)
    ref = pd.read_parquet(S32_REFERENCE)
    print("=" * 78)
    print(f"AUDIT MODE -- {nested_path} ({len(df)} rows)")
    print("=" * 78)
    errs = df[df.error.astype(str) != ""]
    gate("no evaluate() exceptions", len(errs) == 0,
         f"{len(errs)} error rows" + (f": {errs.error.iloc[0][:100]}" if len(errs) else ""))

    base = df[df.delta_frac == 0.0]
    ok1, details = True, []
    for _, r in base.iterrows():
        mref = _ref_floor(ref, r.R2, r.dfrac, r.v)
        rel = abs(r.M_min_nominal - mref) / mref if np.isfinite(mref) else np.inf
        ok1 &= bool(rel <= 0.01)
        details.append(f"({r.R2:g},{r.dfrac:g},{r.v:g}): rel={rel:.2e}")
    gate(f"GATE 1: {len(base)} d=0 baselines match S32 floors",
         ok1 and len(base) > 0, "; ".join(details))

    passes = df[(df.delta_frac > 0.0) & (df.no_pass == False)]  # noqa: E712
    n_bad = 0
    for _, r in passes.iterrows():
        good = (np.isfinite(r.M_min_nominal) and np.isfinite(r.M_fail_below)
                and r.M_fail_below < r.M_min_nominal
                and (r.M_min_nominal - r.M_fail_below) / r.M_min_nominal <= 0.0075
                and r.minec_below < 0.0 <= r.minec_above)
        n_bad += 0 if good else 1
    gate(f"GATE 2: bracket honesty on {len(passes)} graded pass rows",
         n_bad == 0, f"{n_bad} bad rows")

    nop = df[df.no_pass == True]  # noqa: E712
    ok3 = all(bool(r.get("horizon_capped", False))
              or np.isfinite(r.get("scout_peak_minec", np.nan))
              for _, r in nop.iterrows())
    gate(f"GATE 3: no_pass discipline on {len(nop)} no-pass rows", ok3)

    print("-" * 78)
    print("Floor vs S32 single-shell reference (informational):")
    for (R2, dfrac, v), sub in df[(df.no_pass == False) & (df.delta_frac > 0)].groupby(  # noqa: E712
            ["R2", "dfrac", "v"]):
        mref = _ref_floor(ref, R2, dfrac, v)
        best = sub.loc[sub.M_min_nominal.idxmin()]
        red = (1.0 - best.M_min_nominal / mref) * 100.0
        n_below = int((sub.M_min_nominal < mref).sum())
        print(f"  cell ({R2:g},{dfrac:g},{v:g}): ref {mref:.4e}; best graded "
              f"{best.M_min_nominal:.4e} ({red:+.1f}%) at d/R1={best.delta_frac:g}, "
              f"q={best.q:g}, {best.taper}; rows below ref: {n_below}/{len(sub)}")
    n_pass = sum(GATES.values())
    print(f"AUDIT: {n_pass}/{len(GATES)} gates PASS")
    return 0 if n_pass == len(GATES) else 1


def mode_adjudicate(graded_path):
    import time
    t0 = time.time()
    print("=" * 78)
    print("ADJUDICATE MODE -- S47 mask kill-test + cross-builder discriminator")
    print("=" * 78)
    from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

    w = S47_WINNER
    r, Apos, B, F, M_adm, hmin = nested_shell_profiles(
        w["R1"], w["R2"], w["R1_in"], w["R2_in"], w["f_inner"],
        w["M_conf"], w["v"])
    n_r, n_th, na, nt = RES_FULL
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    rs = r[sub]
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    mins = {}
    for name, mask in [
            ("union", ((rs >= w["R1_in"]) & (rs <= w["R2_in"]))
             | ((rs >= w["R1"]) & (rs <= w["R2"]))),
            ("contiguous", (rs >= w["R1_in"]) & (rs <= w["R2"]))]:
        out = evaluate_axisym_ec(rs, Apos[sub], B[sub], F[sub], v=w["v"],
                                 theta=theta, in_shell_mask_1d=mask,
                                 num_angular=na, num_temporal=nt)
        mins[name] = float(out["min"])
        print(f"    {name}: min = {mins[name]:+.4e}  [{time.time()-t0:.0f}s]")
    rel = abs(mins["union"] - mins["contiguous"]) / max(abs(mins["union"]), 1e-300)
    gate("GATE M: S47 winner min(EC) identical under union vs contiguous "
         "mask, both positive at the corrected floor",
         bool(rel < 1e-9 and mins["union"] > 0.0), f"rel diff = {rel:.2e}")

    df = pd.read_parquet(graded_path)
    ref = pd.read_parquet(S32_REFERENCE)
    mref = _ref_floor(ref, 20.0, 0.5, 0.02)
    grow = df[(df.R2 == 20.0) & (df.v == 0.02) & (df.delta_frac == 0.3)
              & (df.q == 1.5) & (df.taper == "flat")]
    m_graded = float(grow.iloc[0].M_min_nominal) if len(grow) else np.nan
    oracle = make_min_ec_nested(7.0, 10.0, 0.1234)
    rec = find_mmin(10.0, 20.0, 0.02, rel_tol=0.005, min_ec_fn=oracle)
    m_nested0 = rec["M_min_nominal"]
    print(f"    same nominal shape: nested-g0 floor = {m_nested0:.5e} "
          f"({m_nested0/mref:.4f}x ref), graded floor = {m_graded:.5e} "
          f"({m_graded/mref:.4f}x ref)  [{time.time()-t0:.0f}s]")
    gate("GATE D: cross-builder floors straddle the S32 floor at identical "
         "nominal rho (pressure ansatz is the lever)",
         bool(np.isfinite(m_graded) and m_nested0 < mref < m_graded),
         f"nested-g0 {m_nested0/mref:.4f}x < 1 < graded {m_graded/mref:.4f}x")
    n_pass = sum(GATES.values())
    print(f"ADJUDICATE: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


def mode_certify(graded_path, n_rows=1):
    import time
    df = pd.read_parquet(graded_path)
    ref = pd.read_parquet(S32_REFERENCE)
    print("=" * 78)
    print(f"CERTIFY MODE -- RES_CONF escalation of the {n_rows} best row(s)")
    print("=" * 78)
    ok_rows = df[(df.delta_frac > 0.0) & (df.no_pass == False)].copy()  # noqa: E712
    ok_rows["mref"] = [_ref_floor(ref, r.R2, r.dfrac, r.v)
                       for _, r in ok_rows.iterrows()]
    ok_rows["reduction"] = 1.0 - ok_rows.M_min_nominal / ok_rows.mref
    ok_rows = ok_rows.sort_values("reduction", ascending=False).head(int(n_rows))
    t0 = time.time()
    for i_row, (_, r) in enumerate(ok_rows.iterrows(), 1):
        rid = f"row{i_row}"
        rel_tol = 0.005
        negative_map = bool(r.reduction <= 0.0)
        print(f"{rid}: cell ({r.R2:g},{r.dfrac:g},{r.v:g}) d/R1={r.delta_frac:g} "
              f"q={r.q:g} {r.taper} M_min={r.M_min_nominal:.5e} "
              f"({r.reduction*100:+.1f}% vs S32)"
              + ("  [NEGATIVE MAP -- confirming best row]" if negative_map else ""))
        oracle = make_min_ec_graded(float(r.delta_frac) * float(r.R1),
                                    float(r.q), str(r.taper))
        mn_lo, _, _, _ = oracle(float(r.R1), float(r.R2),
                                float(r.M_fail_below), float(r.v), RES_CONF)
        print(f"    RES_CONF @ M_fail_below: min_ec = {mn_lo:+.4e} "
              f"[{time.time()-t0:.0f}s]")
        gate(f"{rid} GATE 4a: failing endpoint stays EC-negative at RES_CONF",
             bool(np.isfinite(mn_lo) and mn_lo < 0.0), f"{mn_lo:+.3e}")
        M_up = float(r.M_min_nominal)
        mn_hi, _, _, _ = oracle(float(r.R1), float(r.R2), M_up, float(r.v),
                                RES_CONF)
        print(f"    RES_CONF @ M_min       : min_ec = {mn_hi:+.4e} "
              f"[{time.time()-t0:.0f}s]")
        n_steps = 0
        while not (np.isfinite(mn_hi) and mn_hi >= 0.0) and n_steps < 6:
            n_steps += 1
            M_up *= (1.0 + rel_tol)
            mn_hi, _, _, _ = oracle(float(r.R1), float(r.R2), M_up,
                                    float(r.v), RES_CONF)
            print(f"    RES_CONF walk-up {n_steps}: M = {M_up:.5e}, "
                  f"min_ec = {mn_hi:+.4e} [{time.time()-t0:.0f}s]")
        gate(f"{rid} GATE 4b: RES_CONF-corrected floor passes",
             bool(np.isfinite(mn_hi) and mn_hi >= 0.0),
             f"corrected M_min = {M_up:.5e} after {n_steps} step(s)")
        red_conf = 1.0 - M_up / r.mref
        if negative_map:
            gate(f"{rid} GATE 4c: negative map CONFIRMED at RES_CONF "
                 "(best graded floor stays at/above the S32 floor)",
                 bool(red_conf <= 0.005),
                 f"RES_CONF {red_conf*100:+.2f}%")
        else:
            gate(f"{rid} GATE 4c: improvement survives escalation",
                 bool(red_conf >= 0.5 * r.reduction),
                 f"RES_CONF {red_conf*100:+.2f}% vs RES_FULL "
                 f"{r.reduction*100:+.2f}%")
    n_pass = sum(GATES.values())
    print(f"CERTIFY: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "audit":
        raise SystemExit(mode_audit(sys.argv[2]))
    if len(sys.argv) >= 3 and sys.argv[1] == "adjudicate":
        raise SystemExit(mode_adjudicate(sys.argv[2]))
    if len(sys.argv) >= 3 and sys.argv[1] == "certify":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        raise SystemExit(mode_certify(sys.argv[2], n))
    print(__doc__)
    raise SystemExit(2)
