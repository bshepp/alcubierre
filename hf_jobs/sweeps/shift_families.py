"""Slice 1 (Phase 2C) parameter sweep: alternate axisymmetric shift families.

For each of four families (Alcubierre, Natario, irrotational/Rodal, free-form
single-Bessel-mode), evaluates the Eulerian-frame stress-energy on a (r, theta)
grid and reports WEC and DEC pass fractions across a sweep over the family's
parameters.

The four families share a single ADM-pipeline build path (axisymmetric shift in
spherical coords with unit lapse and flat spatial slices); only the choice of
beta^{hat r}(r, theta) and beta^{hat theta}(r, theta) differs.

Implementation: builds the symbolic Einstein tensor + Eulerian-frame transform
once per family at module import time (slow, ~1 minute total), then lambdifies
to NumPy. Sweep evaluation is fast (<1s per point).
"""

from __future__ import annotations

import math
from itertools import product
from typing import Any

import numpy as np
import sympy as sp


# ---------------------------------------------------------------------------
# Symbolic pipeline (built once per family at module load)
# ---------------------------------------------------------------------------

def _build_eulerian_T(br_hat_expr, bt_hat_expr):
    """Return T_{hat mu hat nu} as a sympy 4x4 Matrix in the Eulerian tetrad.

    Uses the closed-form ADM-metric inverse to avoid SymPy's slow symbolic
    matrix inversion, which is otherwise the bottleneck for tanh-heavy shift
    expressions (Natario, irrotational).
    """
    t, r, theta, phi = sp.symbols('t r theta phi', real=True, positive=True)

    br_coord = br_hat_expr
    bt_coord = bt_hat_expr / r

    br_low = br_coord
    bt_low = (r**2) * bt_coord

    beta_sq = br_coord * br_low + bt_coord * bt_low

    g = sp.Matrix([
        [-1 + beta_sq,    br_low,    bt_low,    0],
        [br_low,          1,         0,         0],
        [bt_low,          0,         r**2,      0],
        [0,               0,         0,         r**2 * sp.sin(theta)**2],
    ])
    coords = (t, r, theta, phi)
    # Closed-form ADM inverse (alpha = 1, gamma = diag(1, r^2, r^2 sin^2 theta)):
    #   g^{tt} = -1
    #   g^{ti} = beta^i
    #   g^{ij} = gamma^{ij} - beta^i beta^j
    bphi_coord = sp.S.Zero
    g_inv = sp.Matrix([
        [-1,                         br_coord,                       bt_coord,                    bphi_coord],
        [br_coord,                   1 - br_coord * br_coord,        -br_coord * bt_coord,        -br_coord * bphi_coord],
        [bt_coord,                   -bt_coord * br_coord,           1/r**2 - bt_coord * bt_coord, -bt_coord * bphi_coord],
        [bphi_coord,                 -bphi_coord * br_coord,         -bphi_coord * bt_coord,      1/(r**2 * sp.sin(theta)**2) - bphi_coord * bphi_coord],
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
                s += sp.diff(Gamma[c][a][b], coords[c])
                s -= sp.diff(Gamma[c][a][c], coords[b])
                for d in range(N):
                    s += Gamma[c][c][d] * Gamma[d][a][b]
                    s -= Gamma[c][b][d] * Gamma[d][a][c]
            Ricci[a, b] = s

    R_scalar = sum(g_inv[a, b] * Ricci[a, b] for a in range(N) for b in range(N))
    G_t = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            G_t[a, b] = Ricci[a, b] - sp.Rational(1, 2) * g[a, b] * R_scalar
    T = G_t / (8 * sp.pi)

    tetrad = sp.Matrix([
        [1,                 0, 0,         0],
        [-br_coord,         1, 0,         0],
        [-bt_coord,         0, 1/r,       0],
        [0,                 0, 0,         1/(r * sp.sin(theta))],
    ])

    T_o = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            s = sp.S.Zero
            for a in range(4):
                for b in range(4):
                    s += tetrad[mu, a] * tetrad[nu, b] * T[a, b]
            T_o[mu, nu] = s
    return T_o, (t, r, theta, phi)


def _build_family_lambdas(family_name: str):
    """Return dict of NumPy-lambdified Eulerian-frame components for the family."""
    t, r, theta, phi = sp.symbols('t r theta phi', real=True, positive=True)
    v = sp.Symbol('v', real=True)
    R0 = sp.Symbol('R0', positive=True)
    sig = sp.Symbol('sigma', positive=True)
    A1 = sp.Symbol('A1', real=True)
    k = sp.Symbol('k', positive=True)

    f_alc = (sp.tanh(sig * (r + R0)) - sp.tanh(sig * (r - R0))) / (2 * sp.tanh(sig * R0))
    f_nat = 1 - f_alc

    if family_name == "alcubierre":
        br = v * f_alc * sp.cos(theta)
        bt = -v * f_alc * sp.sin(theta)
        params = (v, R0, sig)
    elif family_name == "natario":
        f_nat_prime = sp.diff(f_nat, r)
        br = -v * f_nat * sp.cos(theta)
        bt = v * (f_nat + (r / 2) * f_nat_prime) * sp.sin(theta)
        params = (v, R0, sig)
    elif family_name == "irrotational":
        g_irr = (1 / r) * sp.integrate(f_nat, r)
        br = -v * f_nat * sp.cos(theta)
        bt = v * g_irr * sp.sin(theta)
        params = (v, R0, sig)
    elif family_name == "freeform_j1":
        j1 = lambda x: sp.sin(x) / x**2 - sp.cos(x) / x
        br = v * A1 * j1(k * r) * sp.cos(theta)
        bt = -v * A1 * j1(k * r) * sp.sin(theta)
        params = (v, A1, k)
    else:
        raise ValueError(f"Unknown family: {family_name}")

    T_o, coords = _build_eulerian_T(br, bt)

    args = (r, theta) + params
    return {
        "Ttt": sp.lambdify(args, T_o[0, 0], 'numpy'),
        "Ttr": sp.lambdify(args, T_o[0, 1], 'numpy'),
        "Ttth": sp.lambdify(args, T_o[0, 2], 'numpy'),
        "Trr": sp.lambdify(args, T_o[1, 1], 'numpy'),
        "Tthth": sp.lambdify(args, T_o[2, 2], 'numpy'),
        "Tphph": sp.lambdify(args, T_o[3, 3], 'numpy'),
        "param_names": [p.name for p in params],
    }


print("Building shift_families pipelines (slow, ~1 minute)...")
_LAMBDAS = {}
for _name in ("alcubierre", "natario", "irrotational", "freeform_j1"):
    _LAMBDAS[_name] = _build_family_lambdas(_name)
    print(f"  {_name} ready")
print("All four shift_families pipelines built.")


# ---------------------------------------------------------------------------
# Sweep harness
# ---------------------------------------------------------------------------

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
    """Each family has its own axes block in the config."""
    grid = []
    for family_name, family_axes in config["families"].items():
        if family_name == "freeform_j1":
            for vv, A1, kk in product(
                _axis(family_axes["v"]),
                _axis(family_axes["A1"]),
                _axis(family_axes["k"]),
            ):
                grid.append({
                    "family": family_name,
                    "v": float(vv),
                    "A1": float(A1),
                    "k": float(kk),
                    "n_r": int(config.get("n_r", 80)),
                    "n_theta": int(config.get("n_theta", 60)),
                    "r_hi_factor": float(config.get("r_hi_factor", 3.0)),
                    "R0_for_grid": float(config.get("R0_for_grid", 5.0)),
                })
        else:
            for vv, R0v, sigv in product(
                _axis(family_axes["v"]),
                _axis(family_axes["R0"]),
                _axis(family_axes["sigma"]),
            ):
                grid.append({
                    "family": family_name,
                    "v": float(vv),
                    "R0": float(R0v),
                    "sigma": float(sigv),
                    "n_r": int(config.get("n_r", 80)),
                    "n_theta": int(config.get("n_theta", 60)),
                    "r_hi_factor": float(config.get("r_hi_factor", 3.0)),
                })
    return grid


def evaluate(point: dict) -> dict:
    name = point["family"]
    pkg = _LAMBDAS[name]
    n_r = int(point["n_r"])
    n_th = int(point["n_theta"])
    r_hi_factor = float(point["r_hi_factor"])

    if name == "freeform_j1":
        v = float(point["v"]); A1 = float(point["A1"]); k = float(point["k"])
        R0 = float(point.get("R0_for_grid", 5.0))
        family_args = (v, A1, k)
    else:
        v = float(point["v"]); R0 = float(point["R0"]); sigma = float(point["sigma"])
        family_args = (v, R0, sigma)

    rs = np.linspace(0.1, r_hi_factor * R0, n_r)
    ths = np.linspace(0.05, math.pi - 0.05, n_th)
    R_grid, Th_grid = np.meshgrid(rs, ths, indexing='ij')

    args = (R_grid, Th_grid) + family_args
    try:
        Ttt = pkg["Ttt"](*args)
        Ttr = pkg["Ttr"](*args)
        Ttth = pkg["Ttth"](*args)
        Trr = pkg["Trr"](*args)
        Tthth = pkg["Tthth"](*args)
        Tphph = pkg["Tphph"](*args)
    except Exception as exc:
        return {
            **point,
            "wec_fraction": float('nan'),
            "dec_fraction": float('nan'),
            "rho_p_min": float('nan'),
            "rho_p_max": float('nan'),
            "dec_slack_min": float('nan'),
            "error": f"{type(exc).__name__}: {exc}",
        }

    rho_p = -Ttt
    flux = np.maximum(np.abs(Ttr), np.abs(Ttth))
    p_max = np.maximum.reduce([np.abs(Trr), np.abs(Tthth), np.abs(Tphph)])
    dec_slack = rho_p - np.maximum(flux, p_max)

    finite = np.isfinite(rho_p) & np.isfinite(dec_slack)
    if not finite.any():
        return {
            **point,
            "wec_fraction": float('nan'),
            "dec_fraction": float('nan'),
            "rho_p_min": float('nan'),
            "rho_p_max": float('nan'),
            "dec_slack_min": float('nan'),
            "error": "all-nan grid",
        }

    wec_mask = (rho_p > 0) & finite
    dec_mask = wec_mask & (dec_slack > 0)
    return {
        **point,
        "wec_fraction": float(wec_mask.mean()),
        "dec_fraction": float(dec_mask.mean()),
        "rho_p_min": float(np.nanmin(rho_p)),
        "rho_p_max": float(np.nanmax(rho_p)),
        "dec_slack_min": float(np.nanmin(dec_slack)),
        "dec_slack_max": float(np.nanmax(dec_slack)),
    }
