"""Session 47 -- nested-variant minimal-mass map (ROADMAP unranked candidate).

Follow-up to the Session-39 reversal (verification/test_nested_shell_radial_
ladder.py): at the canonical Fuchs cell, splitting 5-10% of M_tot into an
inner shell RAISES the certified min(NEC) margin ~8x at fixed mass. This
sweep asks the question that matters for the landscape: does that margin
improvement convert into a LOWER certified minimal mass? Per (cell, f_inner,
inner-geometry) point it bisects the minimal EC-passing nominal mass exactly
as Task 3.10 did for single shells, reusing the certified bracketing /
horizon-wall / golden-section logic of :func:`hf_jobs.sweeps.mmin_map.
find_mmin` unchanged (injected EC oracle; the search machinery stays
single-sourced).

Method per grid point
---------------------
Identical to mmin_map (scout ladder at RES_SCOUT proposes, RES_FULL
accepts/rejects, bisection to rel_tol), with the EC oracle evaluating the
NESTED two-shell configuration: inner shell (R1_in, R2_in) carrying
f_inner * M, outer shell (R1_out, R2_out) carrying (1 - f_inner) * M, warp
band at the OUTER wall (Session 26/39 convention), per-shell inward TOV
(P = 0 at each shell's outer surface), canonical smoothing.

Slice scope (must accompany any claim built on this map)
--------------------------------------------------------
Constant-density shells; TOV-pinned isotropic pressure per shell; l=1 dipole
Alcubierre shift via the canonical compact sigmoid (sigma=0, Rbuff=0) at the
OUTER wall only; smooth_factor=4000 with the canonical physical sample
spacing (DR_CANON) -- NOTE the ~5 m rho-smoothing length exceeds some
inner-to-outer gaps in the grid (e.g. b_in = 0.475), where the two shells
partially merge; that is a property of the canonical smoothing convention,
inherited from Session 39, not a bug. EC minima over the in-matter mask:
outer shell always, inner shell when f_inner > 0 (vacuum satisfies the ECs
trivially; at f_inner = 0 this reduces exactly to the single-shell
convention). Radial representation only (Cartesian demoted per 3.9). kappa
bookkeeping vs the OUTER geometry (directly comparable to the 3.10 map).

Inner geometry is specified as fractions of the outer radius:
R1_in = a_in * R2_out, R2_in = b_in * R2_out, requiring b_in * R2_out <
R1_out (non-overlap). f_inner = 0 baseline points (one per cell) tie each
cell back to the Session-32 single-shell floor through the nested builder --
the degenerate-limit gate of the verification harness.
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
from warp_factory_py.metrics.warp_shell import metric_nested_warp_shells
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec


def nested_shell_profiles(R1_out: float, R2_out: float, R1_in: float,
                          R2_in: float, f_inner: float, M_nominal: float,
                          v: float):
    """Nested two-shell configuration -> windowed radial profiles.

    Same windowing / diagnostics contract as ``mmin_map.shell_profiles``:
    returns ``(r, Apos, B, F, M_adm, horizon_min)`` on ``[0.5, 1.5*R2_out]``.
    """
    from warp_factory_py.utils.constants import G, c
    centre = 1.75 * R2_out
    world_size = np.sqrt(3.0) * (centre - 1.0)
    r_sample_res = max(50_000, int(round(1.2 * world_size / DR_CANON)))
    _, p = metric_nested_warp_shells(
        (1, 1, 1, 1), (0.0, centre, centre, centre),
        shells=[(R1_in, R2_in, f_inner * M_nominal),
                (R1_out, R2_out, (1.0 - f_inner) * M_nominal)],
        warp_R1=R1_out, warp_R2=R2_out,
        smooth_factor=SF, v_warp=v, do_warp=True,
        grid_scale=(1.0, 1.0, 1.0, 1.0), r_sample_res=r_sample_res,
    )
    rf = p["r"]
    idx = np.where((rf >= 0.5) & (rf <= 1.5 * R2_out))[0]
    r = rf[idx]
    Apos = (-p["A"])[idx]
    B = p["B"][idx]
    F = p["shift"][idx]
    m_running = (r * c**2 / (2.0 * G)) * (1.0 - 1.0 / np.maximum(B, 1e-300))
    M_adm = float(np.interp(1.3 * R2_out, r, m_running))
    horizon_min = float(p.get(
        "horizon_min",
        (1.0 - 2.0 * G * m_running / (r * c**2 + 1e-30)).min(),
    ))
    return r, Apos, B, F, M_adm, horizon_min


def make_min_ec_nested(R1_in: float, R2_in: float, f_inner: float):
    """EC oracle for one (inner geometry, f_inner) -- injectable into find_mmin.

    Signature/return contract matches ``mmin_map.min_ec``: ``(min_ec,
    min_by_cond, M_adm, horizon_min)`` for ``(R1, R2, M_nominal, v, res)``
    where ``R1``/``R2`` are the OUTER shell geometry.
    """

    def min_ec_nested(R1: float, R2: float, M_nominal: float, v: float,
                      res=RES_FULL):
        n_r, n_th, na, nt = res
        r, Apos, B, F, M_adm, hmin = nested_shell_profiles(
            R1, R2, R1_in, R2_in, f_inner, M_nominal, v)
        if hmin < HORIZON_FLOOR:
            return float("nan"), {}, M_adm, hmin
        sub = np.arange(r.size)[:: max(1, r.size // n_r)]
        rs = r[sub]
        mask = (rs >= R1) & (rs <= R2)
        if f_inner > 0.0:
            mask |= (rs >= R1_in) & (rs <= R2_in)
        theta = np.linspace(0.02, np.pi - 0.02, n_th)
        out = evaluate_axisym_ec(
            rs, Apos[sub], B[sub], F[sub], v=v, theta=theta,
            in_shell_mask_1d=mask, num_angular=na, num_temporal=nt,
        )
        return out["min"], out["min_by_cond"], M_adm, hmin

    return min_ec_nested


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``cells x f_inner x inner_geometries`` (+ f=0 baselines).

    Config schema::

        {
          "rel_tol": 0.005,
          "cells": [{"R2": 20.0, "dfrac": 0.5, "v": 0.02}, ...],
          "f_inner": {"values": [0.02, 0.05, ...]},
          "inner_geometries": {"values": [[a_in, b_in], ...]},   # fractions of R2
          "include_f0_baseline": true
        }

    Geometry pairs with ``b_in * R2 >= R1_out`` (overlap) are skipped for
    that cell. f=0 baselines carry the FIRST valid geometry (irrelevant at
    zero inner mass; echoed for schema uniformity).
    """
    rel_tol = float(config.get("rel_tol", 0.005))
    fs = [float(x) for x in config["f_inner"]["values"]]
    geoms = [(float(a), float(b))
             for a, b in config["inner_geometries"]["values"]]
    grid: list[dict] = []
    for cell in config["cells"]:
        R2 = float(cell["R2"])
        dfrac = float(cell["dfrac"])
        v = float(cell["v"])
        R1 = R2 * (1.0 - dfrac)
        valid = [(a, b) for (a, b) in geoms
                 if 0.0 < a < b and b * R2 < R1]
        if config.get("include_f0_baseline", True) and valid:
            a0, b0 = valid[0]
            grid.append({
                "R1": R1, "R2": R2, "dfrac": dfrac, "v": v,
                "a_in": a0, "b_in": b0, "f_inner": 0.0, "rel_tol": rel_tol,
            })
        for (a, b) in valid:
            for f in fs:
                grid.append({
                    "R1": R1, "R2": R2, "dfrac": dfrac, "v": v,
                    "a_in": a, "b_in": b, "f_inner": f, "rel_tol": rel_tol,
                })
    return grid


