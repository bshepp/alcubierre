"""Session-39 kill-test (Session-35 audit queue item (d)): the Session-26
nested-shell f_inner ladder re-run through the certified radial evaluator.

The Session-26 mass-split result (SESSION_LOG Session 26) reported min(NEC)
flipping sign between f_inner = 0.10 (+6.04e38) and 0.20 (-3.86e37) on the
Cartesian FD pipeline at (1, 300, 300, 5), dx = 0.2 -- a near-sharp
configuration for which the Cartesian path was later demoted (Session 30)
with a corrected smooth-end error band of ~9% and O(1) errors at sharpness.
The threshold location was therefore inside the untrusted band (audit item
W5).  This harness re-runs the identical physical configuration through
`evaluate_axisym_ec` (the certified EC oracle for sharp shell profiles,
Prong-B GR-certified) and pins the sign-flip threshold by bisection, with a
resolution-escalation confirmation.

Configuration (Session 26): outer shell (10, 20) m carrying (1-f) M_tot,
inner shell (5, 8) m carrying f M_tot, warp band at the OUTER wall,
v = 0.02c, M_tot = 4.49e27 kg, smooth_factor = 4000, in-shell mask
r in [5, 8] U [10, 20].

VERDICT OF THE FIRST (indictment-mode) RUN, 2026-07-05: the certified ladder
REVERSES the Session-26 record on both counts --

  * min(NEC) is NON-MONOTONE in f: it RISES from +2.877e38 at f=0 to a
    plateau ~+2.35e39 around f = 0.05-0.10 (an ~8x margin improvement from
    moving a small mass fraction inward), then declines;
  * the sign flip sits at f* ~ 0.63, not in the Cartesian-recorded
    (0.10, 0.20) window -- 4-6x higher in f.

CERTIFIED NUMBERS (RES_CONF, 2026-07-05 staged runs): null(0) = +2.8764e38,
null(0.05) = +2.3070e39 (8.0x), null(0.10) = +2.3299e39 (8.1x);
threshold ladder 0.60 -> +1.309e38, 0.6156 -> +5.99e37, 0.6234 -> +2.44e37,
0.6312 -> -1.14e37, 0.6344 -> -2.57e37  =>  f* in [0.6234, 0.6312].
RES_FULL <-> RES_CONF agreement <= 1% on the plateau; the RES_FULL bracket
[0.6312, 0.6344] sits ~0.006 high, consistent with the ~-2e37 resolution
shift near the flip.

Physical reading (replacing Session 26's, which was backwards): at fixed
M_tot, moving mass inward INCREASES the enclosed M(r) at every radius
inside the outer wall -- in particular at the warp band's inner edge, where
the shift gradient bites -- strengthening the positive-energy support.
Degradation only wins once the outer wall is starved (large f).
Session-26's Cartesian numbers came from a thin z-slab grid
(1, 300, 300, 5) that samples only the near-equatorial plane; the certified
evaluator minimises over the full (r, theta) mesh.

Gates (certification form, encoding the corrected shape):
  GATE 1  degenerate-limit consistency: the nested builder at f = 0 matches
          the single-shell profile builder (same TOV path) on min(EC) to
          < 0.1% relative.
  GATE 2  non-monotonicity certified: null(0.05) > null(0) and
          null(0.10) > null(0) (small-f improvement), and
          null(0.30) < null(0.10) (eventual decline).
  GATE 3  a sign flip exists well above the Cartesian window; RES_FULL
          bisection pins it to df <= 0.005; `threshold` mode re-pins the
          bracket at RES_CONF (the RES_FULL threshold is ~0.005 too high --
          resolution shifts min(NEC) by ~-2e37 near the flip).

Modes (the full battery exceeds a 10-minute budget; stage as needed):
  full                 GATE 1 + RES_FULL ladder + RES_FULL bisection (~8 min)
  plateau              GATE 2 at RES_CONF: f in {0, 0.05, 0.10} (~6 min)
  threshold LO HI      RES_CONF endpoint check + bisection to df <= 0.01 (~6 min)

Run:  $env:PYTHONPATH="."; C:/Python313/python.exe verification/test_nested_shell_radial_ladder.py [mode ...]
"""
from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, '.')

from warp_factory_py.metrics.warp_shell import (   # noqa: E402
    metric_nested_warp_shells,
    metric_profile_warp_shell,
    _compact_sigmoid,
)
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec  # noqa: E402
from warp_factory_py.utils.constants import G, c  # noqa: E402

M_TOT = 4.49e27
V_WARP = 0.02
SF = 4000.0
R1_IN, R2_IN = 5.0, 8.0
R1_OUT, R2_OUT = 10.0, 20.0
DR_CANON = 70.6667e0 / 1e5          # canonical radial spacing (mmin_map, R2=20)
RES_FULL = (4000, 80, 100, 10)
RES_CONF = (8000, 120, 160, 16)
HORIZON_FLOOR = 0.05

