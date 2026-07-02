"""Phase 2D Task 2D.11 sweep: vorticity-augmented FH ansatz, Phase 3 --
FH-style multi-mode Cartesian A.

Phase 3 of three (Phase 1 = axisymmetric A_phi; Phase 2 = Cartesian A with
constant amplitudes + shared Gaussian envelope; both NEGATIVE within their
slices, see FELL_HEISENBERG_VORTICAL_NOTES.md Secs. 1-2). Phase 3 removes
the "simple envelope" restriction those negatives share: each Cartesian
component of the vector potential carries its OWN independent FH-style
potential structure -- the same sums-of-erf/exp construction, fractional
Pi-power and z-asymmetry as phi_FH itself -- so the curl-A support has the
same multi-scale wall structure as the FH bubble it is trying to repair,
instead of a single Gaussian shell.

Vector-potential ansatz (this phase):

    A_i(X, Y, Z) = V_Ai * phiFH(X, Y, Z; Pi, r=r_Ai, V=1, sigma=sigma_A,
                                m0, a, ell) / max|grad phiFH(...)|
                                                        for i in {x, y, z}

i.e. each component is a full FH potential with its own bubble radius r_Ai
and shared structure width sigma_A, gradient-normalised on the grid so the
swept amplitude V_Ai directly sets the scale of that component's
contribution to the vortical shift (|curl A| ~ O(sum |V_Ai|), reported
exactly via N_vortical_max). The asymmetry/exponent parameters (m0, a, ell,
Pi) of the A-structure are INHERITED from the FH background point -- a
deliberate slice restriction to keep the preview tractable; recorded in the
notes. Independent per-component radii are the "multi-mode" element: the
three curl source shells need not coincide with each other or with the FH
wall.

No gauge fix (as in Phase 2): curl A is gauge-invariant.

V_Ax = V_Ay = V_Az = 0 reproduces the irrotational baseline bit-exactly
(regression-checked; zero curl terms added to grad phi).

Pipeline reuses adm_stress_energy_from_N + the inline passenger-zone
diagnostic, identical to Phases 1-2, so records are directly comparable.
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


def A_component_fh(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    h: float,
    V_Ai: float,
    r_Ai: float,
    sigma_A: float,
    Pi_val: float,
    m0: float,
    a: float,
    ell: float,
) -> np.ndarray:
    """One Cartesian component: gradient-normalised FH-form potential.

    Returns V_Ai * phiFH_hat where max|grad phiFH_hat| = 1 on the grid, so
    V_Ai directly scales this component's vortical-shift contribution.
    """
    if V_Ai == 0.0:
        return np.zeros_like(X)
    phi_hat = phi_FH_smooth(
        X, Y, Z, Pi=Pi_val, r=r_Ai, V=1.0, sigma=sigma_A, m0=m0, a=a, ell=ell
    )
    g = [fd_grad4(phi_hat, h, axis=ax) for ax in range(3)]
    gmax = float(np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2).max())
    return (V_Ai / (gmax + 1e-30)) * phi_hat


def curl_A_multimode(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    h: float,
    V_Ax: float,
    V_Ay: float,
    V_Az: float,
    r_Ax: float,
    r_Ay: float,
    r_Az: float,
    sigma_A: float,
    Pi_val: float,
    m0: float,
    a: float,
    ell: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cartesian components of curl A for the FH-multi-mode ansatz."""
    A_x = A_component_fh(X, Y, Z, h, V_Ax, r_Ax, sigma_A, Pi_val, m0, a, ell)
    A_y = A_component_fh(X, Y, Z, h, V_Ay, r_Ay, sigma_A, Pi_val, m0, a, ell)
    A_z = A_component_fh(X, Y, Z, h, V_Az, r_Az, sigma_A, Pi_val, m0, a, ell)

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
    """Expand a multi-mode-A sweep config into per-point records.

    Required axes: V, sigma, m0, a, ell, r (FH); V_Ax, V_Ay, V_Az, r_Ax,
    r_Ay, r_Az, sigma_A (vortical). Same FH sanity rules as the
    irrotational sweep. When a component amplitude is exactly 0 its radius
    is canonicalised to 0.0 (the component vanishes identically), and the
    resulting duplicate points are removed -- keeps the all-zero
    irrotational baseline to a single row.
    """
    axes = config["axes"]
    L = float(config.get("L", 12.0))
    Npts = int(config.get("Npts", 49))
    Pi_val = float(config.get("Pi", 0.25))

    fh_axes = ("V", "sigma", "m0", "a", "ell", "r")
    vort_axes = ("V_Ax", "V_Ay", "V_Az", "r_Ax", "r_Ay", "r_Az", "sigma_A")
    for k in fh_axes + vort_axes:
        if k not in axes:
            raise KeyError(f"axes config missing required key: {k}")

    seen: set[tuple] = set()
    grid: list[dict] = []
    for (V_v, s_v, m_v, a_v, ell_v, r_v,
         VAx, VAy, VAz, rAx, rAy, rAz, sA) in product(
        _axis(axes["V"]),
        _axis(axes["sigma"]),
        _axis(axes["m0"]),
        _axis(axes["a"]),
        _axis(axes["ell"]),
        _axis(axes["r"]),
        _axis(axes["V_Ax"]),
        _axis(axes["V_Ay"]),
        _axis(axes["V_Az"]),
        _axis(axes["r_Ax"]),
        _axis(axes["r_Ay"]),
        _axis(axes["r_Az"]),
        _axis(axes["sigma_A"]),
    ):
        if a_v <= 0:
            continue
        if 2 * m_v <= a_v + 1e-9:
            continue
        if r_v >= L - 1.0:
            continue
        if sA <= 0 or rAx <= 0 or rAy <= 0 or rAz <= 0:
            continue
        # canonicalise radii of vanishing components, then dedupe
        rAx_c = rAx if VAx != 0.0 else 0.0
        rAy_c = rAy if VAy != 0.0 else 0.0
        rAz_c = rAz if VAz != 0.0 else 0.0
        # sigma_A is irrelevant when all three amplitudes vanish
        sA_c = sA if (VAx, VAy, VAz) != (0.0, 0.0, 0.0) else 0.0
        key = (V_v, s_v, m_v, a_v, ell_v, r_v,
               VAx, VAy, VAz, rAx_c, rAy_c, rAz_c, sA_c)
        if key in seen:
            continue
        seen.add(key)
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
                "r_Ax": float(rAx_c),
                "r_Ay": float(rAy_c),
                "r_Az": float(rAz_c),
                "sigma_A": float(sA_c),
                "Pi": Pi_val,
                "L": L,
                "Npts": Npts,
            }
        )
    return grid


