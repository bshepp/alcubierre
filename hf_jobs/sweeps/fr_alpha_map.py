"""Session 52 -- Task 2E.2/6b Leg 1: the alpha x geometry map for f(R) = R + alpha R^2.

Bounded-negative survey extending the Session-51 first-physics probes: for
each geometry target, sweep alpha over +/- decades and record the
Jordan-frame matter EC minimum, the binding condition, and the theory
viability flags. The S51 structure (Alcubierre not rescued; Fuchs floor's
viable direction strictly degrading) is either confirmed across wall
shapes / velocities / configurations or a rescuing pocket is found.

Geometry targets: bare Alcubierre walls (three widths + a velocity
variant; Apos = B = 1, F = tanh wall -- the axisymmetric ansatz covers
them exactly) and the certified Fuchs-class configurations (S32 floor,
canonical vessel, S47 two-body winner).

Slice scope: quadratic f(R) only; Jordan-frame ECs on the matter tensor
(the loophole tested on its own terms; Einstein-frame reading dissolves
it); static; radial representation; alpha in m^2; viability = f'(R) > 0
pointwise AND alpha >= 0 (f'' >= 0).
"""

from __future__ import annotations

import time
from functools import lru_cache

import numpy as np

from hf_jobs.sweeps.mmin_map import RES_FULL, shell_profiles
from hf_jobs.sweeps.mmin_map_nested import nested_shell_profiles
from warp_factory_py.solvers.fr_matter import evaluate_axisym_ec_fr


@lru_cache(maxsize=16)
def _profiles_cached(key: tuple):
    kind = key[0]
    if kind == "alcubierre":
        _, r0, w, n_dense = key
        r = np.linspace(0.5, 45.0, int(n_dense))
        Apos = np.ones_like(r)
        B = np.ones_like(r)
        F = 0.5 * (1.0 - np.tanh((r - r0) / w))
        mask_intervals = ((max(r0 - 5 * w, 1.0), r0 + 5 * w),)
    elif kind == "single":
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
    return r, Apos, B, F, mask_intervals


def _key_for(cfg: dict):
    kind = cfg.get("kind")
    if kind == "alcubierre":
        return (kind, float(cfg["r0"]), float(cfg["w"]),
                int(cfg.get("n_dense", 60000)))
    if kind == "single":
        return (kind, float(cfg["R1"]), float(cfg["R2"]), float(cfg["M"]),
                float(cfg["v_build"]))
    if kind == "nested":
        return (kind, float(cfg["R1"]), float(cfg["R2"]), float(cfg["M"]),
                float(cfg["v_build"]), float(cfg["R1_in"]),
                float(cfg["R2_in"]), float(cfg["f_inner"]))
    raise ValueError(f"unknown config kind: {kind}")


def snapshot(cfg: dict, alpha: float, res=RES_FULL):
    n_r, n_th, na, nt = res
    r, Apos, B, F, intervals = _profiles_cached(_key_for(cfg))
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    rs = r[sub]
    mask = np.zeros(rs.shape, dtype=bool)
    for lo, hi in intervals:
        mask |= (rs >= lo) & (rs <= hi)
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    return evaluate_axisym_ec_fr(
        rs, Apos[sub], B[sub], F[sub], v=float(cfg["v"]), alpha=alpha,
        theta=theta, in_shell_mask_1d=mask, num_angular=na, num_temporal=nt)


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``configs x alpha`` (alpha axis: 0 plus +/- magnitudes)."""
    mags = [float(x) for x in config["alpha_mag"]["values"]]
    alphas = [0.0] + [s * m for m in mags for s in (+1.0, -1.0)]
    grid: list[dict] = []
    for cfg in config["configs"]:
        for alpha in alphas:
            grid.append({"cfg": cfg, "alpha": alpha})
    return grid


def evaluate(point: dict) -> dict:
    t0 = time.time()
    cfg = point["cfg"]
    try:
        o = snapshot(cfg, float(point["alpha"]))
        by = o["min_by_cond"]
        return {
            "name": cfg["name"], "kind": cfg["kind"], "v": cfg["v"],
            "alpha": point["alpha"],
            "min_ec": o["min"],
            "min_null": by.get("null", np.nan),
            "min_weak": by.get("weak", np.nan),
            "min_dominant": by.get("dominant", np.nan),
            "min_strong": by.get("strong", np.nan),
            "binding_cond": (min(by, key=by.get) if by else ""),
            "fprime_min": o["fprime_min"],
            "viable": o["viable"],
            "R_absmax": float(np.abs(o["R_scalar"]).max()),
            "wall_s": time.time() - t0, "error": "",
        }
    except Exception as exc:
        return {
            "name": cfg.get("name"), "alpha": point.get("alpha"),
            "error": f"{type(exc).__name__}: {exc}",
        }
