"""Phase 2D Task 2D.4 sweep: Fell-Heisenberg (m, n)-residual-WEC search.

Reproduces the Fell & Heisenberg 2021 (arXiv:2104.06488) smooth multi-mode
irrotational shift construction over a 6-D parameter grid (V, sigma, m0, a,
ell, r), then computes the full ADM stress-energy on a 3D Cartesian grid and
reports comprehensive energy-condition pass fractions.

Question: does any (V, sigma, m0, a, ell, r) point achieve full WEC pass
fraction = 1.0 (zero residual)? At the Session 10 anchor point
(V=0.5, sigma=4, m0=2, a=0.3, ell=4, r=6) the residual is ~1.3% of interior
cells. Fell & Heisenberg's text claims this is irreducible; their numerical
evidence is one parameter point. This sweep tests that claim.

The pipeline is a port of the analysis cells of fell_heisenberg.ipynb
(notebook cells 7, 11, 13). For each grid point we build the smooth
potential phi(X, Y, Z), compute its full Hessian, derive the extrinsic
curvature K_ij = -H_ij (irrotational + N=1 + flat gamma), and compute the
trace-reversed Eulerian-frame stress-energy S_ij from the dynamical equation
for K_ij with (3)R = 0. The principal pressures (eigenvalues of S_ij) give
both the full WEC slack rho + p_min and the full DEC slack rho - |p|_max
at every interior cell.
"""

from __future__ import annotations

import math
import time
from itertools import product
from typing import Any

import numpy as np
from scipy.special import erf


# ---------------------------------------------------------------------------
# Finite-difference helpers (verbatim port of notebook cell 7)
# ---------------------------------------------------------------------------

def fd_grad4(arr: np.ndarray, h: float, axis: int) -> np.ndarray:
    """4th-order centered first derivative with reflective edges.

    Internal nodes use stencil [+1, -8, 0, +8, -1]/(12h); edges fall back to
    np.gradient (2nd-order one-sided / centered).
    """
    out = np.gradient(arr, h, axis=axis, edge_order=2).copy()
    sl = [slice(None)] * arr.ndim

    def s(start, stop):
        sl_ = list(sl)
        sl_[axis] = slice(start, stop)
        return tuple(sl_)

    if arr.shape[axis] >= 5:
        out[s(2, -2)] = (
            -arr[s(4, None)]
            + 8 * arr[s(3, -1)]
            - 8 * arr[s(1, -3)]
            + arr[s(0, -4)]
        ) / (12 * h)
    return out


def hessian_4th(phi: np.ndarray, h: float):
    """Return (gradient, Hessian) of phi using 4th-order centered diffs.

    gradient: list of 3 arrays (d_i phi).
    Hessian:  array (3, 3, *phi.shape) with H[i,j] = d_i d_j phi.
    """
    g = [fd_grad4(phi, h, axis=ax) for ax in range(3)]
    H = np.empty((3, 3) + phi.shape, dtype=phi.dtype)
    for i in range(3):
        for j in range(3):
            H[i, j] = fd_grad4(g[j], h, axis=i)
    return g, H


def eulerian_rho_irrotational(phi: np.ndarray, h: float):
    """For irrotational shift N = grad phi: 8 pi rho_E = h1 + h2 + h3
    where h_i are the principal 2x2 minors of the Hessian.
    """
    _, H = hessian_4th(phi, h)
    h1 = H[1, 1] * H[2, 2] - H[1, 2] ** 2
    h2 = H[0, 0] * H[2, 2] - H[0, 2] ** 2
    h3 = H[0, 0] * H[1, 1] - H[0, 1] ** 2
    rho_E = (h1 + h2 + h3) / (8 * math.pi)
    return rho_E, H


def adm_stress_energy(phi: np.ndarray, h: float):
    """Compute the full Eulerian-frame stress-energy components for an
    irrotational static shift N = grad phi with unit lapse and flat 3-metric.

    Returns
    -------
    rho_E : np.ndarray
        Eulerian energy density (scalar field).
    K     : np.ndarray, shape (3, 3, *phi.shape)
        Extrinsic curvature K_ij = -d_i d_j phi (symmetrised).
    S_ij  : np.ndarray, shape (3, 3, *phi.shape)
        Spatial stress tensor.

    Derivation (port of notebook cell 13). Use the dynamical equation
        L_N K_ij = N (R_ij + K K_ij - 2 K_ik K^k_j
                      + 4 pi ((S - rho) gamma_ij - 2 S_ij))
    with N = 1, gamma flat, (3)R_ij = 0, K_ij = -H_ij (irrotational case).
    Solving the trace-reversed equation gives S_ij directly.
    """
    grads = [fd_grad4(phi, h, axis=ax) for ax in range(3)]

    # K_ij = -d_i d_j phi (symmetrised against finite-difference asymmetry).
    K = np.empty((3, 3) + phi.shape)
    for i in range(3):
        Ni = grads[i]
        for j in range(3):
            K[i, j] = -fd_grad4(Ni, h, axis=j)
    K = 0.5 * (K + np.transpose(K, (1, 0, 2, 3, 4)))
    Ktrace = K[0, 0] + K[1, 1] + K[2, 2]
    KijKij = sum(K[i, j] ** 2 for i in range(3) for j in range(3))

    rho_E = (Ktrace ** 2 - KijKij) / (16 * math.pi)

    KikKkj = np.einsum("ik...,kj...->ij...", K, K)

    # Lie derivative L_N K_ij  along  N^i = grads[i].
    LNK = np.zeros_like(K)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                LNK[i, j] += grads[k] * fd_grad4(K[i, j], h, axis=k)
                LNK[i, j] += K[k, j] * fd_grad4(grads[k], h, axis=i)
                LNK[i, j] += K[i, k] * fd_grad4(grads[k], h, axis=j)

    A_ij = -LNK + Ktrace[np.newaxis, np.newaxis] * K - 2 * KikKkj
    A_trace = A_ij[0, 0] + A_ij[1, 1] + A_ij[2, 2]
    eye3 = np.eye(3)[:, :, None, None, None]
    S_ij = (A_ij - 0.5 * A_trace[np.newaxis, np.newaxis] * eye3) / (16 * math.pi)
    S_ij += 0.5 * rho_E[np.newaxis, np.newaxis] * eye3

    return rho_E, K, S_ij