def evaluate(point: dict) -> dict:
    """Evaluate one FH-multi-mode vorticity-augmented parameter point.

    Output schema mirrors Phases 1-2 so rows are directly comparable.
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
    r_Ax = float(point["r_Ax"])
    r_Ay = float(point["r_Ay"])
    r_Az = float(point["r_Az"])
    sigma_A = float(point["sigma_A"])

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

        phi = phi_FH_smooth(
            X, Y, Z, Pi=Pi_val, r=r, V=V, sigma=sigma, m0=m0, a=a, ell=ell
        )
        if not np.all(np.isfinite(phi)):
            record["error"] = "non-finite phi (potential overflow)"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        grad_phi = [fd_grad4(phi, h, axis=ax) for ax in range(3)]

        # sigma_A = 0 is the canonicalised all-amplitudes-zero baseline row;
        # A_component_fh short-circuits on V_Ai == 0, so pass a dummy 1.0.
        sA_eff = sigma_A if sigma_A > 0 else 1.0
        curl_x, curl_y, curl_z = curl_A_multimode(
            X, Y, Z, h, V_Ax, V_Ay, V_Az,
            max(r_Ax, 1e-3), max(r_Ay, 1e-3), max(r_Az, 1e-3),
            sA_eff, Pi_val, m0, a, ell,
        )
        if not (
            np.all(np.isfinite(curl_x))
            and np.all(np.isfinite(curl_y))
            and np.all(np.isfinite(curl_z))
        ):
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
