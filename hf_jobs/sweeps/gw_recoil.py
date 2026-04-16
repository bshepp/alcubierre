"""GW-recoil ceiling sweep for Fuchs-class warp shells (Package 3, Task 2A.10).

Approach B (PN shell-analog) combined with the Approach A rescaling gives a
conservative ceiling on the recoil delta-v achievable by a Fuchs-class shell
purely from gravitational-wave emission.  This module evaluates that ceiling
over a grid of (beta, C, tau_orbits) points.

Returns one row per grid point with columns

    beta              dimensionless warp speed
    C                 Schwarzschild compactness 2GM/(R c^2)
    M_kg              shell mass used for this point
    R_m               shell radius used for this point
    n_orbits          number of PN-analog orbits integrated
    dv_pn             delta-v from Approach B PN analog   (m/s)
    dv_sxs_rescale    delta-v from Approach A SXS rescaling (m/s)
    dv_kick           max(dv_pn, dv_sxs_rescale)          (m/s)
    log10_dv_kick     log10(dv_kick) for easy plotting
"""
from __future__ import annotations

import itertools
from typing import Any, Iterable

import numpy as np

G_SI = 6.67430e-11
c_SI = 2.99792458e8
V_KICK_BBH_RECORD = 5.0e6  # m/s, Varma et al. 2022


def build_grid(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand a JSON config into an explicit list of parameter points."""
    betas    = np.asarray(config.get("betas",    [0.001, 0.01, 0.1, 0.5]))
    Cs       = np.asarray(config.get("Cs",       [0.01,  0.1,  0.5]))
    Ms       = np.asarray(config.get("Ms_kg",    [1e24, 1e27, 1e30]))
    n_orbits = np.asarray(config.get("n_orbits", [1, 1e4, 1e8]))

    points: list[dict[str, Any]] = []
    for beta, C, M, n_orb in itertools.product(betas, Cs, Ms, n_orbits):
        # R from compactness:  C = 2GM / (R c^2)  =>  R = 2GM / (C c^2)
        R = 2 * G_SI * M / (C * c_SI**2)
        points.append({
            "beta": float(beta),
            "C":    float(C),
            "M_kg": float(M),
            "R_m":  float(R),
            "n_orbits": float(n_orb),
        })
    return points


def _pn_delta_v(point: dict[str, Any]) -> float:
    """Approach B: PN quadrupole-analog recoil for a shell + small beacon binary.

    Uses Fitchett 1983 / Blanchet 2014 leading PN momentum-flux formula with a
    beacon of 1% of shell mass at separation a = 2R.  Accumulates |dP/dt| * T_orb
    over n_orbits; divides by M to get delta-v ceiling.
    """
    M1 = point["M_kg"]
    M2 = 0.01 * M1
    R  = point["R_m"]
    a  = 2.0 * R
    n_orb = point["n_orbits"]

    if M1 == M2 or a <= 0 or M1 <= 0:
        return 0.0

    omega = np.sqrt(G_SI * (M1 + M2) / a**3)
    T_orb = 2.0 * np.pi / omega
    num = 8.0 * G_SI**4 * (M1 * M2)**2 * abs(M1 - M2)
    den = 105.0 * c_SI**7 * a**5
    dPdt = num / den
    dP_total = dPdt * T_orb * n_orb
    return dP_total / M1


def _sxs_rescale_delta_v(point: dict[str, Any]) -> float:
    """Approach A: rescale Varma 2022 BBH record to Fuchs-shell parameters.

    v_kick = v_kick_BBH * beta^2 * C^(3/2)
    """
    beta = point["beta"]
    C    = point["C"]
    return V_KICK_BBH_RECORD * beta**2 * C**1.5


def evaluate(point: dict[str, Any]) -> dict[str, Any]:
    dv_pn   = _pn_delta_v(point)
    dv_sxs  = _sxs_rescale_delta_v(point)
    dv_kick = max(dv_pn, dv_sxs)
    # log10 safely (kick=0 -> -inf -> clip to something finite for plotting).
    log10_dv = float(np.log10(dv_kick)) if dv_kick > 0 else -300.0
    return {
        **point,
        "dv_pn":          float(dv_pn),
        "dv_sxs_rescale": float(dv_sxs),
        "dv_kick":        float(dv_kick),
        "log10_dv_kick":  log10_dv,
    }


def run(points: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate(p) for p in points]
