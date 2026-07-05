"""Task 3.10 -- certified minimal-mass map for the constant-density Fuchs shell.

Locates, per (R1, R2, v) cell, the minimal nominal / ADM mass at which a plain
constant-density Fuchs-class warp shell passes all four pointwise energy
conditions in the certified radial evaluator
(:mod:`warp_factory_py.solvers.axisymmetric_ec` -- Prong-B GR-certified for
sharp profiles, Session 30). Follow-up to the Sessions 29-31 over-provisioning
finding: the canonical shell passes at nominal 2.7e27 kg (ADM 2.786e27), ~40%
below the canonical 4.49e27, but the true floor was never located -- 2.7e27
was simply the lowest mass ever probed.

Method per grid point
---------------------
1. Seed the scan from the 2A.9b scaling law
   ``M_pred = KAPPA_SEED * v * R2**2 * c**2 / (2 G Delta)`` (kappa seed 5.0,
   mid 2A.9b bracket). The seed only centres the scan; it never accepts.
2. Scout ladder at ``RES_SCOUT`` (coarse mesh) to propose a [fail, pass]
   bracket in M.
3. Re-verify both bracket endpoints at ``RES_FULL`` -- the accept/reject tier.
   (S28-S31 methodological rule: the loop objective must be evaluated at
   converged sampling; the coarse tier proposes, it never decides.)
4. Bisect at ``RES_FULL`` to ``rel_tol`` relative precision on M.
5. Report nominal + ADM thresholds, implied kappa (both bookkeepings), the
   binding energy condition, and min(EC) just above/below the threshold.

Cells where the EC-passing floor collides with the horizon cap
(2 G M(r) / (r c^2) -> 1 inside the shell) are reported ``no_pass=True`` with
``horizon_capped=True`` -- the certified-radial analogue of the Session-19
(3.2) "null configuration" cells -- rather than a fabricated threshold.
IMPORTANT (Session-32 spot-check catch): min-EC vs M is NOT monotone -- it is
(physically) unimodal on the horizon-valid range, so the EC-passing window
can be NARROW and sit between two EC-FAIL scout rungs (observed at
(R1,R2,v)=(10,20,0.05c): window ~[7.4e27, <9.8e27] between the 1.0x and
1.45x rungs, both of which fail EC). Before declaring a cell capped, the
bracketer golden-section MAXIMIZES scout min-EC over the horizon-valid mass
range; only if the located peak is still negative is the cell recorded
``no_pass`` (a verdict that inherits the unimodality assumption).
``M_horizon_edge`` (lowest horizon-invalid mass seen), ``M_scout_peak`` and
``scout_peak_minec`` are reported for capped cells so the basis of the
no-pass verdict is explicit.

Slice scope (must accompany any claim built on this map): constant-density
rho(r) on [R1, R2]; TOV-pinned isotropic pressure (P(R2)=0, integrated
inward); l=1 dipole Alcubierre shift via the canonical compact sigmoid
(sigma=0, Rbuff=0); smooth_factor=4000 with the canonical radial sample
spacing dr ~= 7.07e-4 m held fixed across cells (r_sample_res scaled with the
domain so the *physical* smoothing length matches Sessions 25-31); EC minima
over the in-shell mask [R1, R2] x theta in [0.02, pi-0.02]; radial
representation only (Cartesian demoted to smooth-only cross-check per 3.9).
Note for thin cells (Delta comparable to the ~5 m rho-smoothing length) the
smoothed profile is strongly flattened; that is a property of the canonical
smoothing convention, not a bug -- kappa comparisons across Delta inherit it.
"""

from __future__ import annotations

import time

import numpy as np

from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell,
    _compact_sigmoid,
)
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
from warp_factory_py.utils.constants import G, c

SF = 4000.0                  # canonical Fuchs smoothing (Sessions 25-31)
DR_CANON = 70.6667e0 / 1e5   # canonical radial sample spacing [m] (R2=20 setup)
KAPPA_SEED = 5.0             # 2A.9b mid-bracket; scan seed only, never accepts
HORIZON_FLOOR = 0.05         # min allowed (1 - 2GM/rc^2) before "horizon-invalid"

# Resolution tiers: (n_r, n_th, num_angular, num_temporal)
RES_SCOUT = (1500, 40, 60, 6)     # bracket proposal only -- never accepts
RES_FULL = (4000, 80, 100, 10)    # accept/reject tier (S31 full-res settings)
RES_CONF = (8000, 120, 160, 16)   # escalation tier (verification harness)

SCOUT_FACTORS = (0.30, 0.45, 0.65, 1.0, 1.45, 2.1, 3.0)