# ---------------------------------------------------------------------------
# Fell-Heisenberg smooth potential (verbatim port of notebook cell 11)
# ---------------------------------------------------------------------------

def phi_FH_smooth(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    Pi: float = 0.25,
    r: float = 6.0,
    V: float = 10.0,
    sigma: float = 1.0,
    m0: float = 2.0,
    a: float = 1.0,
    ell: float = 2.0,
) -> np.ndarray:
    """Fell-Heisenberg smooth C^2 potential, their Eq. (def:irrotationalpotential).

    The construction is parameterised by:
      Pi    radial-power exponent (Fell-Heisenberg fix at 0.25)
      r     bubble target radius
      V     overall amplitude
      sigma profile width parameter (variance of the Gaussian envelopes)
      m0    asymmetry baseline
      a     asymmetry amplitude (smaller a -> more symmetric)
      ell   asymmetry length scale along z
    """
    R2 = X ** 2 + Y ** 2 + Z ** 2
    R = np.sqrt(R2)
    R2Pi = (R2 + 1e-30) ** Pi
    m = m0 + a * np.tanh(Z / ell)
    n = m0 - a * np.tanh(Z / ell)
    arg1 = r - R2Pi / m
    arg2 = r + R2Pi / n
    e1 = np.exp(-arg1 ** 2 / sigma)
    e2 = np.exp(-arg2 ** 2 / sigma)
    e0 = np.exp(-R2 / sigma)
    erf0 = erf(R / math.sqrt(sigma))
    erf1 = erf(arg1 / math.sqrt(sigma))
    erf2 = erf(arg2 / math.sqrt(sigma))
    inner_exp = sigma * (e1 * m * n + e2 * m * n - e0 * (m + n))
    inner_erf = math.sqrt(sigma * math.pi) * (
        -((m + n) * R * erf0)
        + n * (m * R - R2Pi) * erf1
        + m * (n * R - R2Pi) * erf2
    )
    phi = V / (m + n + 1e-30) * (inner_exp + inner_erf)
    return phi


# ---------------------------------------------------------------------------
# build_grid + evaluate (sweep interface)
# ---------------------------------------------------------------------------

def _axis(spec: dict) -> list[float]:
    """Expand an axis spec ``{lo, hi, n, scale}`` into concrete values."""
    lo, hi, n = spec["lo"], spec["hi"], int(spec["n"])
    scale = spec.get("scale", "linear")
    if scale == "log":
        if lo <= 0 or hi <= 0:
            raise ValueError("log axis needs positive bounds")
        if n == 1:
            return [lo]
        log_lo, log_hi = math.log(lo), math.log(hi)
        step = (log_hi - log_lo) / (n - 1)
        return [math.exp(log_lo + i * step) for i in range(n)]
    if n == 1:
        return [lo]
    step = (hi - lo) / (n - 1)
    return [lo + i * step for i in range(n)]


def build_grid(config: dict) -> list[dict]:
    """Expand a sweep config into per-point evaluation records.

    Required config keys
    --------------------
    L      half-width of the cubic evaluation box
    Npts   number of grid samples per axis (cubic grid Npts^3)
    Pi     fixed radial-power exponent (Fell-Heisenberg use 0.25)
    axes   dict with per-axis specs for V, sigma, m0, a, ell, r

    Per-axis sanity: a > 0 must hold strictly (a = 0 makes m == n and
    asymmetry vanishes trivially), and 2*m0 > a so that both m and n stay
    positive (denominator m + n stays well away from zero).
    """
    axes = config["axes"]
    L = float(config.get("L", 12.0))
    Npts = int(config.get("Npts", 49))
    Pi_val = float(config.get("Pi", 0.25))

    grid: list[dict] = []
    for V_v, s_v, m_v, a_v, ell_v, r_v in product(
        _axis(axes["V"]),
        _axis(axes["sigma"]),
        _axis(axes["m0"]),
        _axis(axes["a"]),
        _axis(axes["ell"]),
        _axis(axes["r"]),
    ):
        if a_v <= 0:
            continue
        if 2 * m_v <= a_v + 1e-9:
            continue  # m or n would be non-positive at large |Z|
        if r_v >= L - 1.0:
            continue  # bubble must fit inside the box with margin
        grid.append(
            {
                "V": float(V_v),
                "sigma": float(s_v),
                "m0": float(m_v),
                "a": float(a_v),
                "ell": float(ell_v),
                "r": float(r_v),
                "Pi": Pi_val,
                "L": L,
                "Npts": Npts,
            }
        )
    return grid


