"""Session 48 -- graded-wall minimal-mass map (ROADMAP unranked follow-on to S47).

Session 47 found the certified nested-shell optimum sitting at the
parameterization's near-wall boundary: the winner is a contiguous inward
extension of the wall at ~1.5x the wall density (an inward-graded wall), not
separated shells. This sweep replaces the two-component split with the
continuous family it was pointing at: a constant-density Fuchs wall
[R1, R2] plus a graded extension on [R1 - d, R1].

Profile family (nominal, before canonical smoothing)
----------------------------------------------------
    rho(r) = rho_w                                   r in [R1, R2]
    rho(r) = q * rho_w * t(r)                        r in [R1 - d, R1]
    rho(r) = 0                                       elsewhere
    t(r)   = 1                          (taper = "flat")
             (r - (R1 - d)) / d         (taper = "linear"; 0 at inner edge)

rho_w is set per bisection mass M by normalisation:
rho_w = M / (V_wall + q * V_ext_eff), V_ext_eff = int_{R1-d}^{R1} t(r) 4 pi r^2 dr.
The warp band stays at the canonical wall [R1, R2] (unchanged shift); the
S47 winner corresponds to ~(d = 0.3 R1, q = 1.5, flat) modulo its 0.5 m
standoff (invisible under the ~5 m smoothing).

Method per grid point: identical to mmin_map / mmin_map_nested -- the
certified find_mmin bracketing with an injected EC oracle built on the
SINGLE-shell profile builder (arbitrary rho_of_r), so d = 0 baseline points
are literally the Session-32 configuration (degenerate-limit gate).

Slice scope (accompanies any claim): constant-density wall + one graded
extension family (two shapes); TOV-pinned isotropic pressure (P(R2) = 0
inward); l=1 dipole shift via the canonical compact sigmoid at [R1, R2];
smooth_factor 4000 with canonical physical spacing (the ~5 m rho-smoothing
length exceeds most extension depths -- nominal taper shapes are partially
smeared; that is the canonical convention, inherited from S39/S47); EC
minima over the in-matter mask [R1 - d, R2]; radial representation only;
kappa bookkeeping vs the outer geometry (comparable to 3.10/S47).
"""

from __future__ import annotations

import numpy as np

from hf_jobs.sweeps.mmin_map import (
    DR_CANON,
    HORIZON_FLOOR,
    RES_FULL,
    SF,
    find_mmin,
)
from warp_factory_py.metrics.warp_shell import (
    metric_profile_warp_shell,
    _compact_sigmoid,
)
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
from warp_factory_py.utils.constants import G, c


def _rho_of_r(R1: float, R2: float, d: float, q: float, taper: str,
              M_nominal: float):
    """Return (rho callable, rho_w) for the graded-wall family at mass M."""
    V_wall = (4.0 / 3.0) * np.pi * (R2**3 - R1**3)
    if d > 0.0 and q > 0.0:
        rg = np.linspace(R1 - d, R1, 20_001)
        t = np.ones_like(rg) if taper == "flat" else (rg - (R1 - d)) / d
        V_ext_eff = float(np.trapezoid(t * 4.0 * np.pi * rg**2, rg))
    else:
        V_ext_eff = 0.0
    rho_w = M_nominal / (V_wall + q * V_ext_eff)

    def rho(r):
        wall = np.where((r >= R1) & (r <= R2), rho_w, 0.0)
        if d <= 0.0 or q <= 0.0:
            return wall
        if taper == "flat":
            tt = 1.0
        else:
            tt = (r - (R1 - d)) / d
        ext = np.where((r >= R1 - d) & (r < R1), q * rho_w * tt, 0.0)
        return wall + ext

    return rho, rho_w