def shell_profiles(R1: float, R2: float, M_nominal: float, v: float):
    """Constant-density shell -> windowed radial profiles + diagnostics.

    Returns ``(r, Apos, B, F, M_adm, horizon_min)`` on the full-resolution
    window ``[0.5, 1.5*R2]`` (subsample later, per tier).
    """
    rho0 = M_nominal / ((4.0 / 3.0) * np.pi * (R2**3 - R1**3))
    centre = 1.75 * R2
    world_size = np.sqrt(3.0) * (centre - 1.0)
    r_sample_res = max(50_000, int(round(1.2 * world_size / DR_CANON)))
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, centre, centre, centre),
        rho_of_r=lambda r: np.where((r >= R1) & (r <= R2), rho0, 0.0),
        shift_of_r=lambda r: _compact_sigmoid(r, R1, R2, 0.0, 0.0),
        R1=R1, R2=R2, smooth_factor=SF, v_warp=v, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=r_sample_res,
    )
    rf = p["r"]
    idx = np.where((rf >= 0.5) & (rf <= 1.5 * R2))[0]
    r = rf[idx]
    Apos = (-p["A"])[idx]
    B = p["B"][idx]
    F = p["shift"][idx]
    m_running = (r * c**2 / (2.0 * G)) * (1.0 - 1.0 / np.maximum(B, 1e-300))
    M_adm = float(np.interp(1.3 * R2, r, m_running))
    horizon_min = float(p.get(
        "horizon_min",
        (1.0 - 2.0 * G * m_running / (r * c**2 + 1e-30)).min(),
    ))
    return r, Apos, B, F, M_adm, horizon_min


def min_ec(R1: float, R2: float, M_nominal: float, v: float, res=RES_FULL):
    """min(EC) over the in-shell mesh at one (geometry, mass, resolution).

    Returns ``(min_ec, min_by_cond, M_adm, horizon_min)``. ``min_ec`` is NaN
    when the configuration is horizon-invalid (metric not evaluable).
    """
    n_r, n_th, na, nt = res
    r, Apos, B, F, M_adm, hmin = shell_profiles(R1, R2, M_nominal, v)
    if hmin < HORIZON_FLOOR:
        return float("nan"), {}, M_adm, hmin
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    out = evaluate_axisym_ec(
        r[sub], Apos[sub], B[sub], F[sub], v=v, theta=theta,
        in_shell_mask_1d=(r[sub] >= R1) & (r[sub] <= R2),
        num_angular=na, num_temporal=nt,
    )
    return out["min"], out["min_by_cond"], M_adm, hmin


def _passes(mn: float) -> bool:
    return np.isfinite(mn) and mn >= 0.0