def evaluate(point: dict) -> dict:
    """One (cell, geometry, f_inner) -> nested M_min record."""
    try:
        R1 = float(point["R1"])
        R2 = float(point["R2"])
        v = float(point["v"])
        a_in = float(point["a_in"])
        b_in = float(point["b_in"])
        f_inner = float(point["f_inner"])
        R1_in = a_in * R2
        R2_in = b_in * R2
        oracle = make_min_ec_nested(R1_in, R2_in, f_inner)
        rec = find_mmin(R1, R2, v,
                        rel_tol=float(point.get("rel_tol", 0.005)),
                        min_ec_fn=oracle)
        rec.update({
            "dfrac": float(point.get("dfrac", np.nan)),
            "a_in": a_in, "b_in": b_in,
            "R1_in": R1_in, "R2_in": R2_in, "f_inner": f_inner,
            "M_inner_at_min": (
                f_inner * rec["M_min_nominal"]
                if np.isfinite(rec.get("M_min_nominal", np.nan)) else np.nan
            ),
            "error": "",
        })
        return rec
    except Exception as exc:  # sweep must not die on one bad cell
        return {
            "R1": point.get("R1"), "R2": point.get("R2"),
            "v": point.get("v"), "dfrac": point.get("dfrac"),
            "a_in": point.get("a_in"), "b_in": point.get("b_in"),
            "f_inner": point.get("f_inner"),
            "error": f"{type(exc).__name__}: {exc}",
        }