def graded_shell_profiles(R1: float, R2: float, d: float, q: float,
                          taper: str, M_nominal: float, v: float):
    """Graded-wall configuration -> windowed radial profiles.

    Same windowing / diagnostics contract as ``mmin_map.shell_profiles``.
    """
    rho, _ = _rho_of_r(R1, R2, d, q, taper, M_nominal)
    centre = 1.75 * R2
    world_size = np.sqrt(3.0) * (centre - 1.0)
    r_sample_res = max(50_000, int(round(1.2 * world_size / DR_CANON)))
    _, p = metric_profile_warp_shell(
        (1, 1, 1, 1), (0.0, centre, centre, centre),
        rho_of_r=rho,
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


def make_min_ec_graded(d: float, q: float, taper: str):
    """EC oracle for one (d, q, taper) -- injectable into find_mmin."""

    def min_ec_graded(R1: float, R2: float, M_nominal: float, v: float,
                      res=RES_FULL):
        n_r, n_th, na, nt = res
        r, Apos, B, F, M_adm, hmin = graded_shell_profiles(
            R1, R2, d, q, taper, M_nominal, v)
        if hmin < HORIZON_FLOOR:
            return float("nan"), {}, M_adm, hmin
        sub = np.arange(r.size)[:: max(1, r.size // n_r)]
        rs = r[sub]
        lo = R1 - d if (d > 0.0 and q > 0.0) else R1
        mask = (rs >= lo) & (rs <= R2)
        theta = np.linspace(0.02, np.pi - 0.02, n_th)
        out = evaluate_axisym_ec(
            rs, Apos[sub], B[sub], F[sub], v=v, theta=theta,
            in_shell_mask_1d=mask, num_angular=na, num_temporal=nt,
        )
        return out["min"], out["min_by_cond"], M_adm, hmin

    return min_ec_graded


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``cells x delta_frac x q x taper`` (+ d=0 baselines).

    Config schema::

        {
          "rel_tol": 0.005,
          "cells": [{"R2": 20.0, "dfrac": 0.5, "v": 0.02}, ...],
          "delta_frac": {"values": [0.15, 0.3, ...]},   # d = delta_frac * R1
          "q": {"values": [0.5, 1.0, 1.5, ...]},
          "taper": {"values": ["flat", "linear"]},
          "include_baseline": true
        }
    """
    rel_tol = float(config.get("rel_tol", 0.005))
    dfs = [float(x) for x in config["delta_frac"]["values"]]
    qs = [float(x) for x in config["q"]["values"]]
    tapers = [str(x) for x in config["taper"]["values"]]
    grid: list[dict] = []
    for cell in config["cells"]:
        R2 = float(cell["R2"])
        dfrac = float(cell["dfrac"])
        v = float(cell["v"])
        R1 = R2 * (1.0 - dfrac)
        if config.get("include_baseline", True):
            grid.append({
                "R1": R1, "R2": R2, "dfrac": dfrac, "v": v,
                "delta_frac": 0.0, "q": 0.0, "taper": "flat",
                "rel_tol": rel_tol,
            })
        for df in dfs:
            for q in qs:
                for taper in tapers:
                    grid.append({
                        "R1": R1, "R2": R2, "dfrac": dfrac, "v": v,
                        "delta_frac": df, "q": q, "taper": taper,
                        "rel_tol": rel_tol,
                    })
    return grid


def evaluate(point: dict) -> dict:
    """One (cell, d, q, taper) -> graded M_min record."""
    try:
        R1 = float(point["R1"])
        R2 = float(point["R2"])
        v = float(point["v"])
        df = float(point["delta_frac"])
        q = float(point["q"])
        taper = str(point["taper"])
        d = df * R1
        oracle = make_min_ec_graded(d, q, taper)
        rec = find_mmin(R1, R2, v,
                        rel_tol=float(point.get("rel_tol", 0.005)),
                        min_ec_fn=oracle)
        rho_w_at_min = np.nan
        f_ext = np.nan
        if np.isfinite(rec.get("M_min_nominal", np.nan)):
            _, rho_w_at_min = _rho_of_r(R1, R2, d, q, taper,
                                        rec["M_min_nominal"])
            f_ext = 1.0 - rho_w_at_min * (4.0 / 3.0) * np.pi \
                * (R2**3 - R1**3) / rec["M_min_nominal"]
        rec.update({
            "dfrac": float(point.get("dfrac", np.nan)),
            "delta_frac": df, "q": q, "taper": taper, "d_ext": d,
            "rho_w_at_min": rho_w_at_min,
            "f_ext_at_min": f_ext,
            "error": "",
        })
        return rec
    except Exception as exc:  # sweep must not die on one bad cell
        return {
            "R1": point.get("R1"), "R2": point.get("R2"),
            "v": point.get("v"), "dfrac": point.get("dfrac"),
            "delta_frac": point.get("delta_frac"), "q": point.get("q"),
            "taper": point.get("taper"),
            "error": f"{type(exc).__name__}: {exc}",
        }