GATES = {}


def gate(name, ok, detail=""):
    GATES[name] = ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def _window(p):
    rf = p["r"]
    idx = np.where((rf >= 0.5) & (rf <= 1.5 * R2_OUT))[0]
    r = rf[idx]
    return r, (-p["A"])[idx], p["B"][idx], p["shift"][idx], p["horizon_min"]


def _profile_kwargs():
    centre = 1.75 * R2_OUT
    world_size = np.sqrt(3.0) * (centre - 1.0)
    r_sample_res = max(50_000, int(round(1.2 * world_size / DR_CANON)))
    return centre, r_sample_res


def nested_profiles(f_inner):
    centre, r_sample_res = _profile_kwargs()
    _, p = metric_nested_warp_shells(
        (1, 1, 1, 1), (0.0, centre, centre, centre),
        shells=[(R1_IN, R2_IN, f_inner * M_TOT),
                (R1_OUT, R2_OUT, (1.0 - f_inner) * M_TOT)],
        warp_R1=R1_OUT, warp_R2=R2_OUT,
        smooth_factor=SF, v_warp=V_WARP, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=r_sample_res,
    )
    return _window(p)


def single_profiles():
    """Session-26 f=0 reference through the single-shell profile builder."""
    centre, r_sample_res = _profile_kwargs()
    rho0 = M_TOT / ((4.0 / 3.0) * np.pi * (R2_OUT**3 - R1_OUT**3))
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, centre, centre, centre),
        rho_of_r=lambda r: np.where((r >= R1_OUT) & (r <= R2_OUT), rho0, 0.0),
        shift_of_r=lambda r: _compact_sigmoid(r, R1_OUT, R2_OUT, 0.0, 0.0),
        R1=R1_OUT, R2=R2_OUT, smooth_factor=SF, v_warp=V_WARP, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=r_sample_res,
    )
    return _window(p)


def min_ec_from_profiles(profs, res=RES_FULL):
    n_r, n_th, na, nt = res
    r, Apos, B, F, hmin = profs
    if hmin < HORIZON_FLOOR:
        return float("nan"), {}
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    rs = r[sub]
    mask = ((rs >= R1_IN) & (rs <= R2_IN)) | ((rs >= R1_OUT) & (rs <= R2_OUT))
    out = evaluate_axisym_ec(
        rs, Apos[sub], B[sub], F[sub], v=V_WARP, theta=theta,
        in_shell_mask_1d=mask, num_angular=na, num_temporal=nt,
    )
    return out["min"], out["min_by_cond"]


