"""Task 2A.13 parameter sweep: Krasnikov tube wall stress-energy and DEC.

For a grid of (eta, eps, rho_max), this sweep computes the Krasnikov-tube
orthonormal-frame stress-energy across the wall and asks: does any positive
classical matter EoS satisfy WEC AND DEC anywhere in the wall?

Expected outcome: NO point in the (eta, eps, rho_max) parameter space allows
WEC.  This is the Path 2A no-go for static-infrastructure Krasnikov tubes.

The wall metric is

    ds^2 = -dt^2 + (1 - k(rho)) dx dt + k(rho) dx^2 + drho^2 + rho^2 dphi^2,
    k(rho) = 1 - eta * theta_eps(rho_max - rho),

with the Everett-Roman 1997 Eq. 35 smooth step.

Implementation: build the orthonormal-frame T_{hat mu hat nu} components
symbolically once at module-load time, then lambdify to NumPy.  This is
slower to import (~0.5s) but is provably correct -- the symbolic pipeline
was verified to reproduce Everett-Roman Eq. 14 exactly in the notebook
`krasnikov_tube.ipynb` Cell 2.
"""

from __future__ import annotations

import math
from itertools import product

import numpy as np
import sympy as sp


# ---------------------------------------------------------------------------
# One-time symbolic setup -> NumPy lambdas
# ---------------------------------------------------------------------------

def _build_T_lambdas():
    t, x, rho, phi = sp.symbols('t x rho phi', real=True)
    eta_s = sp.Symbol('eta', positive=True)
    eps_s = sp.Symbol('epsilon', positive=True)
    rho_max_s = sp.Symbol('rho_m', positive=True)

    theta_eps = sp.Rational(1, 2) * (sp.tanh(2 * (2 * (rho_max_s - rho) / eps_s - 1)) + 1)
    k = 1 - eta_s * theta_eps

    g = sp.Matrix([
        [-1,                        sp.Rational(1, 2) * (1 - k), 0, 0],
        [sp.Rational(1, 2) * (1 - k), k,                          0, 0],
        [0,                          0,                            1, 0],
        [0,                          0,                            0, rho**2],
    ])
    coords = (t, x, rho, phi)
    g_inv = g.inv()
    N = 4
    Gamma = [[[sp.S.Zero for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                s = sp.S.Zero
                for d in range(N):
                    s += g_inv[a, d] * (sp.diff(g[d, b], coords[c])
                                        + sp.diff(g[d, c], coords[b])
                                        - sp.diff(g[b, c], coords[d]))
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
    G_tensor = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            G_tensor[a, b] = Ricci[a, b] - sp.Rational(1, 2) * g[a, b] * R_scalar
    T_tensor = G_tensor / (8 * sp.pi)

    tetrad = sp.Matrix([
        [1, 0, 0, 0],
        [(1 - k) / (1 + k), 2 / (1 + k), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1 / rho],
    ])
    T_ortho = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            s = sp.S.Zero
            for a in range(4):
                for b in range(4):
                    s += tetrad[mu, a] * tetrad[nu, b] * T_tensor[a, b]
            T_ortho[mu, nu] = s  # skip simplify: too slow on tanh expressions

    args = (rho, eta_s, eps_s, rho_max_s)
    return {
        "Ttt": sp.lambdify(args, T_ortho[0, 0], 'numpy'),
        "Ttx": sp.lambdify(args, T_ortho[0, 1], 'numpy'),
        "Txx": sp.lambdify(args, T_ortho[1, 1], 'numpy'),
        "Trr": sp.lambdify(args, T_ortho[2, 2], 'numpy'),
        "Tpp": sp.lambdify(args, T_ortho[3, 3], 'numpy'),
    }


_T_LAMBDAS = _build_T_lambdas()


def _T_orthonormal(rho, eta, eps, rho_max):
    """Return (T_tt, T_tx, T_xx, T_rr, T_phiphi) in the static-observer
    orthonormal frame.  Vectorised over rho (NumPy)."""
    return tuple(_T_LAMBDAS[name](rho, eta, eps, rho_max)
                 for name in ("Ttt", "Ttx", "Txx", "Trr", "Tpp"))


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
    axes = config["axes"]
    grid = []
    for eta_v, eps_v, n_v in product(
        _axis(axes["eta"]),
        _axis(axes["eps"]),
        _axis(axes["n"]),  # n = rho_max / eps
    ):
        if eta_v >= 2.0:
            continue
        if n_v < 2.0:
            continue
        grid.append({
            "eta":     float(eta_v),
            "eps":     float(eps_v),
            "n":       float(n_v),
            "rho_max": float(eps_v * n_v),
            "n_rho":   int(config.get("n_rho", 401)),
            "margin":  float(config.get("margin", 3.0)),
        })
    return grid


def evaluate(point: dict) -> dict:
    eta = float(point["eta"])
    eps = float(point["eps"])
    rho_max = float(point["rho_max"])
    n_rho = int(point.get("n_rho", 401))
    margin = float(point.get("margin", 3.0))

    rhos = np.linspace(rho_max - margin * eps, rho_max + margin * eps, n_rho)
    Ttt, Ttx, Txx, Trr, Tpp = _T_orthonormal(rhos, eta, eps, rho_max)

    rho_p = -Ttt
    p_max = np.maximum.reduce([np.abs(Txx), np.abs(Trr), np.abs(Tpp)])
    flux = np.abs(Ttx)
    dec_slack = rho_p - np.maximum(p_max, flux)

    rho_p_min = float(np.min(rho_p))
    rho_p_max = float(np.max(rho_p))
    Ttt_min = float(np.min(Ttt))
    Ttt_max = float(np.max(Ttt))
    dec_slack_min = float(np.min(dec_slack))
    dec_slack_max = float(np.max(dec_slack))
    rho_at_min_density = float(rhos[int(np.argmin(rho_p))])
    rho_at_worst_dec = float(rhos[int(np.argmin(dec_slack))])

    wec_holds = bool(rho_p_min >= 0)
    dec_holds = bool(wec_holds and dec_slack_min >= 0)

    return {
        "eta": eta,
        "eps": eps,
        "n": float(point["n"]),
        "rho_max": rho_max,
        "Ttt_min": Ttt_min,
        "Ttt_max": Ttt_max,
        "rho_p_min": rho_p_min,
        "rho_p_max": rho_p_max,
        "dec_slack_min": dec_slack_min,
        "dec_slack_max": dec_slack_max,
        "rho_at_min_density": rho_at_min_density,
        "rho_at_worst_dec": rho_at_worst_dec,
        "wec_holds": wec_holds,
        "dec_holds": dec_holds,
        # Predicted scaling: -rho_p_min * eps^2 = kappa_K(eta), with empirical
        # small-eta limit kappa_K ~ 1.534 * eta / (4 pi) ~ 0.122 * eta.
        # See krasnikov_tube.ipynb Cell 13 for the fit.
        "kappa_K": -rho_p_min * eps * eps,
        "kappa_K_predicted_small_eta": 1.534 * eta / (4.0 * math.pi),
    }
