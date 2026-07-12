"""Session 49 -- Task 2E.1: spin-up EC margin surface min-EC(v, vd).

The rigid-profile spin-up family: the Fuchs-class TOV parts (Apos, B) and
shift form factor F are v-independent, so the comoving-form metric with
v -> v(t) is an EXACT time-dependent spacetime. Its exact Einstein tensor
(solvers.axisymmetric_ec._build_lambdas_timedep) depends on the ramp only
through (v, vd = dv/d(ct)); vdd never appears (Session-49 GATE B, exact).
Therefore the ENTIRE inflate-coast-deflate lifecycle EC question for this
family reduces to one margin surface per configuration:

    margin(v, vd) = min over the in-shell mesh of all four pointwise ECs.

Any ramp v(t) = v_target * S(t / tau) maps to the curve
(v(s), v_target S'(s) / (c tau)); the fastest EC-clean spin-up is

    tau* = max_s  v_target S'(s) / (c * vd_max(v(s))),

with vd_max(v) the positive-vd zero crossing of the margin at fixed v.
The vd = 0 row is the quasi-static corridor kill-test (a shell provisioned
for v_target should pass at every intermediate v).

Slice scope (accompanies any claim): rigid radial profiles during spin-up
(no shell restructuring -- legitimate within the family, since the TOV
parts are exactly v-independent; what is NOT captured is any additional
stress a real assembly/acceleration history might require outside this
metric family); comoving-form coordinates (shift amplitude ramps in
place); subluminal v only; constant-density Fuchs shell (+ the S47
two-body variant); canonical smoothing; EC minima over the in-matter
mask; radial representation.

Units: vd in 1/m (dv per meter of light travel). vd = 1e-3 /m means
spinning up to v = 0.02 within ~one light-crossing of the R2 = 20 m shell.
"""

from __future__ import annotations

import time
from functools import lru_cache

import numpy as np

from hf_jobs.sweeps.mmin_map import RES_FULL, shell_profiles
from hf_jobs.sweeps.mmin_map_nested import nested_shell_profiles
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec_timedep


@lru_cache(maxsize=8)
def _profiles_cached(key: tuple):
    """Profile build keyed by config values (profiles are v/vd-independent
    apart from v_build, which only scales the stored shift overlay -- the
    evaluator takes v separately, so one build serves every snapshot of a
    config; ~30-40 s saved per reused point)."""
    kind = key[0]
    if kind == "single":
        _, R1, R2, M, v_build = key
        r, Apos, B, F, M_adm, hmin = shell_profiles(R1, R2, M, v_build)
        mask_intervals = ((R1, R2),)
    elif kind == "nested":
        _, R1, R2, M, v_build, R1_in, R2_in, f_inner = key
        r, Apos, B, F, M_adm, hmin = nested_shell_profiles(
            R1, R2, R1_in, R2_in, f_inner, M, v_build)
        mask_intervals = ((R1_in, R2_in), (R1, R2))
    else:
        raise ValueError(f"unknown config kind: {kind}")
    return r, Apos, B, F, hmin, mask_intervals


def _profiles_for(cfg: dict, M: float, v_build: float):
    """Return (r, Apos, B, F, horizon_min, mask_intervals) for a config spec."""
    kind = cfg.get("kind", "single")
    R1, R2 = float(cfg["R1"]), float(cfg["R2"])
    if kind == "single":
        key = (kind, R1, R2, float(M), float(v_build))
    else:
        key = (kind, R1, R2, float(M), float(v_build),
               float(cfg["R1_in"]), float(cfg["R2_in"]),
               float(cfg["f_inner"]))
    return _profiles_cached(key)


def snapshot_min_ec(cfg: dict, M: float, v: float, vd: float,
                    res=RES_FULL):
    """One spin-up snapshot -> (min_ec, min_by_cond, horizon_min).

    NOTE the profile build uses the config's v_build only through the
    (v-independent) TOV parts and form factor; the snapshot's v enters the
    evaluator, so one profile build serves every (v, vd) point.
    """
    n_r, n_th, na, nt = res
    r, Apos, B, F, hmin, intervals = _profiles_for(cfg, M, float(cfg["v_build"]))
    if hmin < 0.05:
        return float("nan"), {}, hmin
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    rs = r[sub]
    mask = np.zeros(rs.shape, dtype=bool)
    for lo, hi in intervals:
        mask |= (rs >= lo) & (rs <= hi)
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    out = evaluate_axisym_ec_timedep(
        rs, Apos[sub], B[sub], F[sub], v=v, vd=vd, theta=theta,
        in_shell_mask_1d=mask, num_angular=na, num_temporal=nt,
    )
    return out["min"], out["min_by_cond"], hmin


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``configs x v x vd`` (vd axis: 0 plus +/- log-spaced values).

    Config schema::

        {
          "configs": [
            {"name": "canonical", "kind": "single", "R1": 10.0, "R2": 20.0,
             "M": 4.49e27, "v_build": 0.02},
            {"name": "floor",     "kind": "single", "R1": 10.0, "R2": 20.0,
             "M": 2.567991e27, "v_build": 0.02},
            {"name": "twobody",   "kind": "nested", "R1": 10.0, "R2": 20.0,
             "R1_in": 7.0, "R2_in": 9.5, "f_inner": 0.10,
             "M": 2.22558e27, "v_build": 0.02}
          ],
          "v":  {"values": [...]},
          "vd_mag": {"values": [...]},     # magnitudes; 0 and both signs added
          "res": "full"
        }
    """
    vs = [float(x) for x in config["v"]["values"]]
    mags = [float(x) for x in config["vd_mag"]["values"]]
    vds = [0.0] + [s * m for m in mags for s in (+1.0, -1.0)]
    grid: list[dict] = []
    for cfg in config["configs"]:
        for v in vs:
            for vd in vds:
                grid.append({"cfg": cfg, "v": v, "vd": vd})
    return grid


def evaluate(point: dict) -> dict:
    """One (config, v, vd) snapshot -> margin record."""
    t0 = time.time()
    cfg = point["cfg"]
    try:
        mn, by, hmin = snapshot_min_ec(
            cfg, float(cfg["M"]), float(point["v"]), float(point["vd"]))
        return {
            "name": cfg["name"], "kind": cfg.get("kind", "single"),
            "R1": cfg["R1"], "R2": cfg["R2"], "M": cfg["M"],
            "v": point["v"], "vd": point["vd"],
            "min_ec": mn,
            "min_null": by.get("null", np.nan),
            "min_weak": by.get("weak", np.nan),
            "min_dominant": by.get("dominant", np.nan),
            "min_strong": by.get("strong", np.nan),
            "binding_cond": (min(by, key=by.get) if by else ""),
            "horizon_min": hmin,
            "wall_s": time.time() - t0, "error": "",
        }
    except Exception as exc:  # sweep must not die on one bad cell
        return {
            "name": cfg.get("name"), "v": point.get("v"),
            "vd": point.get("vd"),
            "error": f"{type(exc).__name__}: {exc}",
        }
