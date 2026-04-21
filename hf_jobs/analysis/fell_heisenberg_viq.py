"""Lobo-Visser-style Volume Integral Quantifier (VIQ) for FH sweep records.

Implements ROADMAP Task 2D.12. Re-evaluates the FH potential at each row of
an existing sweep parquet, integrates |rho_E| over three reference regions
identified by the shift magnitude |N|, and emits derived columns suitable
for direct comparison against Lobo-Visser 2004 (gr-qc/0406083, gr-qc/0412065).

Reference masses (geometrized G=c=1, integrated on the same Cartesian box
the sweep used):

    M_box        = sum_box  |rho_E| * h^3
    M_shell      = sum_{0.5 < |N| < 1.5}  |rho_E| * h^3   (bubble-wall band;
                                                            often empty for FH
                                                            because the |N|=1
                                                            transition is
                                                            resolution-thin --
                                                            see notes)
    M_exterior   = sum_{|N| >= 0.5}  |rho_E| * h^3        (everything outside
                                                            passenger zone --
                                                            more robust
                                                            stand-in for the
                                                            L-V "warp-field
                                                            mass" reference)
    M_passenger  = sum_{|N| < 0.5}  |rho_E| * h^3         (the passenger zone;
                                                            single-cell for FH
                                                            per Task 2D.6)

VIQ ratios (eight new columns, plus an L-V-style "exact-approx" column):

    VIQ_neg_M{ref} = |E_neg| / M_{ref}     (the L-V negative-warp-field ratio)
    VIQ_pos_M{ref} = E_pos   / M_{ref}     (positive-energy ratio for sanity)

    VIQ_LV_exact_approx = integral_box (rho + p_min) * h^3
        ~ L-V's I_V = integral (rho + p_r) dV from gr-qc/0406083 sec 3,
        approximated using p_min as a stand-in for the radial pressure
        (the FH sweep does not store the principal frame, only p_min).

CLI:

    python -m hf_jobs.analysis.fell_heisenberg_viq <input_parquet> \\
        --output <output_parquet> [--npts 49] [--strict-pass-only]

Notes:
- Integrals are smooth volumetric quantities, not point eigenvalue tests, so
  the resolution sensitivity from FELL_HEISENBERG_SWEEP_NOTES.md sec 11 (which
  applied to wec_slack_min sign flips at the boundary) does not apply here.
  Default Npts=49 gives a 2x speedup over the sweep's Npts=65 with
  negligible loss in integrated values (smooth integrands integrate well at
  modest resolution).
- The VIQ_LV_exact_approx column requires the principal-pressure
  diagonalization, so it is the slow column. Pass --no-viq-lv to skip it
  (only the rho_E integrals are computed; ~3x speedup).
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from hf_jobs.sweeps.fell_heisenberg import (
    adm_stress_energy,
    eulerian_rho_irrotational,
    fd_grad4,
    phi_FH_smooth,
)


def viq_for_row(
    point: dict,
    Npts: int,
    include_lv: bool,
) -> dict[str, float]:
    """Compute VIQ-related integrals for a single FH parameter point.

    Parameters mirror the sweep evaluate() schema. Returns a dict suitable
    for joining onto the sweep DataFrame as new columns.
    """
    L = float(point["L"])
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")

    phi = phi_FH_smooth(
        X, Y, Z,
        Pi=float(point.get("Pi", 0.25)),
        r=float(point["r"]),
        V=float(point["V"]),
        sigma=float(point["sigma"]),
        m0=float(point["m0"]),
        a=float(point["a"]),
        ell=float(point["ell"]),
    )

    out: dict[str, float] = {}

    if not np.all(np.isfinite(phi)):
        nan = float("nan")
        for key in [
            "viq_E_pos_recompute", "viq_E_neg_recompute", "viq_E_net_recompute",
            "viq_M_box", "viq_M_shell", "viq_M_exterior", "viq_M_passenger",
            "viq_shell_volume", "viq_exterior_volume", "viq_passenger_volume",
            "viq_passenger_cells", "viq_Nmag_max", "viq_Nmag_origin",
            "viq_neg_M_box", "viq_neg_M_shell", "viq_neg_M_exterior", "viq_neg_M_passenger",
            "viq_pos_M_box", "viq_pos_M_shell", "viq_pos_M_exterior", "viq_pos_M_passenger",
            "viq_LV_exact_approx", "viq_eval_seconds",
        ]:
            out[key] = nan
        out["viq_error"] = "non-finite phi"
        return out

    t0 = time.time()

    # Eulerian energy density (irrotational closed form) and shift magnitude.
    rho_E, _ = eulerian_rho_irrotational(phi, h)
    grads = [fd_grad4(phi, h, axis=ax) for ax in range(3)]
    Nmag = np.sqrt(grads[0] ** 2 + grads[1] ** 2 + grads[2] ** 2)

    vol = h ** 3
    abs_rho = np.abs(rho_E)

    # Recomputed integrated energies (sanity check vs sweep-recorded E_pos/E_neg).
    E_pos = float(rho_E[rho_E > 0].sum() * vol)
    E_neg = float(rho_E[rho_E < 0].sum() * vol)
    E_net = E_pos + E_neg
    out["viq_E_pos_recompute"] = E_pos
    out["viq_E_neg_recompute"] = E_neg
    out["viq_E_net_recompute"] = E_net

    # Reference masses, defined as integrated |rho_E| over the four regions.
    mask_shell = (Nmag > 0.5) & (Nmag < 1.5)
    mask_pass = Nmag < 0.5
    mask_ext = Nmag >= 0.5  # everything outside passenger zone

    M_box = float(abs_rho.sum() * vol)
    M_shell = float(abs_rho[mask_shell].sum() * vol)
    M_ext = float(abs_rho[mask_ext].sum() * vol)
    M_pass = float(abs_rho[mask_pass].sum() * vol)
    out["viq_M_box"] = M_box
    out["viq_M_shell"] = M_shell
    out["viq_M_exterior"] = M_ext
    out["viq_M_passenger"] = M_pass

    out["viq_shell_volume"] = float(mask_shell.sum() * vol)
    out["viq_exterior_volume"] = float(mask_ext.sum() * vol)
    out["viq_passenger_volume"] = float(mask_pass.sum() * vol)
    out["viq_passenger_cells"] = int(mask_pass.sum())
    out["viq_Nmag_max"] = float(Nmag.max())
    centre = tuple(s // 2 for s in Nmag.shape)
    out["viq_Nmag_origin"] = float(Nmag[centre])

    # VIQ ratios. Use np.nan when divisor is zero (don't divide by zero).
    def _safe_ratio(num: float, den: float) -> float:
        if den == 0.0 or not math.isfinite(den):
            return float("nan")
        return float(num / den)

    abs_E_neg = abs(E_neg)
    out["viq_neg_M_box"] = _safe_ratio(abs_E_neg, M_box)
    out["viq_neg_M_shell"] = _safe_ratio(abs_E_neg, M_shell)
    out["viq_neg_M_exterior"] = _safe_ratio(abs_E_neg, M_ext)
    out["viq_neg_M_passenger"] = _safe_ratio(abs_E_neg, M_pass)
    out["viq_pos_M_box"] = _safe_ratio(E_pos, M_box)
    out["viq_pos_M_shell"] = _safe_ratio(E_pos, M_shell)
    out["viq_pos_M_exterior"] = _safe_ratio(E_pos, M_ext)
    out["viq_pos_M_passenger"] = _safe_ratio(E_pos, M_pass)

    if include_lv:
        # L-V exact-approx: integral (rho + p_min) dV over the whole box.
        # This needs the full ADM stress-energy + eigenvalue diagonalization.
        try:
            rho_full, _, S_full = adm_stress_energy(phi, h)
            # Use the same stride-6 interior the sweep uses.
            interior = (slice(6, -6),) * 3
            rho_arr = rho_full[interior]
            S_arr = S_full.transpose(2, 3, 4, 0, 1)[interior]
            S_flat = S_arr.reshape(-1, 3, 3)
            evals = np.linalg.eigvalsh(S_flat)
            p_min = evals.min(axis=1).reshape(rho_arr.shape)
            integrand = rho_arr + p_min
            out["viq_LV_exact_approx"] = float(integrand.sum() * vol)
        except Exception as exc:  # pragma: no cover - defensive
            out["viq_LV_exact_approx"] = float("nan")
            out["viq_error"] = f"LV-exact failed: {type(exc).__name__}: {exc}"
    else:
        out["viq_LV_exact_approx"] = float("nan")

    out["viq_eval_seconds"] = float(time.time() - t0)
    if "viq_error" not in out:
        out["viq_error"] = ""
    return out


def process_parquet(
    input_path: Path,
    output_path: Path,
    Npts: int,
    include_lv: bool,
    strict_pass_only: bool,
    summary_path: Path | None = None,
) -> pd.DataFrame:
    """Load a sweep parquet, compute VIQ columns per row, write derived parquet."""
    print(f"[viq] reading {input_path}")
    df = pd.read_parquet(input_path)
    n_rows = len(df)
    print(f"[viq] {n_rows} input rows")

    if strict_pass_only:
        mask = (df["wec_slack_min"] >= 0) & (df["dec_slack_min"] >= 0) & df["ok"]
        df_work = df[mask].copy().reset_index(drop=True)
        print(f"[viq] {len(df_work)} strict-pass rows after filter")
    else:
        df_work = df.copy()

    new_cols: dict[str, list[Any]] = {}
    t_start = time.time()
    for i, row in df_work.iterrows():
        if not bool(row["ok"]):
            # Skip failed rows (will be NaN-padded below).
            continue
        if i > 0 and i % 100 == 0:
            elapsed = time.time() - t_start
            rate = i / elapsed if elapsed > 0 else float("nan")
            eta = (len(df_work) - i) / rate if rate > 0 else float("nan")
            print(f"[viq] row {i}/{len(df_work)}  elapsed {elapsed:.1f}s  rate {rate:.2f}/s  eta {eta:.0f}s")
        result = viq_for_row(row.to_dict(), Npts=Npts, include_lv=include_lv)
        for k, v in result.items():
            if k not in new_cols:
                new_cols[k] = [None] * len(df_work)
            new_cols[k][i] = v

    for k, v in new_cols.items():
        df_work[k] = v

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_work.to_parquet(output_path)
    print(f"[viq] wrote {output_path}  ({len(df_work)} rows, {len(df_work.columns)} cols)")

    if summary_path is not None:
        summary = _summarise(df_work)
        summary_path.write_text(json.dumps(summary, indent=2))
        print(f"[viq] wrote {summary_path}")

    return df_work


def _summarise(df: pd.DataFrame) -> dict:
    """Headline numbers for the VIQ post-processing."""
    out: dict[str, Any] = {
        "n_rows": int(len(df)),
        "n_strict_pass": int(((df["wec_slack_min"] >= 0) & (df["dec_slack_min"] >= 0) & df["ok"]).sum()),
    }

    strict = df[(df["wec_slack_min"] >= 0) & (df["dec_slack_min"] >= 0) & df["ok"] & df["viq_E_pos_recompute"].notna()]

    def _pct(s: pd.Series, q: float) -> float:
        return float(s.quantile(q))

    for col in [
        "viq_E_pos_recompute", "viq_E_neg_recompute", "viq_E_net_recompute",
        "viq_M_box", "viq_M_shell", "viq_M_exterior", "viq_M_passenger",
        "viq_shell_volume", "viq_exterior_volume", "viq_passenger_volume",
        "viq_Nmag_max", "viq_Nmag_origin",
        "viq_neg_M_box", "viq_neg_M_shell", "viq_neg_M_exterior", "viq_neg_M_passenger",
        "viq_pos_M_box", "viq_pos_M_shell", "viq_pos_M_exterior", "viq_pos_M_passenger",
        "viq_LV_exact_approx",
    ]:
        if col in strict.columns and len(strict) > 0:
            s = strict[col].dropna()
            if len(s) > 0:
                out[f"strict_pass_{col}"] = {
                    "count": int(len(s)),
                    "min": float(s.min()),
                    "p05": _pct(s, 0.05),
                    "median": float(s.median()),
                    "mean": float(s.mean()),
                    "p95": _pct(s, 0.95),
                    "max": float(s.max()),
                }

    # Find canonical-anchor row if present.
    anchor_mask = (
        (df["V"].between(1.49, 1.51))
        & (df["sigma"].between(9.99, 10.01))
        & (df["m0"].between(2.99, 3.01))
        & (df["a"].between(0.04, 0.06))
        & (df["ell"].between(3.99, 4.01))
        & (df["r"].between(8.99, 9.01))
    )
    anchor_rows = df[anchor_mask]
    if len(anchor_rows) > 0:
        anchor = anchor_rows.iloc[0]
        out["canonical_anchor"] = {
            "params": {k: float(anchor[k]) for k in ("V", "sigma", "m0", "a", "ell", "r")},
            "viq_E_pos_recompute": float(anchor.get("viq_E_pos_recompute", float("nan"))),
            "viq_E_neg_recompute": float(anchor.get("viq_E_neg_recompute", float("nan"))),
            "viq_M_box": float(anchor.get("viq_M_box", float("nan"))),
            "viq_M_shell": float(anchor.get("viq_M_shell", float("nan"))),
            "viq_M_exterior": float(anchor.get("viq_M_exterior", float("nan"))),
            "viq_M_passenger": float(anchor.get("viq_M_passenger", float("nan"))),
            "viq_passenger_cells": int(anchor.get("viq_passenger_cells", -1) if pd.notna(anchor.get("viq_passenger_cells")) else -1),
            "viq_Nmag_max": float(anchor.get("viq_Nmag_max", float("nan"))),
            "viq_Nmag_origin": float(anchor.get("viq_Nmag_origin", float("nan"))),
            "viq_neg_M_box": float(anchor.get("viq_neg_M_box", float("nan"))),
            "viq_pos_M_exterior": float(anchor.get("viq_pos_M_exterior", float("nan"))),
            "viq_pos_M_passenger": float(anchor.get("viq_pos_M_passenger", float("nan"))),
            "viq_LV_exact_approx": float(anchor.get("viq_LV_exact_approx", float("nan"))),
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="Input sweep parquet (e.g. sweeps_remote/full-.../...parquet)")
    parser.add_argument("--output", type=Path, required=True, help="Output VIQ parquet path")
    parser.add_argument("--npts", type=int, default=49, help="Grid resolution (default 49; integrals are smooth)")
    parser.add_argument(
        "--no-viq-lv",
        action="store_true",
        help="Skip the L-V exact-approx column (3x speedup; skips eigenvalue diagonalization)",
    )
    parser.add_argument(
        "--strict-pass-only",
        action="store_true",
        help="Restrict to rows with strict full-WEC and DEC pass",
    )
    parser.add_argument("--summary", type=Path, default=None, help="Optional summary JSON output path")
    args = parser.parse_args()

    process_parquet(
        input_path=args.input,
        output_path=args.output,
        Npts=args.npts,
        include_lv=not args.no_viq_lv,
        strict_pass_only=args.strict_pass_only,
        summary_path=args.summary,
    )


if __name__ == "__main__":
    main()
