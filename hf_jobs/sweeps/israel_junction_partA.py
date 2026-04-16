"""Package 1 Part A parameter sweep.

Evaluates the Israel-junction surface stress-energy for a shift-perturbed
Alcubierre interior matched to a static Schwarzschild exterior, across a grid
of (M, R, v_s, sigma_w) (shell mass, radius, warp velocity, wall-inverse-
thickness). For each point, records whether the dominant energy condition
(DEC) is satisfied at every sampled polar angle, and the worst-case slack.

The scalar formulas are closed-form counterparts of the symbolic cells 2-7 of
``israel_junction.ipynb``. Keeping them duplicated (instead of imported from
the notebook) lets the sweep run on bare HF Jobs workers without nbconvert.

Geometrised units (G = c = 1); velocities v_s are dimensionless (v_s = v/c).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product


def _axis(spec: dict) -> list[float]:
    lo, hi, n = spec["lo"], spec["hi"], int(spec["n"])
    scale = spec.get("scale", "linear")
    if scale == "log":
        if lo <= 0 or hi <= 0:
            raise ValueError("log axis requires strictly positive bounds")
        return [float(x) for x in _logspace(lo, hi, n)]
    return [float(x) for x in _linspace(lo, hi, n)]


def _linspace(lo: float, hi: float, n: int) -> list[float]:
    if n == 1:
        return [lo]
    step = (hi - lo) / (n - 1)
    return [lo + i * step for i in range(n)]


def _logspace(lo: float, hi: float, n: int) -> list[float]:
    if n == 1:
        return [lo]
    log_lo, log_hi = math.log(lo), math.log(hi)
    step = (log_hi - log_lo) / (n - 1)
    return [math.exp(log_lo + i * step) for i in range(n)]


def build_grid(config: dict) -> list[dict]:
    axes = config["axes"]
    Ms = _axis(axes["M"])
    Rs = _axis(axes["R"])
    vs_s = _axis(axes["v_s"])
    sigs = _axis(axes["sigma_w"])

    grid = []
    for M_val, R_val, vs_val, sw_val in product(Ms, Rs, vs_s, sigs):
        if 2 * M_val >= R_val:
            continue
        grid.append({
            "M": M_val,
            "R": R_val,
            "v_s": vs_val,
            "sigma_w": sw_val,
            "n_theta": int(config.get("n_theta", 33)),
        })
    return grid


@dataclass(frozen=True)
class _Point:
    sigma: float
    q: float
    Ptheta: float
    Pphi: float


def _surface_tensor(theta: float, M: float, R: float, v_s: float, sigma_w: float) -> _Point:
    """Closed-form S^a_b components at polar angle theta.

    Derived from cells 5-6 of israel_junction.ipynb after simplification in
    the thin-wall, weak-field limit consistent to O(v_s^2) and O(GM/R)^2.
    """
    fR = 1.0 - 2.0 * M / R
    sqrt_fR = math.sqrt(max(fR, 1e-300))

    # l=0 (Schwarzschild) surface density and pressure (Poisson 2004 Ch.3):
    sigma_0 = (1.0 - sqrt_fR) / (4.0 * math.pi * R)
    P_0 = (1.0 - sqrt_fR) ** 2 / (8.0 * math.pi * R * sqrt_fR) if sqrt_fR > 0 else math.inf

    # l=1 dipole pieces induced by the shift (cells 3, 5):
    #   - radial-shift sourced dipole on sigma: scales as (v_s sigma_w / R) cos(theta)
    #   - tangential-shift-sourced momentum flux q: scales as (v_s / R) sin(theta)
    # The coefficients below are the analytic result of the symbolic simplification
    # to leading order in v_s.
    c_sigma1 = -v_s * sigma_w / (16.0 * math.pi * R)
    c_q1     =  v_s / (8.0 * math.pi * R * R)
    c_P1     =  v_s * sigma_w / (32.0 * math.pi * R)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    sigma = sigma_0 + c_sigma1 * cos_t
    q     = c_q1 * sin_t
    Pt    = P_0 + c_P1 * cos_t
    Pp    = P_0 + c_P1 * cos_t

    return _Point(sigma=sigma, q=q, Ptheta=Pt, Pphi=Pp)


def evaluate(point: dict) -> dict:
    M = float(point["M"])
    R = float(point["R"])
    v_s = float(point["v_s"])
    sigma_w = float(point["sigma_w"])
    n_theta = int(point.get("n_theta", 33))

    thetas = [math.pi * (i + 0.5) / n_theta for i in range(n_theta)]

    worst_dec_slack = math.inf
    worst_theta = 0.0
    nec_ok = wec_ok = dec_ok = sec_ok = True

    for th in thetas:
        s = _surface_tensor(th, M, R, v_s, sigma_w)

        if s.sigma < 0:
            wec_ok = False
        if s.sigma + s.Ptheta < 0 or s.sigma + s.Pphi < 0:
            nec_ok = False
        if s.sigma + s.Ptheta + s.Pphi < 0:
            sec_ok = False

        dec_slack = s.sigma - max(abs(s.q), abs(s.Ptheta), abs(s.Pphi))
        if s.sigma < 0 or dec_slack < 0:
            dec_ok = False
        if dec_slack < worst_dec_slack:
            worst_dec_slack = dec_slack
            worst_theta = th

    return {
        "M": M,
        "R": R,
        "v_s": v_s,
        "sigma_w": sigma_w,
        "compactness": 2 * M / R,
        "WEC": bool(wec_ok),
        "NEC": bool(nec_ok),
        "DEC": bool(dec_ok),
        "SEC": bool(sec_ok),
        "worst_dec_slack": float(worst_dec_slack),
        "worst_theta": float(worst_theta),
    }
