"""Phase 2D Task 2D.11 sweep: vorticity-augmented FH ansatz, Cartesian A.

Phase 2 of three (Phase 1 = axisymmetric A_phi; Phase 2 = Cartesian A with
constant amplitudes; Phase 3 = FH-style multi-mode A). Phase 1 was negative
within its slice (see FELL_HEISENBERG_VORTICAL_NOTES.md §1).

Vector-potential ansatz (this phase):

    A_i(X, Y, Z) = V_{A,i} · exp(-(R - r_A)^2 / sigma_A^2)
                           · exp(-Z^2 / (2 sigma_A^2))
                           · tanh(Z / ell_A)        for i in {x, y, z}

with R = sqrt(X^2 + Y^2). Three independent amplitudes (V_Ax, V_Ay, V_Az)
for each Cartesian direction sharing the same Gaussian-modulated profile.
This is genuinely distinct from Phase 1 (where A pointed in the locally-
rotating phi-hat direction); here A points in a fixed direction. No gauge
fix is needed: the physical vortical shift curl A is gauge-invariant, so
sweeping the three amplitudes sweeps over physically distinct curls.

The shared profile is the same Gaussian × tanh × Gaussian envelope used in
Phase 1 (proven well-behaved on the canonical FH grid). The pipeline reuses
adm_stress_energy_from_N + the inline passenger_zone diagnostic from the
Phase-1 module.
"""

from __future__ import annotations

import time
from itertools import product
from typing import Any

import numpy as np

from hf_jobs.sweeps.fell_heisenberg import (
    adm_stress_energy_from_N,
    eulerian_rho_irrotational,
    fd_grad4,
    phi_FH_smooth,
    _axis,
)
from hf_jobs.sweeps.fell_heisenberg_vortical import passenger_zone


def A_cartesian_profile(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    sigma_A: float,
    r_A: float,
    ell_A: float,
) -> np.ndarray:
    """Shared scalar profile g(X,Y,Z) = exp(-(R-r_A)^2/sigma_A^2) ·
    exp(-Z^2/(2 sigma_A^2)) · tanh(Z/ell_A)."""
    R = np.sqrt(X ** 2 + Y ** 2)
    radial = np.exp(-((R - r_A) ** 2) / (sigma_A ** 2))
    z_envelope = np.exp(-(Z ** 2) / (2.0 * sigma_A ** 2))
    z_asym = np.tanh(Z / ell_A)
    return radial * z_envelope * z_asym