def evaluate(point: dict) -> dict:
    """Evaluate one Fell-Heisenberg parameter point.

    Returns a record matching the schema in the project plan: parameter
    echo, validity flags, Eulerian rho_E statistics, full WEC slack, full
    DEC slack, integrated energies, and per-point timing.
    """
    t0 = time.time()

    L = float(point["L"])
    Npts = int(point["Npts"])
    Pi_val = float(point.get("Pi", 0.25))
    V = float(point["V"])
    sigma = float(point["sigma"])
    m0 = float(point["m0"])
    a = float(point["a"])
    ell = float(point["ell"])
    r = float(point["r"])

    record: dict[str, Any] = {**point}
    nan = float("nan")
    record.update(
        {
            "ok": False,
            "error": None,
            "central_N_max": nan,
            "rho_E_min": nan,
            "rho_E_max": nan,
            "rho_E_pos_fraction": nan,
            "wec_slack_min": nan,
            "wec_slack_max": nan,
            "wec_pass_fraction": nan,
            "dec_slack_min": nan,
            "dec_slack_max": nan,
            "dec_pass_fraction": nan,
            "E_pos": nan,
            "E_neg": nan,
            "E_net": nan,
            "eval_seconds": nan,
        }
    )

    try:
        xs = np.linspace(-L, L, Npts)
        h = float(xs[1] - xs[0])
        X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")

        phi = phi_FH_smooth(X, Y, Z, Pi=Pi_val, r=r, V=V, sigma=sigma, m0=m0, a=a, ell=ell)
        if not np.all(np.isfinite(phi)):
            record["error"] = "non-finite phi (potential overflow)"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        rho_E_irrot, _ = eulerian_rho_irrotational(phi, h)
        rho_full, K, S_full = adm_stress_energy(phi, h)

        # ADM stride-6 interior matches the notebook (cell 13).
        interior = (slice(6, -6),) * 3
        rho_arr = rho_full[interior]
        if not np.all(np.isfinite(rho_arr)):
            record["error"] = "non-finite ADM stress-energy"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        # Diagonalise S_ij at every interior point to extract principal pressures.
        S_arr = S_full.transpose(2, 3, 4, 0, 1)[interior]
        S_flat = S_arr.reshape(-1, 3, 3)
        evals = np.linalg.eigvalsh(S_flat)
        p_min = evals.min(axis=1).reshape(rho_arr.shape)
        p_abs_max = np.abs(evals).max(axis=1).reshape(rho_arr.shape)

        wec_slack = rho_arr + p_min
        dec_slack = rho_arr - p_abs_max

        # Eulerian-energy statistics on stride-4 interior (matches notebook cell 11).
        e_interior = (slice(4, -4),) * 3
        rho_E_for_int = rho_E_irrot[e_interior]
        rho_E_pos_fraction = float((rho_E_for_int > 0).mean())

        # Integrated geometric-unit energies.
        vol = h ** 3
        E_pos = float((rho_E_irrot[rho_E_irrot > 0]).sum() * vol)
        E_neg = float((rho_E_irrot[rho_E_irrot < 0]).sum() * vol)
        E_net = E_pos + E_neg

        # Central |N| max in 7^3 cube around origin.
        grads = [fd_grad4(phi, h, axis=ax) for ax in range(3)]
        Nmag = np.sqrt(grads[0] ** 2 + grads[1] ** 2 + grads[2] ** 2)
        central = (slice(Npts // 2 - 3, Npts // 2 + 4),) * 3
        central_N_max = float(Nmag[central].max())

        record.update(
            {
                "ok": True,
                "central_N_max": central_N_max,
                "rho_E_min": float(rho_E_for_int.min()),
                "rho_E_max": float(rho_E_for_int.max()),
                "rho_E_pos_fraction": rho_E_pos_fraction,
                "wec_slack_min": float(wec_slack.min()),
                "wec_slack_max": float(wec_slack.max()),
                "wec_pass_fraction": float((wec_slack >= 0).mean()),
                "dec_slack_min": float(dec_slack.min()),
                "dec_slack_max": float(dec_slack.max()),
                "dec_pass_fraction": float((dec_slack >= 0).mean()),
                "E_pos": E_pos,
                "E_neg": E_neg,
                "E_net": E_net,
                "eval_seconds": float(time.time() - t0),
            }
        )
        return record
    except Exception as exc:  # pragma: no cover - defensive
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["eval_seconds"] = float(time.time() - t0)
        return record
