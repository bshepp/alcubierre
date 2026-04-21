"""Phase 2D Task 2D.11 sweep: Fell-Heisenberg ansatz augmented with vorticity.

Generalises the irrotational FH shift ``N = grad phi`` to
``N = grad phi + curl A`` and asks whether vortical augmentation either
(a) recovers a finite-volume passenger zone (the Session 14 wall finding said
the irrotational FH "all-wall-no-interior" passenger zone scales as h^3) or
(b) still admits strict WEC+DEC pass.

Phase 1 of three: **axisymmetric A_phi(R, Z)** — single azimuthal vector
potential component preserves Z-axis symmetry and adds the smallest number
of new parameters. Subsequent Phase 2 (Cartesian A with ∇·A=0) and Phase 3
(FH-style multi-mode A) live in sibling modules.

Vector potential ansatz (this phase):

    A_phi(R, Z) = V_A · R · exp(-(R - r_A)^2 / sigma_A^2)
                          · tanh(Z / ell_A)
                          · exp(-Z^2 / (2 sigma_A^2))

The leading R factor enforces regularity on the Z-axis (A_phi → 0 as R → 0
so that A_x = -Y A_phi/R, A_y = X A_phi/R remain bounded). The tanh×Gaussian
Z-dependence mirrors the FH potential's tanh asymmetry while the Gaussian
envelope ensures decay at large |Z|. This is one specific choice; the form
is documented inline so a future agent can swap it cleanly.

Cartesian conversion: with hat_phi = (-Y, X, 0)/R,

    A_x = -Y · (A_phi / R) ;  A_y = X · (A_phi / R) ;  A_z = 0

and we evaluate ``(A_phi / R)`` directly to avoid R=0 singularities (since
A_phi ∝ R, the quotient is regular). The curl is then computed by 4th-order
finite difference.
"""

from __future__ import annotations

import math
import time
from itertools import product
from typing import Any

import numpy as np
from scipy import ndimage

from hf_jobs.sweeps.fell_heisenberg import (
    adm_stress_energy_from_N,
    eulerian_rho_irrotational,
    fd_grad4,
    phi_FH_smooth,
    _axis,
)


# ---------------------------------------------------------------------------
# Vortical vector-potential and curl
# ---------------------------------------------------------------------------

def A_over_R_axisymm(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    V_A: float,
    sigma_A: float,
    r_A: float,
    ell_A: float,
) -> np.ndarray:
    """Return ``A_phi / R`` for the axisymmetric vortical ansatz.

    Defined as ``V_A · exp(-(R - r_A)^2 / sigma_A^2) · tanh(Z / ell_A)
    · exp(-Z^2 / (2 sigma_A^2))`` — the leading ``R`` factor of
    ``A_phi = R · (this)`` is absorbed into the Cartesian multipliers
    ``A_x = -Y · (A/R)``, ``A_y = X · (A/R)``.
    """
    R = np.sqrt(X ** 2 + Y ** 2)
    radial = np.exp(-((R - r_A) ** 2) / (sigma_A ** 2))
    z_asym = np.tanh(Z / ell_A)
    z_envelope = np.exp(-(Z ** 2) / (2.0 * sigma_A ** 2))
    return V_A * radial * z_asym * z_envelope


