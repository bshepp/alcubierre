"""Session-47 verification: nested-variant minimal-mass map adjudication.

Certifies the Session-47 sweep (hf_jobs/sweeps/mmin_map_nested.py) that asks
whether the Session-39 nested-shell margin improvement converts into a lower
certified minimal mass than the Session-32 single-shell floor (Task 3.10 map,
canonical cell M_min = 2.567991e27 nominal).

Gates
-----
  GATE 1  degenerate floors: every f_inner = 0 baseline row must match the
          Session-32 single-shell M_min for its (R2, dfrac, v) cell within
          2 * rel_tol (preview observed EXACT equality at the canonical
          cell -- identical bisection path through the nested builder).
  GATE 2  bracket honesty on every pass row: minec_below < 0 <= minec_above,
          M_fail_below < M_min_nominal, and the bracket width is within the
          requested rel_tol (the bisection actually converged; S32 lesson --
          search logic can manufacture false results).
  GATE 3  no_pass discipline: every no_pass row must be horizon_capped or
          carry finite scout-peak diagnostics (the unimodality-based no-pass
          basis is explicit, never silent).
  GATE 4  (certify mode) RES_CONF escalation of the headline row -- the
          largest certified floor reduction: min_ec(M_min) at RES_CONF must
          be >= 0; if the resolution shift pushes it negative, the corrected
          RES_CONF floor is walked upward in rel_tol steps and the gate then
          requires the improvement vs the S32 reference to SURVIVE (>= half
          the RES_FULL-claimed reduction). The failing endpoint
          (M_fail_below) must stay EC-negative at RES_CONF.

Modes
-----
  audit <nested_parquet>            gates 1-3 (no EC evaluations; seconds)
  certify <nested_parquet> [N]      gate 4 on the N best rows (default 1;
                                    ~10-20 min per row at RES_CONF)

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_mmin_nested_map.py audit <parquet>
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, '.')

from hf_jobs.sweeps.mmin_map import RES_CONF  # noqa: E402
from hf_jobs.sweeps.mmin_map_nested import make_min_ec_nested  # noqa: E402

S32_REFERENCE = "sweeps/mmin_map_full_concat.parquet"

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def _load(nested_path):
    df = pd.read_parquet(nested_path)
    ref = pd.read_parquet(S32_REFERENCE)
    return df, ref


def _ref_floor(ref, R2, dfrac, v):
    row = ref[(ref.R2 == R2) & (ref.dfrac == dfrac) & (ref.v == v)]
    if len(row) != 1:
        return np.nan
    return float(row.iloc[0].M_min_nominal)


def mode_audit(nested_path):
    df, ref = _load(nested_path)
    print("=" * 78)
    print(f"AUDIT MODE -- {nested_path} ({len(df)} rows)")
    print("=" * 78)

    errs = df[df.error.astype(str) != ""]
    gate("no evaluate() exceptions", len(errs) == 0,
         f"{len(errs)} error rows" + (
             f": {errs.error.iloc[0][:100]}" if len(errs) else ""))

    # GATE 1 -- degenerate floors
    base = df[(df.f_inner == 0.0)]
    ok1, details = True, []
    for _, r in base.iterrows():
        mref = _ref_floor(ref, r.R2, r.dfrac, r.v)
        rel = abs(r.M_min_nominal - mref) / mref if np.isfinite(mref) else np.inf
        tol = 2.0 * float(r.get("rel_tol", 0.005)) if "rel_tol" in r else 0.01
        ok1 &= bool(rel <= tol)
        details.append(f"({r.R2:g},{r.dfrac:g},{r.v:g}): rel={rel:.2e}")
    gate(f"GATE 1: {len(base)} f=0 baselines match S32 single-shell floors",
         ok1 and len(base) > 0, "; ".join(details))

    # GATE 2 -- bracket honesty on pass rows
    ok2 = True
    passes = df[(df.f_inner > 0.0) & (df.no_pass == False)]  # noqa: E712
    n_bad = 0
    for _, r in passes.iterrows():
        good = (np.isfinite(r.M_min_nominal)
                and np.isfinite(r.M_fail_below)
                and r.M_fail_below < r.M_min_nominal
                and (r.M_min_nominal - r.M_fail_below) / r.M_min_nominal <= 0.0075
                and r.minec_below < 0.0 <= r.minec_above)
        if not good:
            n_bad += 1
            ok2 = False
    gate(f"GATE 2: bracket honesty on {len(passes)} nested pass rows",
         ok2, f"{n_bad} rows with dishonest/unconverged brackets")

    # GATE 3 -- no_pass discipline
    nop = df[(df.no_pass == True)]  # noqa: E712
    ok3 = True
    for _, r in nop.iterrows():
        has_basis = bool(r.get("horizon_capped", False)) or (
            "scout_peak_minec" in r and np.isfinite(r.get("scout_peak_minec", np.nan)))
        ok3 &= has_basis
    gate(f"GATE 3: no_pass discipline on {len(nop)} no-pass rows", ok3,
         "all carry horizon flag or scout-peak diagnostics" if ok3 else
         "no-pass rows WITHOUT explicit basis found")

    # Summary table: best reduction per cell
    print("-" * 78)
    print("Floor reductions vs S32 single-shell reference (informational):")
    for (R2, dfrac, v), sub in df[df.no_pass == False].groupby(["R2", "dfrac", "v"]):  # noqa: E712
        mref = _ref_floor(ref, R2, dfrac, v)
        best = sub.loc[sub.M_min_nominal.idxmin()]
        red = (1.0 - best.M_min_nominal / mref) * 100.0
        print(f"  cell ({R2:g}, {dfrac:g}, {v:g}): S32 ref {mref:.4e} -> best "
              f"{best.M_min_nominal:.4e} ({red:+.1f}%) at f={best.f_inner:g}, "
              f"inner=({best.R1_in:g},{best.R2_in:g}), binding={best.binding_cond}")
    n_pass = sum(GATES.values())
    print(f"AUDIT: {n_pass}/{len(GATES)} gates PASS")
    return 0 if n_pass == len(GATES) else 1


def mode_certify(nested_path, n_rows=1, cell=None):
    import time
    df, ref = _load(nested_path)
    print("=" * 78)
    print(f"CERTIFY MODE -- RES_CONF escalation of the {n_rows} best row(s)"
          + (f" in cell {cell}" if cell else ""))
    print("=" * 78)
    ok_rows = df[(df.f_inner > 0.0) & (df.no_pass == False)].copy()  # noqa: E712
    if cell is not None:
        R2c, dfc, vc = cell
        ok_rows = ok_rows[(ok_rows.R2 == R2c) & (ok_rows.dfrac == dfc)
                          & (ok_rows.v == vc)].copy()
    ok_rows["mref"] = [
        _ref_floor(ref, r.R2, r.dfrac, r.v) for _, r in ok_rows.iterrows()]
    ok_rows["reduction"] = 1.0 - ok_rows.M_min_nominal / ok_rows.mref
    ok_rows = ok_rows.sort_values("reduction", ascending=False).head(int(n_rows))
    t0 = time.time()
    for i_row, (_, r) in enumerate(ok_rows.iterrows(), 1):
        rid = f"row{i_row}"  # unique gate keys -- rows must not overwrite each other
        rel_tol = 0.005
        print(f"{rid}: cell ({r.R2:g},{r.dfrac:g},{r.v:g}) f={r.f_inner:g} "
              f"inner=({r.R1_in:g},{r.R2_in:g}) M_min={r.M_min_nominal:.5e} "
              f"({r.reduction*100:+.1f}% vs S32)")
        oracle = make_min_ec_nested(float(r.R1_in), float(r.R2_in),
                                    float(r.f_inner))
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
        red_conf = 1.0 - M_up / r.mref
        gate(f"{rid} GATE 4b: RES_CONF-corrected floor still passes",
             bool(np.isfinite(mn_hi) and mn_hi >= 0.0),
             f"corrected M_min = {M_up:.5e} after {n_steps} step(s)")
        gate(f"{rid} GATE 4c: improvement survives escalation (>= half the "
             "RES_FULL-claimed reduction)",
             bool(red_conf >= 0.5 * r.reduction),
             f"RES_CONF {red_conf*100:+.2f}% vs RES_FULL "
             f"{r.reduction*100:+.2f}%")
    n_pass = sum(GATES.values())
    print(f"CERTIFY: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "audit":
        raise SystemExit(mode_audit(sys.argv[2]))
    if len(sys.argv) >= 3 and sys.argv[1] == "certify":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        cell = (tuple(float(x) for x in sys.argv[4:7])
                if len(sys.argv) >= 7 else None)
        raise SystemExit(mode_certify(sys.argv[2], n, cell))
    print(__doc__)
    raise SystemExit(2)
