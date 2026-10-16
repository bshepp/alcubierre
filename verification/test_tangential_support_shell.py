"""Session 58 side quest (Le 2026c) -- tangential-support Fuchs shell: does
replacing the isotropic TOV pressure by Le's p_r = 0 class move the certified
minimal mass?

Background. Le 2026c proves an isotropic-pressure static shell cannot have a
free inner face (TOV forces p' <= 0, so p(R2) = 0 => p == 0), and exhibits
DEC-respecting shells supported by TANGENTIAL stress alone (p_r = 0, two
free faces). The project's Fuchs-class builder uses isotropic TOV pressure
cut to zero inside R1 and smoothed. With ``pressure_mode="zero_radial"`` the
lapse is solved with p_r = 0 and the Einstein tensor then demands whatever
tangential stress the geometry needs; the exact EC oracle judges it.

Modes:
  compare  -- at the canonical cell (10, 20, 0.02c): exact EC minima for the
              two support classes at the isotropic floor mass and at the
              canonical mass; the required principal pressures at the
              worst point; Type-I fraction.  (~4 RES_FULL evaluations)
  floor    -- bisect the p_r = 0 floor with the exact oracle (find_mmin
              with a zero_radial min_ec); report shift vs the exact
              isotropic floor 2.5754e27.  (~10 evaluations)

Slice: constant-density rho on [R1, R2]; canonical smoothing; l=1 dipole
shift at the wall; radial representation; exact (observer-robust) EC minima
over the in-shell mask. This is a REQUIRED-STRESS comparison: neither class
is a material model.

Run with repo root on PYTHONPATH.
"""
from __future__ import annotations

import json
import sys
import time
from functools import partial

import numpy as np

from hf_jobs.sweeps.mmin_map import (
    RES_FULL, SF, DR_CANON, HORIZON_FLOOR, find_mmin, min_ec as min_ec_tov)
from warp_factory_py.metrics.warp_shell import metric_profile_warp_shell, _compact_sigmoid
from warp_factory_py.solvers.axisymmetric_ec import evaluate_axisym_ec
from warp_factory_py.utils.constants import G, c


def shell_profiles_mode(R1, R2, M_nominal, v, pressure_mode):
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
        pressure_mode=pressure_mode,
    )
    rf = p["r"]
    idx = np.where((rf >= 0.5) & (rf <= 1.5 * R2))[0]
    r = rf[idx]
    Apos = (-p["A"])[idx]; B = p["B"][idx]; F = p["shift"][idx]
    m_running = (r * c**2 / (2.0 * G)) * (1.0 - 1.0 / np.maximum(B, 1e-300))
    M_adm = float(np.interp(1.3 * R2, r, m_running))
    hmin = float(p.get("horizon_min", (1.0 - 2.0 * G * m_running / (r * c**2 + 1e-30)).min()))
    return r, Apos, B, F, M_adm, hmin


def min_ec_mode(R1, R2, M_nominal, v, res=RES_FULL, pressure_mode="zero_radial", want_T=False):
    n_r, n_th, na, nt = res
    r, Apos, B, F, M_adm, hmin = shell_profiles_mode(R1, R2, M_nominal, v, pressure_mode)
    if hmin < HORIZON_FLOOR:
        return float("nan"), {}, M_adm, hmin
    sub = np.arange(r.size)[:: max(1, r.size // n_r)]
    theta = np.linspace(0.02, np.pi - 0.02, n_th)
    mask = (r[sub] >= R1) & (r[sub] <= R2)
    out = evaluate_axisym_ec(r[sub], Apos[sub], B[sub], F[sub], v=v, theta=theta,
                             in_shell_mask_1d=mask, num_angular=na, num_temporal=nt, exact=True)
    if want_T:
        return out, r[sub], theta, mask
    return out["min"], out["min_by_cond"], M_adm, hmin


def principal_pressures_at_worst(out, rs, theta, mask):
    T = out["T_eul"]
    arr = np.where(mask[:, None], out["null"], np.inf)
    i, j = np.unravel_index(np.argmin(arr), arr.shape)
    Tp = T[:, :, i, j]
    eta = np.diag([-1.0, 1, 1, 1])
    w, v = np.linalg.eig(eta @ Tp)
    vn = np.einsum("ai,ab,bi->i", v.real, eta, v.real)
    it = int(np.argmin(vn))
    rho = -w.real[it]; p = np.delete(w.real, it)
    return dict(r=float(rs[i]), theta=float(theta[j]), rho=float(rho), p=[float(x) for x in np.sort(p)],
                typeI_frac=float(out["type_I"][mask[:, None] & np.ones_like(out["type_I"], bool)].mean()))


def mode_compare():
    R1, R2, v = 10.0, 20.0, 0.02
    recs = []
    for M, lab in ((2.5754e27, "exact isotropic floor"), (4.49e27, "canonical vessel")):
        for pm in ("tov", "zero_radial"):
            t0 = time.time()
            out, rs, th, mask = min_ec_mode(R1, R2, M, v, pressure_mode=pm, want_T=True)
            scale = float(np.abs(out["T_eul"][0, 0][mask[:, None] & np.ones(out["T_eul"].shape[2:], bool)]).max())
            pp = principal_pressures_at_worst(out, rs, th, mask)
            rec = dict(label=lab, M=M, pressure_mode=pm, min_ec=out["min"],
                       min_by_cond={k: float(x) for k, x in out["min_by_cond"].items()},
                       min_rel=out["min"] / scale, worst_point=pp, secs=round(time.time() - t0, 1))
            recs.append(rec); print(json.dumps(rec, indent=1), flush=True)
    print("\nSUMMARY (exact EC min / scale):")
    for r_ in recs:
        print(f"  {r_['label']:>22s} {r_['pressure_mode']:>12s}: min={r_['min_ec']:+.3e} ({r_['min_rel']:+.2e} of scale), worst at r={r_['worst_point']['r']:.2f} th={r_['worst_point']['theta']:.2f}; rho/p = {r_['worst_point']['rho']:.3e} / {[f'{x:.2e}' for x in r_['worst_point']['p']]}")
    return recs


def mode_floor():
    t0 = time.time()
    res = find_mmin(10.0, 20.0, 0.02, rel_tol=0.005, min_ec_fn=partial(min_ec_mode, pressure_mode="zero_radial"))
    ref = 2.5754e27
    out = {k: (float(x) if isinstance(x, (int, float, np.floating)) else str(x)) for k, x in res.items() if not isinstance(x, (dict, np.ndarray))}
    out["secs"] = round(time.time() - t0, 1)
    if out.get("M_min_nominal") == out.get("M_min_nominal"):
        out["shift_vs_exact_isotropic_floor"] = out["M_min_nominal"] / ref - 1.0
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "compare"
    (mode_floor if mode == "floor" else mode_compare)()