def find_mmin(R1: float, R2: float, v: float, rel_tol: float = 0.005) -> dict:
    """Bisect the minimal EC-passing nominal mass for one (R1, R2, v) cell."""
    t0 = time.time()
    Delta = R2 - R1
    M_pred = KAPPA_SEED * v * R2**2 * c**2 / (2.0 * G * Delta)
    n_scout = n_full = 0
    horizon_seen = False

    def scout(M):
        nonlocal n_scout, horizon_seen
        n_scout += 1
        mn, _, _, hmin = min_ec(R1, R2, M, v, RES_SCOUT)
        if not np.isfinite(mn):
            horizon_seen = True
        return mn

    def full(M):
        nonlocal n_full, horizon_seen
        n_full += 1
        mn, by, M_adm, hmin = min_ec(R1, R2, M, v, RES_FULL)
        if not np.isfinite(mn):
            horizon_seen = True
        return mn, by, M_adm

    base = dict(
        R1=R1, R2=R2, v=v, Delta_over_R2=Delta / R2, M_pred_seed=M_pred,
    )

    # --- scout ladder: propose bracket -------------------------------------
    ladder = [f * M_pred for f in SCOUT_FACTORS]
    results = {M: scout(M) for M in ladder}
    passing = sorted(M for M, mn in results.items() if _passes(mn))
    # extend upward while nothing passes and no horizon wall yet
    M_hi_try = ladder[-1]
    while not passing and not horizon_seen and M_hi_try < 12.0 * M_pred:
        M_hi_try *= 1.45
        results[M_hi_try] = scout(M_hi_try)
        if _passes(results[M_hi_try]):
            passing = [M_hi_try]
    if not passing:
        # min-EC vs M is (physically) unimodal on the horizon-valid range:
        # the NEC margin rises with M (mass support against the shift's
        # negative contribution) while the high-compactness margin falls
        # (TOV pressure), so a NARROW passing window can hide between two
        # EC-FAIL rungs -- observed at (10, 20, 0.05c): window ~[7.4e27,
        # <9.8e27] sits between the 1.0x and 1.45x rungs, BOTH of which
        # fail EC (the first bracketing fix searched fail->horizon and
        # missed it). Golden-section MAXIMIZE scout min-EC over the valid
        # mass range before declaring the cell capped. Unimodality is an
        # assumption (one rising + one falling margin curve); it is recorded
        # here and the no-pass verdict inherits it.
        valid = sorted(M for M, mn in results.items() if np.isfinite(mn))
        walls_now = sorted(M for M, mn in results.items()
                           if not np.isfinite(mn))
        if valid:
            a = valid[0]
            b = walls_now[0] * 0.999 if walls_now else valid[-1]
            gr = 0.6180339887498949
            c1 = b - gr * (b - a)
            c2 = a + gr * (b - a)
            f1, f2 = scout(c1), scout(c2)
            results[c1], results[c2] = f1, f2
            for _ in range(16):
                if _passes(f1) or _passes(f2):
                    break
                v1 = f1 if np.isfinite(f1) else -np.inf
                v2 = f2 if np.isfinite(f2) else -np.inf
                if v1 < v2:
                    a, c1, f1 = c1, c2, f2
                    c2 = a + gr * (b - a)
                    f2 = scout(c2)
                    results[c2] = f2
                else:
                    b, c2, f2 = c2, c1, f1
                    c1 = b - gr * (b - a)
                    f1 = scout(c1)
                    results[c1] = f1
            passing = sorted(M for M in (c1, c2)
                             if _passes(results.get(M, np.nan)))
    wall_edge_all = [M for M, mn in results.items() if not np.isfinite(mn)]
    M_horizon_edge = min(wall_edge_all) if wall_edge_all else np.nan
    finite_res = {M: mn for M, mn in results.items() if np.isfinite(mn)}
    M_scout_peak = max(finite_res, key=finite_res.get) if finite_res else np.nan
    scout_peak_minec = finite_res.get(M_scout_peak, np.nan)
    if not passing:
        return {
            **base, "no_pass": True, "horizon_capped": bool(horizon_seen),
            "M_horizon_edge": M_horizon_edge,
            "M_scout_peak": M_scout_peak,
            "scout_peak_minec": scout_peak_minec,
            "M_min_nominal": np.nan, "M_min_adm": np.nan,
            "kappa_nominal": np.nan, "kappa_adm": np.nan,
            "binding_cond": "", "minec_above": np.nan, "minec_below": np.nan,
            "n_eval_scout": n_scout, "n_eval_full": n_full,
            "wall_s": time.time() - t0,
        }
    lo_candidates = sorted(
        M for M, mn in results.items()
        if M < passing[0] and np.isfinite(mn) and mn < 0.0
    )
    M_pass = passing[0]
    M_fail = lo_candidates[-1] if lo_candidates else None
    # extend downward if even the lowest scout mass passed
    M_lo_try = min(results)
    while M_fail is None and M_lo_try > 0.02 * M_pred:
        M_lo_try *= 0.65
        mn = scout(M_lo_try)
        if np.isfinite(mn) and mn < 0.0:
            M_fail = M_lo_try
        elif _passes(mn):
            M_pass = M_lo_try
    if M_fail is None:
        return {
            **base, "no_pass": False, "horizon_capped": False,
            "unbounded_below": True, "M_horizon_edge": M_horizon_edge,
            "M_min_nominal": M_pass, "M_min_adm": np.nan,
            "kappa_nominal": np.nan, "kappa_adm": np.nan,
            "binding_cond": "", "minec_above": np.nan, "minec_below": np.nan,
            "n_eval_scout": n_scout, "n_eval_full": n_full,
            "wall_s": time.time() - t0,
        }

    # --- verify bracket endpoints at the accept/reject tier ----------------
    # Walk / bisect at full res until a passing upper endpoint is found.
    # Invariants: M_fail = highest known full/scout finite-EC-fail (always a
    # genuine EC fail, never a horizon point); M_horizon_edge = lowest known
    # horizon-invalid mass (NaN if none). A horizon-invalid probe is NOT an
    # EC lower bound -- it caps the search from above.
    mn_hi, by_hi, adm_hi = full(M_pass)
    it_guard = 0
    while not _passes(mn_hi):
        it_guard += 1
        if np.isfinite(mn_hi):
            M_fail = M_pass          # genuine EC fail -> floor is higher
            nxt = M_pass * 1.25
            if np.isfinite(M_horizon_edge):
                nxt = min(nxt, 0.5 * (M_pass + M_horizon_edge))
        else:                        # stepped past a horizon wall
            M_horizon_edge = (
                M_pass if not np.isfinite(M_horizon_edge)
                else min(M_horizon_edge, M_pass)
            )
            nxt = 0.5 * (M_fail + M_horizon_edge)
        no_room = (
            np.isfinite(M_horizon_edge)
            and (M_horizon_edge - M_fail) / M_horizon_edge < rel_tol
        )
        if nxt > 20.0 * M_pred or no_room or it_guard > 40:
            return {
                **base, "no_pass": True, "horizon_capped": bool(horizon_seen),
                "M_horizon_edge": M_horizon_edge,
                "M_min_nominal": np.nan, "M_min_adm": np.nan,
                "kappa_nominal": np.nan, "kappa_adm": np.nan,
                "binding_cond": "", "minec_above": np.nan,
                "minec_below": np.nan,
                "n_eval_scout": n_scout, "n_eval_full": n_full,
                "wall_s": time.time() - t0,
            }
        M_pass = nxt
        mn_hi, by_hi, adm_hi = full(M_pass)
    mn_lo, by_lo, adm_lo = full(M_fail)
    while _passes(mn_lo):
        # scout-fail actually passes at full res; walk downward
        # (adm_hi must track M_pass -- a stale adm_hi here would misreport
        # M_min_adm/kappa_adm by up to one scout rung if the bisection then
        # accepts no midpoint)
        M_pass, mn_hi, by_hi, adm_hi = M_fail, mn_lo, by_lo, adm_lo
        M_fail *= 0.75
        mn_lo, by_lo, adm_lo = full(M_fail)
        if not np.isfinite(mn_lo):
            # Defensive: horizon validity is monotone in M, so a
            # horizon-invalid probe BELOW a full-res pass should be
            # unreachable. Per the bracket invariant above, a horizon point
            # must never serve as the EC-fail bisection endpoint -- return
            # the certified pass as an upper bound with a loud anomaly flag
            # instead of silently bisecting against a horizon wall.
            return {
                **base, "no_pass": False, "horizon_capped": True,
                "horizon_below_anomaly": True,
                "M_horizon_edge": M_horizon_edge,
                "M_min_nominal": M_pass, "M_min_adm": adm_hi,
                "kappa_nominal": np.nan, "kappa_adm": np.nan,
                "binding_cond": min(by_hi, key=by_hi.get) if by_hi else "",
                "minec_above": mn_hi, "minec_below": np.nan,
                "n_eval_scout": n_scout, "n_eval_full": n_full,
                "wall_s": time.time() - t0,
            }

    # --- bisection at the accept/reject tier -------------------------------
    while (M_pass - M_fail) / M_pass > rel_tol:
        M_mid = 0.5 * (M_pass + M_fail)
        mn_mid, by_mid, adm_mid = full(M_mid)
        if _passes(mn_mid):
            M_pass, mn_hi, by_hi, adm_hi = M_mid, mn_mid, by_mid, adm_mid
        else:
            M_fail, mn_lo = M_mid, mn_mid

    C_min_nom = 2.0 * G * M_pass / (R2 * c**2)
    C_min_adm = 2.0 * G * adm_hi / (R2 * c**2)
    kappa_nom = (Delta / R2) * C_min_nom / v
    kappa_adm = (Delta / R2) * C_min_adm / v
    binding = min(by_hi, key=by_hi.get) if by_hi else ""
    return {
        **base, "no_pass": False, "horizon_capped": False,
        "M_horizon_edge": M_horizon_edge,
        "M_min_nominal": M_pass, "M_min_adm": adm_hi,
        "M_fail_below": M_fail,
        "kappa_nominal": kappa_nom, "kappa_adm": kappa_adm,
        "binding_cond": binding,
        "minec_above": mn_hi, "minec_below": mn_lo,
        "n_eval_scout": n_scout, "n_eval_full": n_full,
        "wall_s": time.time() - t0,
    }


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``axes: {R2: {values}, dfrac: {values}, v: {values}}``.

    ``dfrac`` is Delta/R2; each point carries explicit R1 = R2 (1 - dfrac).
    """
    axes = config["axes"]
    r2s = [float(x) for x in axes["R2"]["values"]]
    dfracs = [float(x) for x in axes["dfrac"]["values"]]
    vs = [float(x) for x in axes["v"]["values"]]
    rel_tol = float(config.get("rel_tol", 0.005))
    grid = []
    for R2 in r2s:
        for dfrac in dfracs:
            for v in vs:
                grid.append({
                    "R1": R2 * (1.0 - dfrac), "R2": R2, "dfrac": dfrac,
                    "v": v, "rel_tol": rel_tol,
                })
    return grid


def evaluate(point: dict) -> dict:
    """One grid cell -> M_min record (exceptions become an error column)."""
    try:
        rec = find_mmin(
            float(point["R1"]), float(point["R2"]), float(point["v"]),
            rel_tol=float(point.get("rel_tol", 0.005)),
        )
        rec["dfrac"] = float(point.get("dfrac", np.nan))
        rec["error"] = ""
        return rec
    except Exception as exc:  # sweep must not die on one bad cell
        return {
            "R1": point.get("R1"), "R2": point.get("R2"),
            "v": point.get("v"), "dfrac": point.get("dfrac"),
            "error": f"{type(exc).__name__}: {exc}",
        }
