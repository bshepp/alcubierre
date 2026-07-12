"""Session 50 -- Task 2E.4 residual axis: JOINT vortical + Pi sweep with
independently varied A-structure exponents, under the dual-box protocol.

The last computational sub-axis of 2E.4. Sessions 33/38 closed multi-mode
vortical A with exponents INHERITED from the FH background; Session 44
closed the background-Pi axis alone (far-field gate negative at every Pi:
the R-linear growth of phi carries no Pi). This sweep varies the
A-structure's exponents INDEPENDENTLY of the background Pi -- including
per-component splits -- asking whether any joint combination cancels the
far-field violation or opens the passenger zone.

Ansatz: N = grad phi(Pi) + curl A, with each Cartesian component

    A_i = V_Ai * phiFH(X,Y,Z; Pi_Ai, r_Ai, V=1, sigma_A, m0, a, ell) / gmax_i

gradient-normalised with gmax_i measured ON THE L=12 GRID and reused for
the L=45 far-field box (one physical field, two evaluation windows -- a
grid-local renormalisation would silently change the ansatz between boxes).

Dual-box protocol (Session-42 rule, as in Session 44): L = 12, Npts = 65
box ECs + passenger zone + central |N|; L = 45, Npts = 65 far-field WEC/DEC
slack minima (the decisive gate -- Session 42 proved box strict-pass alone
is truncation-scoped).

Slice scope: adopted m,n concretization (m,n = m0 +/- a tanh(Z/ell), a > 0);
three certified anchor structures (A1, B1, S12 of Sessions 38/42/44);
Pi, Pi_A in [0.125, 1]; FH-form A components (gradient-normalised, own
radii/exponents, shared sigma_A); FD pipeline at Npts = 65 (validated for
smooth FH fields, cross-checked to 2.1e-4 at these anchors -- Session 42);
static, classical.
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np

from hf_jobs.sweeps.fell_heisenberg import (
    adm_stress_energy_from_N,
    fd_grad4,
    phi_FH_smooth,
)
from hf_jobs.sweeps.fell_heisenberg_vortical import passenger_zone

ANCHORS = {
    "A1":  dict(V=1.5, sigma=10.0, m0=3.0, a=0.223606797749979, ell=6.0, r=9.0),
    "B1":  dict(V=1.5, sigma=6.0,  m0=3.0, a=0.223606797749979, ell=6.0, r=7.75),
    "S12": dict(V=1.5, sigma=10.0, m0=3.0, a=0.05,              ell=4.0, r=9.0),
}


def _grid(L: float, Npts: int):
    ax = np.linspace(-L, L, Npts)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    return X, Y, Z, h


def _A_fields(X, Y, Z, h, pars, gmax_override=None):
    """The three A components + their grid gmax normalisers.

    Returns (A_x, A_y, A_z, gmaxes). If gmax_override is given (from the
    L=12 grid) it is used instead of this grid's own maxima.
    """
    comps, gmaxes = [], []
    for i, ax_name in enumerate(("x", "y", "z")):
        V_Ai = pars[f"V_A{ax_name}"]
        if V_Ai == 0.0:
            comps.append(np.zeros_like(X))
            gmaxes.append(0.0)
            continue
        phi_hat = phi_FH_smooth(
            X, Y, Z, Pi=pars[f"Pi_A{ax_name}"], r=pars[f"r_A{ax_name}"],
            V=1.0, sigma=pars["sigma_A"], m0=pars["m0"], a=pars["a"],
            ell=pars["ell"],
        )
        if gmax_override is not None:
            gmax = gmax_override[i]
        else:
            g = [fd_grad4(phi_hat, h, axis=axn) for axn in range(3)]
            gmax = float(np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2).max())
        comps.append((V_Ai / (gmax + 1e-30)) * phi_hat)
        gmaxes.append(gmax)
    return comps[0], comps[1], comps[2], gmaxes


def _N_total(X, Y, Z, h, pars, gmax_override=None):
    """Total shift N = grad phi(Pi) + curl A(Pi_A*) and the gmax list."""
    phi = phi_FH_smooth(
        X, Y, Z, Pi=pars["Pi"], r=pars["r"], V=pars["V"],
        sigma=pars["sigma"], m0=pars["m0"], a=pars["a"], ell=pars["ell"],
    )
    N = [fd_grad4(phi, h, axis=axn) for axn in range(3)]
    A_x, A_y, A_z, gmaxes = _A_fields(X, Y, Z, h, pars, gmax_override)
    if any(g > 0 for g in gmaxes) or gmax_override is not None:
        dAz_dy = fd_grad4(A_z, h, axis=1)
        dAy_dz = fd_grad4(A_y, h, axis=2)
        dAx_dz = fd_grad4(A_x, h, axis=2)
        dAz_dx = fd_grad4(A_z, h, axis=0)
        dAy_dx = fd_grad4(A_y, h, axis=0)
        dAx_dy = fd_grad4(A_x, h, axis=1)
        N[0] = N[0] + (dAz_dy - dAy_dz)
        N[1] = N[1] + (dAx_dz - dAz_dx)
        N[2] = N[2] + (dAy_dx - dAx_dy)
    return N, gmaxes


def _slacks(N, h):
    """WEC/DEC slack fields + rho from the shared ADM pipeline.

    Interior crop of 6 cells per side (4th-order FD stencil guard),
    identical to the 2D.11 pipeline so rows are directly comparable.
    """
    rho_full, K, S_full = adm_stress_energy_from_N(N, h)
    interior = (slice(6, -6),) * 3
    rho_arr = rho_full[interior]
    S_arr = S_full.transpose(2, 3, 4, 0, 1)[interior]
    S_flat = S_arr.reshape(-1, 3, 3)
    evals = np.linalg.eigvalsh(S_flat)
    p_min = evals.min(axis=1).reshape(rho_arr.shape)
    p_abs_max = np.abs(evals).max(axis=1).reshape(rho_arr.shape)
    return {
        "rho_E": rho_arr,
        "wec_slack": rho_arr + p_min,
        "dec_slack": rho_arr - p_abs_max,
    }


# --------------------------------------------------------------------------
# Sweep interface (hf_jobs/run_sweep.py)
# --------------------------------------------------------------------------

def build_grid(config: dict) -> list[dict]:
    """Expand ``anchors x Pi x Pi_A-patterns x amplitude-patterns``.

    Config schema::

        {
          "Npts": 65, "L_box": 12.0, "L_far": 45.0,
          "anchors": ["A1", "B1", "S12"],
          "Pi": {"values": [0.125, 0.25, 0.5, 1.0]},
          "Pi_A": {"values": [0.125, 0.25, 0.5, 1.0]},
          "amp_patterns": [[0,0,0], [0.1,0.1,0.1], [0.3,0.3,0.3], [0,0,0.3]],
          "split_exponent_cells": true    # add (Pi_Ax,Pi_Ay,Pi_Az) split spots
        }

    Baselines are the [0,0,0] amplitude patterns (one per anchor x Pi;
    Pi_A canonicalised to 0 there). A-radii are wall-coincident (r_Ai = r)
    plus the interleaved 2/3 radius for the z component in split cells,
    mirroring the S38 design. sigma_A = 5.
    """
    Npts = int(config.get("Npts", 65))
    L_box = float(config.get("L_box", 12.0))
    L_far = float(config.get("L_far", 45.0))
    pis = [float(x) for x in config["Pi"]["values"]]
    pias = [float(x) for x in config["Pi_A"]["values"]]
    amps = [tuple(float(v) for v in p) for p in config["amp_patterns"]]
    grid: list[dict] = []
    seen: set[tuple] = set()

    def add(anchor_name, Pi, amp, pia_triplet, r_triplet):
        pars = dict(ANCHORS[anchor_name])
        zero = amp == (0.0, 0.0, 0.0)
        pia_c = (0.0, 0.0, 0.0) if zero else pia_triplet
        r_c = (0.0, 0.0, 0.0) if zero else r_triplet
        key = (anchor_name, Pi, amp, pia_c, r_c)
        if key in seen:
            return
        seen.add(key)
        grid.append({
            "anchor": anchor_name, **pars, "Pi": Pi,
            "V_Ax": amp[0], "V_Ay": amp[1], "V_Az": amp[2],
            "Pi_Ax": pia_c[0], "Pi_Ay": pia_c[1], "Pi_Az": pia_c[2],
            "r_Ax": r_c[0], "r_Ay": r_c[1], "r_Az": r_c[2],
            "sigma_A": 0.0 if zero else 5.0,
            "Npts": Npts, "L_box": L_box, "L_far": L_far,
        })

    for name in config["anchors"]:
        r = ANCHORS[name]["r"]
        for Pi in pis:
            for amp in amps:
                for pia in pias:
                    add(name, Pi, amp, (pia, pia, pia), (r, r, r))
            if config.get("split_exponent_cells", True):
                # exponent-split spot cells at the strong z-only pattern:
                # the z component carries the asymmetry coupling, so give
                # it extremes while x,y sit at the background value
                for piz in (min(pias), max(pias)):
                    add(name, Pi, (0.1, 0.1, 0.3), (Pi, Pi, piz),
                        (r, r, 2.0 * r / 3.0))
    return grid


def evaluate(point: dict) -> dict:
    """One joint cell -> dual-box record (box ECs + far-field gate)."""
    t0 = time.time()
    record: dict[str, Any] = {**point, "ok": False, "error": ""}
    nan = float("nan")
    record.update({
        "wec_slack_min": nan, "dec_slack_min": nan,
        "wec_pass_fraction": nan, "dec_pass_fraction": nan,
        "rho_E_min": nan, "central_N_max": nan,
        "passenger_zone_volume": nan, "passenger_zone_radius": nan,
        "far_wec_slack_min": nan, "far_dec_slack_min": nan,
        "eval_seconds": nan,
    })
    try:
        Npts = int(point["Npts"])
        # --- box (L=12): ECs + passenger zone; also defines the A normalisers
        X, Y, Z, h = _grid(float(point["L_box"]), Npts)
        N, gmaxes = _N_total(X, Y, Z, h, point)
        out = _slacks(N, h)
        wec = out["wec_slack"]
        dec = out["dec_slack"]
        record.update({
            "wec_slack_min": float(wec.min()),
            "dec_slack_min": float(dec.min()),
            "wec_pass_fraction": float((wec >= 0).mean()),
            "dec_pass_fraction": float((dec >= 0).mean()),
            "rho_E_min": float(out["rho_E"].min()),
        })
        Nmag = np.sqrt(N[0] ** 2 + N[1] ** 2 + N[2] ** 2)
        central = (slice(Npts // 2 - 3, Npts // 2 + 4),) * 3
        record["central_N_max"] = float(Nmag[central].max())
        pz_vol, pz_rad = passenger_zone(Nmag, X, Y, Z, h)
        record["passenger_zone_volume"] = float(pz_vol)
        record["passenger_zone_radius"] = float(pz_rad)

        # --- far-field box (L=45): SAME physical A fields (L=12 gmax)
        Xf, Yf, Zf, hf = _grid(float(point["L_far"]), Npts)
        Nf, _ = _N_total(Xf, Yf, Zf, hf, point, gmax_override=gmaxes)
        outf = _slacks(Nf, hf)
        record["far_wec_slack_min"] = float(outf["wec_slack"].min())
        record["far_dec_slack_min"] = float(outf["dec_slack"].min())

        record["ok"] = True
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    record["eval_seconds"] = time.time() - t0
    return record