def curl_A_cartesian(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    h: float,
    V_Ax: float,
    V_Ay: float,
    V_Az: float,
    sigma_A: float,
    r_A: float,
    ell_A: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cartesian components of curl A for the constant-amplitude ansatz."""
    g = A_cartesian_profile(X, Y, Z, sigma_A, r_A, ell_A)
    A_x = V_Ax * g
    A_y = V_Ay * g
    A_z = V_Az * g

    # curl A = (dA_z/dy - dA_y/dz, dA_x/dz - dA_z/dx, dA_y/dx - dA_x/dy).
    dAz_dy = fd_grad4(A_z, h, axis=1)
    dAy_dz = fd_grad4(A_y, h, axis=2)
    dAx_dz = fd_grad4(A_x, h, axis=2)
    dAz_dx = fd_grad4(A_z, h, axis=0)
    dAy_dx = fd_grad4(A_y, h, axis=0)
    dAx_dy = fd_grad4(A_x, h, axis=1)

    curl_x = dAz_dy - dAy_dz
    curl_y = dAx_dz - dAz_dx
    curl_z = dAy_dx - dAx_dy
    return curl_x, curl_y, curl_z


def build_grid(config: dict) -> list[dict]:
    """Expand a Cartesian-A sweep config into per-point evaluation records.

    Required axes: V, sigma, m0, a, ell, r (FH); V_Ax, V_Ay, V_Az, sigma_A,
    r_A, ell_A (vortical). Same FH sanity rules as the irrotational sweep;
    sigma_A > 0, ell_A > 0, r_A > 0 for the vortical envelope. V_A* may be
    any sign or zero (zero reproduces irrotational baseline, sign flips
    swap the curl direction).
    """
    axes = config["axes"]
    L = float(config.get("L", 12.0))
    Npts = int(config.get("Npts", 49))
    Pi_val = float(config.get("Pi", 0.25))

    fh_axes = ("V", "sigma", "m0", "a", "ell", "r")
    vort_axes = ("V_Ax", "V_Ay", "V_Az", "sigma_A", "r_A", "ell_A")
    for k in fh_axes + vort_axes:
        if k not in axes:
            raise KeyError(f"axes config missing required key: {k}")

    grid: list[dict] = []
    for V_v, s_v, m_v, a_v, ell_v, r_v, VAx, VAy, VAz, sA, rA, lA in product(
        _axis(axes["V"]),
        _axis(axes["sigma"]),
        _axis(axes["m0"]),
        _axis(axes["a"]),
        _axis(axes["ell"]),
        _axis(axes["r"]),
        _axis(axes["V_Ax"]),
        _axis(axes["V_Ay"]),
        _axis(axes["V_Az"]),
        _axis(axes["sigma_A"]),
        _axis(axes["r_A"]),
        _axis(axes["ell_A"]),
    ):
        if a_v <= 0:
            continue
        if 2 * m_v <= a_v + 1e-9:
            continue
        if r_v >= L - 1.0:
            continue
        if sA <= 0 or lA <= 0 or rA <= 0:
            continue
        grid.append(
            {
                "V": float(V_v),
                "sigma": float(s_v),
                "m0": float(m_v),
                "a": float(a_v),
                "ell": float(ell_v),
                "r": float(r_v),
                "V_Ax": float(VAx),
                "V_Ay": float(VAy),
                "V_Az": float(VAz),
                "sigma_A": float(sA),
                "r_A": float(rA),
                "ell_A": float(lA),
                "Pi": Pi_val,
                "L": L,
                "Npts": Npts,
            }
        )
    return grid


def evaluate(point: dict) -> dict:
    """Evaluate one Cartesian-A vorticity-augmented FH parameter point.

    Output schema mirrors the Phase-1 sweep, with vortical-amplitude fields
    expanded to (V_Ax, V_Ay, V_Az) instead of a single scalar.
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
    V_Ax = float(point["V_Ax"])
    V_Ay = float(point["V_Ay"])
    V_Az = float(point["V_Az"])
    sigma_A = float(point["sigma_A"])
    r_A = float(point["r_A"])
    ell_A = float(point["ell_A"])

    record: dict[str, Any] = {**point}
    nan = float("nan")
    record.update(
        {
            "ok": False,
            "error": None,
            "central_N_max": nan,
            "N_vortical_max": nan,
            "N_vortical_origin": nan,
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
            "passenger_zone_volume": nan,
            "passenger_zone_radius": nan,
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

        grad_phi = [fd_grad4(phi, h, axis=ax) for ax in range(3)]

        curl_x, curl_y, curl_z = curl_A_cartesian(
            X, Y, Z, h, V_Ax, V_Ay, V_Az, sigma_A, r_A, ell_A
        )
        if not (np.all(np.isfinite(curl_x)) and np.all(np.isfinite(curl_y)) and np.all(np.isfinite(curl_z))):
            record["error"] = "non-finite curl A"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        N = [grad_phi[0] + curl_x, grad_phi[1] + curl_y, grad_phi[2] + curl_z]

        rho_E_irrot, _ = eulerian_rho_irrotational(phi, h)
        rho_full, K, S_full = adm_stress_energy_from_N(N, h)

        interior = (slice(6, -6),) * 3
        rho_arr = rho_full[interior]
        if not np.all(np.isfinite(rho_arr)):
            record["error"] = "non-finite ADM stress-energy"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        S_arr = S_full.transpose(2, 3, 4, 0, 1)[interior]
        S_flat = S_arr.reshape(-1, 3, 3)
        evals = np.linalg.eigvalsh(S_flat)
        p_min = evals.min(axis=1).reshape(rho_arr.shape)
        p_abs_max = np.abs(evals).max(axis=1).reshape(rho_arr.shape)

        wec_slack = rho_arr + p_min
        dec_slack = rho_arr - p_abs_max

        e_interior = (slice(4, -4),) * 3
        rho_E_for_int = rho_E_irrot[e_interior]
        rho_E_pos_fraction = float((rho_E_for_int > 0).mean())

        vol = h ** 3
        E_pos = float((rho_E_irrot[rho_E_irrot > 0]).sum() * vol)
        E_neg = float((rho_E_irrot[rho_E_irrot < 0]).sum() * vol)
        E_net = E_pos + E_neg

        Nmag = np.sqrt(N[0] ** 2 + N[1] ** 2 + N[2] ** 2)
        central = (slice(Npts // 2 - 3, Npts // 2 + 4),) * 3
        central_N_max = float(Nmag[central].max())

        curl_mag = np.sqrt(curl_x ** 2 + curl_y ** 2 + curl_z ** 2)
        N_vortical_max = float(curl_mag[e_interior].max())
        mid = Npts // 2
        N_vortical_origin = float(curl_mag[mid, mid, mid])

        passenger_volume, passenger_radius = passenger_zone(Nmag, X, Y, Z, h)

        record.update(
            {
                "ok": True,
                "central_N_max": central_N_max,
                "N_vortical_max": N_vortical_max,
                "N_vortical_origin": N_vortical_origin,
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
                "passenger_zone_volume": passenger_volume,
                "passenger_zone_radius": passenger_radius,
                "eval_seconds": float(time.time() - t0),
            }
        )
        return record
    except Exception as exc:  # pragma: no cover
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["eval_seconds"] = float(time.time() - t0)
        return record
