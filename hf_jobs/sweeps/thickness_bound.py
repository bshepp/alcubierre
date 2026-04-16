"""Package 2 parameter sweep: minimum shell thickness for DEC on a shift-perturbed shell.

For a grid of (M, R, beta, Delta/R), this sweep asks: does a Part-A-style
thin-shell junction, thickened to radial extent Delta via a uniform spreading
of the surface tensor, satisfy DEC at every polar angle?

We use a simple but physically motivated "thick-shell DEC" proxy:

    sigma_3D(theta) = sigma_thin(theta) / Delta               (energy density)
    T^ij_3D(theta)  = P_thin(theta) / Delta                    (spatial stress)
    T^0i_3D(theta)  = q_thin(theta) * (beta / Delta)           (momentum density,
                                                                 gets an extra
                                                                 beta factor from
                                                                 the shift itself)

The critical inequality is sigma_3D >= |T^ij_3D| AND sigma_3D >= |T^0i_3D|,
which reproduces the analytical cell-3 derivation. Running this sweep gives
a numerical measurement of the coefficient kappa in Delta_min/R = kappa beta/C.
"""

from __future__ import annotations

import math
from itertools import product


def _axis(spec: dict) -> list[float]:
    lo, hi, n = spec["lo"], spec["hi"], int(spec["n"])
    scale = spec.get("scale", "linear")
    if scale == "log":
        if lo <= 0 or hi <= 0:
            raise ValueError("log axis needs positive bounds")
        log_lo, log_hi = math.log(lo), math.log(hi)
        if n == 1:
            return [lo]
        step = (log_hi - log_lo) / (n - 1)
        return [math.exp(log_lo + i * step) for i in range(n)]
    if n == 1:
        return [lo]
    step = (hi - lo) / (n - 1)
    return [lo + i * step for i in range(n)]


def build_grid(config: dict) -> list[dict]:
    axes = config["axes"]
    grid = []
    for M, R, beta, DoR in product(
        _axis(axes["M"]),
        _axis(axes["R"]),
        _axis(axes["beta"]),
        _axis(axes["Delta_over_R"]),
    ):
        if 2 * M >= R:
            continue
        grid.append({
            "M": M,
            "R": R,
            "beta": beta,
            "Delta_over_R": DoR,
            "n_theta": int(config.get("n_theta", 33)),
        })
    return grid


def _volumetric_shell(theta: float, M: float, R: float, beta: float, Delta: float):
    """Return (rho, T^0r, T^rr, T^thth, T^phph) volumetric densities."""
    fR = 1.0 - 2.0 * M / R
    sqrt_fR = math.sqrt(max(fR, 1e-300))

    sigma_0 = (1.0 - sqrt_fR) / (4.0 * math.pi * R)
    P_0 = (1.0 - sqrt_fR) ** 2 / (8.0 * math.pi * R * sqrt_fR) if sqrt_fR > 0 else math.inf

    sigma_w = 1.0 / Delta
    c_sigma1 = -beta * sigma_w / (16.0 * math.pi * R)
    c_q1     =  beta / (8.0 * math.pi * R * R)
    c_P1     =  beta * sigma_w / (32.0 * math.pi * R)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    sigma_thin = sigma_0 + c_sigma1 * cos_t
    q_thin     = c_q1 * sin_t
    P_thin     = P_0 + c_P1 * cos_t

    rho  = sigma_thin / Delta
    T_0r = q_thin * beta / Delta
    T_rr = P_thin / Delta
    T_th = P_thin / Delta
    T_ph = P_thin / Delta
    return rho, T_0r, T_rr, T_th, T_ph


def evaluate(point: dict) -> dict:
    M = float(point["M"])
    R = float(point["R"])
    beta = float(point["beta"])
    DoR = float(point["Delta_over_R"])
    Delta = DoR * R
    n_theta = int(point.get("n_theta", 33))

    thetas = [math.pi * (i + 0.5) / n_theta for i in range(n_theta)]
    worst_slack = math.inf
    worst_theta = 0.0
    dec_ok = True
    for th in thetas:
        rho, T0r, Trr, Tth, Tph = _volumetric_shell(th, M, R, beta, Delta)
        slack = rho - max(abs(T0r), abs(Trr), abs(Tth), abs(Tph))
        if rho < 0 or slack < 0:
            dec_ok = False
        if slack < worst_slack:
            worst_slack = slack
            worst_theta = th

    C = 2.0 * M / R
    Delta_min_predicted = 0.75 * beta / C * R if C > 0 else math.inf

    return {
        "M": M,
        "R": R,
        "beta": beta,
        "Delta_over_R": DoR,
        "Delta": Delta,
        "compactness": C,
        "DEC": bool(dec_ok),
        "worst_slack": float(worst_slack),
        "worst_theta": float(worst_theta),
        "Delta_min_predicted": Delta_min_predicted,
        "Delta_min_predicted_over_R": Delta_min_predicted / R,
        "predicted_ok": Delta >= Delta_min_predicted,
    }
