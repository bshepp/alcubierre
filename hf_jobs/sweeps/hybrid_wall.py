"""Slice 2 (Phase 2C) sweep: Krasnikov wall with Fuchs-style matter perturbation.

Modifies the bare Krasnikov k(rho) profile by adding a localised bump representing
the matter-shell density:

    k(rho) = 1 - eta * theta_eps(rho_max - rho) + delta_M * B_{w_M}(rho - rho_max)

Computes the resulting Eulerian-frame T_{hat mu hat nu} and reports WEC/DEC pass
fractions across the wall band.

Question: does any (eta, eps, rho_max, delta_M, w_M) point achieve full WEC?
Expected outcome (per scratch validation): no, the matter perturbation introduces
its own curvature that does not surgically cancel the geometric negative spike.
"""

from __future__ import annotations

import math
from itertools import product
from typing import Any

import numpy as np
import sympy as sp


def _build_lambdas():
    t, x, rho, phi = sp.symbols('t x rho phi', real=True)
    eta_s = sp.Symbol('eta', positive=True)
    eps = sp.Symbol('epsilon', positive=True)
    rho_max = sp.Symbol('rho_m', positive=True)
    delta_M = sp.Symbol('delta_M', real=True)
    w_M = sp.Symbol('w_M', positive=True)

    theta_eps = sp.Rational(1, 2) * (sp.tanh(2 * (2 * (rho_max - rho) / eps - 1)) + 1)
    B_w = sp.Rational(1, 2) * (sp.tanh((w_M - (rho - rho_max)) / w_M) - sp.tanh((-w_M - (rho - rho_max)) / w_M))
    k = 1 - eta_s * theta_eps + delta_M * B_w

    g = sp.Matrix([
        [-1,                            sp.Rational(1, 2) * (1 - k), 0, 0],
        [sp.Rational(1, 2) * (1 - k),   k,                            0, 0],
        [0,                              0,                            1, 0],
        [0,                              0,                            0, rho**2],
    ])
    coords = (t, x, rho, phi)

    a_blk = -1
    b_blk = sp.Rational(1, 2) * (1 - k)
    c_blk = k
    det_blk = a_blk * c_blk - b_blk**2
    g_inv = sp.Matrix([
        [c_blk / det_blk,   -b_blk / det_blk,  0,        0],
        [-b_blk / det_blk,  a_blk / det_blk,   0,        0],
        [0,                  0,                 1,        0],
        [0,                  0,                 0,        1/rho**2],
    ])

    N = 4
    Gamma = [[[sp.S.Zero for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                s = sp.S.Zero
                for d in range(N):
                    s += g_inv[a, d] * (
                        sp.diff(g[d, b], coords[c])
                        + sp.diff(g[d, c], coords[b])
                        - sp.diff(g[b, c], coords[d])
                    )
                Gamma[a][b][c] = s / 2

    Ricci = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            s = sp.S.Zero
            for c in range(N):
                s += sp.diff(Gamma[c][a][b], coords[c]) - sp.diff(Gamma[c][a][c], coords[b])
                for d in range(N):
                    s += Gamma[c][c][d] * Gamma[d][a][b] - Gamma[c][b][d] * Gamma[d][a][c]
            Ricci[a, b] = s

    R_scalar = sum(g_inv[a, b] * Ricci[a, b] for a in range(N) for b in range(N))
    G_t = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            G_t[a, b] = Ricci[a, b] - sp.Rational(1, 2) * g[a, b] * R_scalar
    T = G_t / (8 * sp.pi)

    tetrad = sp.Matrix([
        [1, 0, 0, 0],
        [(1 - k) / (1 + k), 2 / (1 + k), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1 / rho],
    ])
    T_o = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            s = sp.S.Zero
            for a in range(4):
                for b in range(4):
                    s += tetrad[mu, a] * tetrad[nu, b] * T[a, b]
            T_o[mu, nu] = s

    args = (rho, eta_s, eps, rho_max, delta_M, w_M)
    return {
        "Ttt": sp.lambdify(args, T_o[0, 0], 'numpy'),
        "Ttx": sp.lambdify(args, T_o[0, 1], 'numpy'),
        "Txx": sp.lambdify(args, T_o[1, 1], 'numpy'),
        "Trr": sp.lambdify(args, T_o[2, 2], 'numpy'),
        "Tpp": sp.lambdify(args, T_o[3, 3], 'numpy'),
    }


print("Building hybrid_wall pipeline (one-time, ~5s)...")
_LAMBDAS = _build_lambdas()
print("hybrid_wall pipeline ready.")


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
    for eta_v, eps_v, n_v, dM_v, w_v in product(
        _axis(axes["eta"]),
        _axis(axes["eps"]),
        _axis(axes["n"]),
        _axis(axes["delta_M"]),
        _axis(axes["w_M"]),
    ):
        if eta_v >= 2.0 or n_v < 2.0:
            continue
        grid.append({
            "eta":     float(eta_v),
            "eps":     float(eps_v),
            "n":       float(n_v),
            "rho_max": float(eps_v * n_v),
            "delta_M": float(dM_v),
            "w_M":     float(w_v),
            "n_rho":   int(config.get("n_rho", 2001)),
            "margin":  float(config.get("margin", 4.0)),
        })
    return grid


def evaluate(point: dict) -> dict:
    eta = float(point["eta"]); eps = float(point["eps"])
    rho_max = float(point["rho_max"])
    dM = float(point["delta_M"]); w = float(point["w_M"])
    n_rho = int(point["n_rho"]); margin = float(point["margin"])

    rs = np.linspace(rho_max - margin * eps, rho_max + margin * eps, n_rho)
    try:
        Ttt = _LAMBDAS["Ttt"](rs, eta, eps, rho_max, dM, w)
        Ttx = _LAMBDAS["Ttx"](rs, eta, eps, rho_max, dM, w)
        Txx = _LAMBDAS["Txx"](rs, eta, eps, rho_max, dM, w)
        Trr = _LAMBDAS["Trr"](rs, eta, eps, rho_max, dM, w)
        Tpp = _LAMBDAS["Tpp"](rs, eta, eps, rho_max, dM, w)
    except Exception as exc:
        return {**point, "error": f"{type(exc).__name__}: {exc}",
                "wec_fraction": float('nan'), "dec_fraction": float('nan'),
                "rho_p_min": float('nan'), "dec_slack_min": float('nan')}

    rho_p = -Ttt
    flux = np.abs(Ttx)
    pmax = np.maximum.reduce([np.abs(Txx), np.abs(Trr), np.abs(Tpp)])
    slack = rho_p - np.maximum(flux, pmax)
    finite = np.isfinite(rho_p) & np.isfinite(slack)
    if not finite.any():
        return {**point, "error": "all-nan",
                "wec_fraction": float('nan'), "dec_fraction": float('nan'),
                "rho_p_min": float('nan'), "dec_slack_min": float('nan')}

    return {
        **point,
        "rho_p_min": float(np.nanmin(rho_p)),
        "rho_p_max": float(np.nanmax(rho_p)),
        "dec_slack_min": float(np.nanmin(slack)),
        "dec_slack_max": float(np.nanmax(slack)),
        "wec_fraction": float(np.mean((rho_p > 0) & finite)),
        "dec_fraction": float(np.mean((rho_p > 0) & (slack > 0) & finite)),
    }
