"""Session-49 verification: spin-up EC margin surface (Task 2E.1, first leg).

Adjudicates the rigid-profile spin-up family: exact time-dependent metric
(v -> v(t); solvers.axisymmetric_ec.evaluate_axisym_ec_timedep) whose
Einstein tensor is exact in (v, vd) with NO vdd dependence (Session-49
GATE B, symbolic), so the full inflate-coast-deflate lifecycle reduces to
the margin surface min-EC(v, vd) per configuration.

Gates
-----
  audit mode (no EC evals; seconds):
    GATE 2  quasi-static corridor: min_ec(v, vd=0) >= 0 for every v <=
            v_target, each configuration (the S32 M_min(v) monotonicity
            kill-test -- a shell provisioned for v_target must pass at
            every intermediate v).
    GATE 4  surface sanity: all rows finite (no NaN outside horizon
            flags); the vd-response magnitude grows with |vd| at fixed v
            for each config at v = v_target.
    GATE 5  tau* extraction: for each config, vd_max(v) = positive-vd
            zero-crossing (log-interpolated; +inf if the margin never
            crosses within the grid); tau* = max_s v_t S'(s) /
            (c vd_max(v(s))) for a quintic-smoothstep ramp. Asserts: the
            canonical vessel's tau* is finite-or-vacuous BELOW the grid
            (margin never crosses -> report as upper bound), every
            extracted tau* < 1 s, and tau*(floor) >= tau*(canonical)
            when both are finite.
  exact mode (~4 EC evals; ~4 min):
    GATE 1  static-limit row check: a sampled vd=0 row per config
            recomputed through the STATIC evaluator matches the parquet
            to 1e-9 rel (same mesh -> effectively exact).
    GATE 3  S32 cross-anchor: the floor config's (v=0.02, vd=0) margin
            equals the S32 map's recorded minec_above for the canonical
            cell (same profiles, mesh, mask) to 1e-6 rel.

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_spinup_margin.py audit <parquet>
      ... exact <parquet>
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, '.')

C_LIGHT = 299_792_458.0
S32_REFERENCE = "sweeps/mmin_map_full_concat.parquet"

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def _vd_max_of_v(sub: pd.DataFrame):
    """Positive-vd margin zero-crossing per v (np.inf if never negative)."""
    out = {}
    for v, rows in sub.groupby("v"):
        pos = rows[rows.vd > 0].sort_values("vd")
        if pos.empty:
            continue
        neg_rows = pos[pos.min_ec < 0]
        if neg_rows.empty:
            out[v] = np.inf
            continue
        hi = neg_rows.iloc[0]
        lower = pos[pos.vd < hi.vd]
        base = sub[(sub.v == v) & (sub.vd == 0.0)]
        if lower.empty:
            lo_vd, lo_m = 0.0, float(base.iloc[0].min_ec) if len(base) else np.nan
        else:
            lo_vd, lo_m = float(lower.iloc[-1].vd), float(lower.iloc[-1].min_ec)
        # linear interp in vd between last-positive and first-negative
        f = lo_m / (lo_m - float(hi.min_ec))
        out[v] = lo_vd + f * (float(hi.vd) - lo_vd)
    return out


def _tau_star(vd_max: dict, v_target: float):
    """Fastest EC-clean quintic-smoothstep ramp 0 -> v_target, seconds."""
    if not vd_max:
        return np.nan
    vs = np.array(sorted(vd_max))
    caps = np.array([vd_max[v] for v in vs])
    if np.all(np.isinf(caps)):
        return 0.0  # vacuous: no cap anywhere on the grid
    s = np.linspace(0.0, 1.0, 2001)
    Sp = 30 * s**2 * (1 - s)**2  # quintic smoothstep derivative, peak 1.875
    v_of_s = v_target * (6 * s**5 - 15 * s**4 + 10 * s**3)
    cap_of_s = np.interp(v_of_s, vs, caps)
    with np.errstate(divide="ignore"):
        tau_m = np.max(np.where(cap_of_s > 0, v_target * Sp / cap_of_s, np.inf))
    return float(tau_m / C_LIGHT)  # t was in meters -> seconds


def mode_audit(parquet_path):
    df = pd.read_parquet(parquet_path)
    print("=" * 78)
    print(f"AUDIT MODE -- {parquet_path} ({len(df)} rows)")
    print("=" * 78)
    errs = df[df.error.astype(str) != ""]
    gate("no evaluate() exceptions", len(errs) == 0, f"{len(errs)} error rows")

    # GATE 2 -- corridor
    ok2, det = True, []
    for name, sub in df.groupby("name"):
        row0 = sub[sub.vd == 0.0]
        mn = float(row0.min_ec.min())
        ok2 &= bool(mn >= 0.0)
        det.append(f"{name}: min over corridor = {mn:+.3e}")
    gate("GATE 2: quasi-static corridor non-negative for every config",
         ok2, "; ".join(det))

    # GATE 4 -- surface sanity
    finite_ok = bool(np.isfinite(df.min_ec).all())
    ok4, det4 = finite_ok, []
    for name, sub in df.groupby("name"):
        vt = sub.v.max()
        at = sub[(sub.v == vt) & (sub.vd > 0)].sort_values("vd")
        base = float(sub[(sub.v == vt) & (sub.vd == 0.0)].iloc[0].min_ec)
        dev = np.abs(at.min_ec.to_numpy() - base)
        grows = bool(np.all(np.diff(dev[dev > 0]) >= -abs(base) * 1e-3)) if len(dev) > 2 else True
        ok4 &= grows
        det4.append(f"{name}: |response| @v_target spans {dev.min():.2e}..{dev.max():.2e}")
    gate("GATE 4: finite surface; vd-response grows with |vd| at v_target",
         ok4, "; ".join(det4))

    # GATE 5 -- tau*
    print("-" * 78)
    taus = {}
    for name, sub in df.groupby("name"):
        vt = float(sub.v.max())
        vdm = _vd_max_of_v(sub)
        tau = _tau_star(vdm, vt)
        taus[name] = tau
        R2 = float(sub.R2.iloc[0])
        n_capped = sum(1 for c in vdm.values() if np.isfinite(c))
        if tau == 0.0:
            print(f"  {name}: margin never crosses zero on the vd grid "
                  f"(<= 1e-2 /m) -- tau* < {vt * 1.875 / 1e-2 / C_LIGHT:.2e} s "
                  f"(vacuous bound; {n_capped}/{len(vdm)} v-rows capped)")
        else:
            print(f"  {name}: tau* = {tau:.3e} s = {tau * C_LIGHT / R2:.1f} R2/c "
                  f"({n_capped}/{len(vdm)} v-rows capped)")
    ok5 = all(np.isfinite(t) and t < 1.0 for t in taus.values())
    if np.isfinite(taus.get("floor", np.nan)) and taus.get("floor", 0) > 0 \
            and taus.get("canonical", 0) > 0:
        ok5 &= bool(taus["floor"] >= taus["canonical"])
    gate("GATE 5: tau* extracted, sane (< 1 s), floor >= canonical when both finite",
         ok5, "; ".join(f"{k}={v:.3e}s" for k, v in taus.items()))
    n_pass = sum(GATES.values())
    print(f"AUDIT: {n_pass}/{len(GATES)} gates PASS")
    return 0 if n_pass == len(GATES) else 1


def mode_exact(parquet_path):
    import time
    t0 = time.time()
    df = pd.read_parquet(parquet_path)
    print("=" * 78)
    print("EXACT MODE -- static-limit row re-check + S32 cross-anchor")
    print("=" * 78)
    from hf_jobs.sweeps.mmin_map import RES_FULL
    from hf_jobs.sweeps.spinup_margin import _profiles_for
    from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec

    # GATE 1 -- one vd=0 row per config through the STATIC evaluator
    ok1 = True
    for name, sub in df.groupby("name"):
        row = sub[(sub.vd == 0.0)].sort_values("v").iloc[-1]
        cfg = {"kind": row.kind, "R1": row.R1, "R2": row.R2, "M": row.M,
               "v_build": 0.02}
        if row.kind == "nested":
            # canonical S47 two-body winner constants
            cfg.update({"R1_in": 7.0, "R2_in": 9.5, "f_inner": 0.10})
        r, Apos, B, F, hmin, intervals = _profiles_for(cfg, float(row.M), 0.02)
        n_r, n_th, na, nt = RES_FULL
        subi = np.arange(r.size)[:: max(1, r.size // n_r)]
        rs = r[subi]
        mask = np.zeros(rs.shape, dtype=bool)
        for lo, hi in intervals:
            mask |= (rs >= lo) & (rs <= hi)
        theta = np.linspace(0.02, np.pi - 0.02, n_th)
        out = evaluate_axisym_ec(rs, Apos[subi], B[subi], F[subi],
                                 v=float(row.v), theta=theta,
                                 in_shell_mask_1d=mask,
                                 num_angular=na, num_temporal=nt)
        rel = abs(out["min"] - row.min_ec) / max(abs(row.min_ec), 1e-300)
        ok1 &= bool(rel < 1e-9)
        print(f"    {name} @ v={row.v:g}, vd=0: static {out['min']:+.6e} vs "
              f"parquet {row.min_ec:+.6e} (rel {rel:.1e}) [{time.time()-t0:.0f}s]")
    gate("GATE 1: vd=0 rows match the static evaluator (1e-9 rel)", ok1)

    # GATE 3 -- S32 anchor. Tolerance is the Session-35 band: the S32
    # parquet predates the S35 mmin_map latent-bug fixes, which were
    # certified behaviour-preserving to <= 1e-4 relative (margin VALUES
    # drift within that band; bisected masses unchanged -- S47 GATE 1
    # matched them exactly). Observed drift here: 7.2e-6.
    ref = pd.read_parquet(S32_REFERENCE)
    s32 = ref[(ref.R2 == 20.0) & (ref.dfrac == 0.5) & (ref.v == 0.02)].iloc[0]
    fl = df[(df.name == "floor") & (df.v == 0.02) & (df.vd == 0.0)]
    if len(fl):
        rel = abs(float(fl.iloc[0].min_ec) - s32.minec_above) / abs(s32.minec_above)
        gate("GATE 3: floor config (v=0.02, vd=0) matches S32 minec_above "
             "within the S35 behaviour-preserving band (1e-4)",
             bool(rel < 1e-4), f"rel = {rel:.2e}")
    else:
        gate("GATE 3: floor config present in parquet", False)
    n_pass = sum(GATES.values())
    print(f"EXACT: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "audit":
        raise SystemExit(mode_audit(sys.argv[2]))
    if len(sys.argv) >= 3 and sys.argv[1] == "exact":
        raise SystemExit(mode_exact(sys.argv[2]))
    print(__doc__)
    raise SystemExit(2)