def curl_A_axisymm(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    h: float,
    V_A: float,
    sigma_A: float,
    r_A: float,
    ell_A: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cartesian components of ``curl A`` for the axisymmetric ansatz.

    Computes ``A_x, A_y, A_z`` on the grid then takes the FD curl. Returns
    ``(curl_X, curl_Y, curl_Z)`` arrays with the same shape as ``X``.
    """
    A_over_R = A_over_R_axisymm(X, Y, Z, V_A, sigma_A, r_A, ell_A)
    A_x = -Y * A_over_R
    A_y = X * A_over_R
    # A_z = 0 identically.

    # curl A = (dA_z/dy - dA_y/dz, dA_x/dz - dA_z/dx, dA_y/dx - dA_x/dy).
    dAy_dz = fd_grad4(A_y, h, axis=2)
    dAx_dz = fd_grad4(A_x, h, axis=2)
    dAy_dx = fd_grad4(A_y, h, axis=0)
    dAx_dy = fd_grad4(A_x, h, axis=1)

    curl_x = -dAy_dz
    curl_y = dAx_dz
    curl_z = dAy_dx - dAx_dy
    return curl_x, curl_y, curl_z


# ---------------------------------------------------------------------------
# Passenger-zone diagnostic (inline copy from fell_heisenberg_horizon.py
# so the sweep produces this metric without a separate analysis pass)
# ---------------------------------------------------------------------------

def passenger_zone(Nmag: np.ndarray, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, h: float) -> tuple[float, float]:
    """Return ``(passenger_zone_volume, passenger_zone_radius)``.

    Passenger zone = connected component of ``|N| < 1`` containing the origin.
    Radius = smallest distance from origin to any non-passenger cell. Returns
    ``(0.0, 0.0)`` if the origin sits in the superluminal region.
    """
    superluminal = Nmag >= 1.0
    subluminal = ~superluminal
    sub_labels, _ = ndimage.label(subluminal, structure=ndimage.generate_binary_structure(3, 1))
    Npts = Nmag.shape[0]
    origin_label = int(sub_labels[Npts // 2, Npts // 2, Npts // 2])
    if origin_label == 0:
        return 0.0, 0.0
    passenger_mask = sub_labels == origin_label
    passenger_volume = float(passenger_mask.sum() * h ** 3)
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    non_pass_R = R[~passenger_mask]
    passenger_radius = float(non_pass_R.min()) if non_pass_R.size > 0 else float(R.max())
    return passenger_volume, passenger_radius


# ---------------------------------------------------------------------------
# build_grid + evaluate (sweep interface)
# ---------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand a sweep config into per-point evaluation records.

    Required config keys
    --------------------
    L, Npts, Pi   as in :mod:`hf_jobs.sweeps.fell_heisenberg`
    axes          dict with per-axis specs for V, sigma, m0, a, ell, r,
                  V_A, sigma_A, r_A, ell_A

    Sanity rules
    ------------
    - ``a > 0`` strictly and ``2 m0 > a`` (FH denominator regularity).
    - ``r < L - 1`` (bubble fits in the box with margin).
    - ``sigma_A > 0``, ``ell_A > 0``, ``r_A > 0`` (vortical envelope sanity).
    - V_A = 0 is permitted (irrotational baseline via the augmented pipeline).
    """
    axes = config["axes"]
    L = float(config.get("L", 12.0))
    Npts = int(config.get("Npts", 49))
    Pi_val = float(config.get("Pi", 0.25))

    fh_axes = ("V", "sigma", "m0", "a", "ell", "r")
    vort_axes = ("V_A", "sigma_A", "r_A", "ell_A")
    for k in fh_axes + vort_axes:
        if k not in axes:
            raise KeyError(f"axes config missing required key: {k}")

    grid: list[dict] = []
    for V_v, s_v, m_v, a_v, ell_v, r_v, VA_v, sA_v, rA_v, lA_v in product(
        _axis(axes["V"]),
        _axis(axes["sigma"]),
        _axis(axes["m0"]),
        _axis(axes["a"]),
        _axis(axes["ell"]),
        _axis(axes["r"]),
        _axis(axes["V_A"]),
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
        if sA_v <= 0 or lA_v <= 0 or rA_v <= 0:
            continue
        grid.append(
            {
                "V": float(V_v),
                "sigma": float(s_v),
                "m0": float(m_v),
                "a": float(a_v),
                "ell": float(ell_v),
                "r": float(r_v),
                "V_A": float(VA_v),
                "sigma_A": float(sA_v),
                "r_A": float(rA_v),
                "ell_A": float(lA_v),
                "Pi": Pi_val,
                "L": L,
                "Npts": Npts,
            }
        )
    return grid


def evaluate(point: dict) -> dict:
    """Evaluate one vorticity-augmented FH parameter point.

    Output schema mirrors :func:`hf_jobs.sweeps.fell_heisenberg.evaluate`
    plus four extra fields:

    - ``N_vortical_max`` : max ``|curl A|`` on stride-4 interior
    - ``N_vortical_origin`` : ``|curl A|`` at the box centre
    - ``passenger_zone_volume``, ``passenger_zone_radius`` : foliation-health
      diagnostics from :func:`passenger_zone` (computed inline so the sweep
      can triage which points warrant a separate horizon-analysis pass).
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
    V_A = float(point["V_A"])
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

        # Irrotational shift component.
        grad_phi = [fd_grad4(phi, h, axis=ax) for ax in range(3)]

        # Vortical shift component: curl A.
        curl_x, curl_y, curl_z = curl_A_axisymm(X, Y, Z, h, V_A, sigma_A, r_A, ell_A)
        if not (np.all(np.isfinite(curl_x)) and np.all(np.isfinite(curl_y)) and np.all(np.isfinite(curl_z))):
            record["error"] = "non-finite curl A"
            record["eval_seconds"] = float(time.time() - t0)
            return record

        # Total shift N = grad phi + curl A.
        N = [grad_phi[0] + curl_x, grad_phi[1] + curl_y, grad_phi[2] + curl_z]

        # Eulerian-rho diagnostic on irrotational part only (used for E_pos/E_neg/E_net,
        # rho_E_pos_fraction, central |N|max consistency with baseline sweep).
        rho_E_irrot, _ = eulerian_rho_irrotational(phi, h)

        # Full ADM stress-energy from the augmented shift.
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
    except Exception as exc:  # pragma: no cover - defensive
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["eval_seconds"] = float(time.time() - t0)
        return record