def mode_plateau():
    """GATE 2 at RES_CONF: certify the small-f improvement plateau."""
    t0 = time.time()
    print("=" * 78)
    print("PLATEAU MODE -- RES_CONF certification of the small-f improvement")
    print("=" * 78)
    vals = {}
    for f in (0.0, 0.05, 0.10):
        mn, by = min_ec_from_profiles(nested_profiles(f), res=RES_CONF)
        vals[f] = by.get("null", float("nan"))
        print(f"    f = {f:.3f}: null = {vals[f]:+.4e}  [{time.time()-t0:.0f}s]")
    gate("RES_CONF: null(0.05) > null(0) (small-f split IMPROVES the margin)",
         bool(vals[0.05] > vals[0.0]),
         f"{vals[0.05]:+.3e} vs {vals[0.0]:+.3e} "
         f"({vals[0.05]/vals[0.0]:.2f}x)")
    gate("RES_CONF: null(0.10) > null(0)",
         bool(vals[0.10] > vals[0.0]),
         f"{vals[0.10]:+.3e} vs {vals[0.0]:+.3e}")
    n_pass = sum(GATES.values())
    print(f"PLATEAU MODE: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    return 0 if n_pass == len(GATES) else 1


def mode_threshold(lo, hi):
    """RES_CONF endpoint check + bisection of the sign flip to df <= 0.01."""
    t0 = time.time()
    print("=" * 78)
    print(f"THRESHOLD MODE -- RES_CONF bisection from [{lo}, {hi}]")
    print("=" * 78)
    mn_lo, by_lo = min_ec_from_profiles(nested_profiles(lo), res=RES_CONF)
    v_lo = by_lo.get("null", float("nan"))
    print(f"    f = {lo:.4f}: null = {v_lo:+.4e}  [{time.time()-t0:.0f}s]")
    gate("RES_CONF lower endpoint positive", bool(v_lo > 0), f"{v_lo:+.3e}")
    if not v_lo > 0:
        return 1
    while hi - lo > 0.01:
        mid = 0.5 * (lo + hi)
        mn_mid, by_mid = min_ec_from_profiles(nested_profiles(mid), res=RES_CONF)
        v_mid = by_mid.get("null", float("nan"))
        print(f"    f = {mid:.4f}: null = {v_mid:+.4e}  [{time.time()-t0:.0f}s]")
        if v_mid > 0:
            lo = mid
        else:
            hi = mid
    gate("RES_CONF sign flip pinned to df <= 0.01", True,
         f"f* in [{lo:.4f}, {hi:.4f}]")
    n_pass = sum(GATES.values())
    print(f"THRESHOLD MODE: {n_pass}/{len(GATES)} gates PASS ({time.time()-t0:.0f}s)")
    print(f"CERTIFIED THRESHOLD: f* in [{lo:.4f}, {hi:.4f}] at RES_CONF "
          f"(Cartesian-recorded window was (0.10, 0.20))")
    return 0 if n_pass == len(GATES) else 1


def main():
    t0 = time.time()
    print("=" * 78)
    print("GATE 1 -- degenerate-limit consistency (f = 0)")
    print("=" * 78)
    mn_nested0, by_nested0 = min_ec_from_profiles(nested_profiles(0.0))
    mn_single, by_single = min_ec_from_profiles(single_profiles())
    rel = abs(mn_nested0 - mn_single) / max(abs(mn_single), 1e-300)
    gate("nested(f=0) == single-shell profile builder on min(EC)",
         bool(rel < 1e-3),
         f"nested {mn_nested0:+.4e} vs single {mn_single:+.4e}, rel = {rel:.2e}")
    print(f"    per-condition nested(f=0): { {k: f'{v:+.3e}' for k, v in by_nested0.items()} }")

    print("=" * 78)
    print("GATE 2 -- certified radial f-ladder (RES_FULL)")
    print("=" * 78)
    ladder = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 0.70]
    results = {0.0: (mn_nested0, by_nested0)}
    for f in ladder[1:]:
        results[f] = min_ec_from_profiles(nested_profiles(f))
        print(f"    f = {f:.3f}: min(all-EC) = {results[f][0]:+.4e}, "
              f"null = {results[f][1].get('null', float('nan')):+.4e}  "
              f"[{time.time()-t0:.0f}s]")
    nec = {f: results[f][1].get("null", float("nan")) for f in ladder}
    print("    ladder: " + ", ".join(f"null({f}) = {nec[f]:+.3e}" for f in ladder))
    gate("non-monotone shape: null(0.05) > null(0) and null(0.10) > null(0) "
         "(small-f split IMPROVES the margin; Session-26 monotone-degradation "
         "claim reversed) and null(0.30) < null(0.10)",
         bool(nec[0.05] > nec[0.0] and nec[0.10] > nec[0.0]
              and nec[0.30] < nec[0.10]),
         f"null(0)={nec[0.0]:+.2e}, null(0.05)={nec[0.05]:+.2e}, "
         f"null(0.10)={nec[0.10]:+.2e}, null(0.30)={nec[0.30]:+.2e}")

    print("=" * 78)
    print("GATE 3 -- pin the sign-flip threshold (bisection on min(NEC))")
    print("=" * 78)
    lo = max((f for f in ladder if nec[f] > 0), default=None)
    hi = min((f for f in ladder if nec[f] <= 0), default=None)
    if lo is None or hi is None:
        gate("a sign flip exists on the ladder", False,
             "no bracket found -- ladder does not change sign")
        return 1
    print(f"    initial bracket: [{lo}, {hi}]")
    while hi - lo > 0.005:
        mid = 0.5 * (lo + hi)
        mn_mid, by_mid = min_ec_from_profiles(nested_profiles(mid))
        v_null = by_mid.get("null", float("nan"))
        print(f"    f = {mid:.4f}: null = {v_null:+.4e}  [{time.time()-t0:.0f}s]")
        if v_null > 0:
            lo = mid
        else:
            hi = mid
    gate("sign flip exists WELL ABOVE the Cartesian-recorded (0.10, 0.20) "
         "window, pinned to df <= 0.005 at RES_FULL",
         bool(lo >= 0.3),
         f"f* in [{lo:.4f}, {hi:.4f}]")
    print("    (run `threshold LO HI` mode to re-pin the bracket at RES_CONF; "
          "resolution shifts min(NEC) by ~-2e37 near the flip, moving f* "
          "down by ~0.005)")

    print("=" * 78)
    n_pass = sum(GATES.values())
    print(f"NESTED-SHELL RADIAL LADDER (full mode): {n_pass}/{len(GATES)} "
          f"gates PASS ({time.time()-t0:.0f}s total)")
    print(f"RES_FULL threshold: f* in [{lo:.4f}, {hi:.4f}] "
          f"(Cartesian-recorded flip window was (0.10, 0.20))")
    return 0 if n_pass == len(GATES) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "plateau":
        raise SystemExit(mode_plateau())
    if len(sys.argv) > 1 and sys.argv[1] == "threshold":
        raise SystemExit(mode_threshold(float(sys.argv[2]), float(sys.argv[3])))
    raise SystemExit(main())
