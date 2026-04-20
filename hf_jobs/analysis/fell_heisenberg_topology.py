"""Connectivity / topology analysis for the Fell-Heisenberg WEC+DEC sweep.

Operates on any parquet emitted by ``hf_jobs/sweeps/fell_heisenberg.py``.
The strict WEC+DEC-passing subset is interpreted as a discrete subset of the
sweep's grid lattice, projected to the dimensionless control parameters
(sigma, m0, a, ell, r) -- V is dropped because Session 11 sanity check §2.4
established that strict pass is V-independent (slacks scale as V^2 so the sign
is V-invariant for V > 0).

Outputs (when run via ``main`` as a script):
- ``summary.json``               - aggregate counts and connectivity verdict
- ``component_summary.csv``      - one row per connected component
- ``boundary_cells.csv``         - flat list of boundary points
- ``pairwise_pass_count.png``    - 5x5 grid of 2-D projections (count agg)
- ``pairwise_dec_slack.png``     - 5x5 grid of 2-D projections (max dec_slack agg)
- ``boundary_cells.png``         - 2-D projection showing interior vs boundary
- ``slack_vs_distance.png``      - dec_slack vs Chebyshev distance to boundary
- ``symmetry_probe.json``        - dimensionless ratio invariance scores

Usage::

    python -m hf_jobs.analysis.fell_heisenberg_topology \\
        sweeps_remote/full-20260420T022727/fell_heisenberg_20260420T022809.parquet \\
        fell_heisenberg_topology/

Re-runnable on any combination of parquets (Stage 1 + Stage 2 refinement
data) by passing multiple paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

# Connected-component labelling and basic morphology.
from scipy import ndimage

# Plotting; force a non-interactive backend so the script works in any env.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Standard parameter axes for the FH sweep (excluding V which is amplitude-redundant).
PARAM_AXES: tuple[str, ...] = ("sigma", "m0", "a", "ell", "r")


# ---------------------------------------------------------------------------
# Loading and grid setup
# ---------------------------------------------------------------------------

def load_strict_pass(parquet_paths: Iterable[Path]) -> pd.DataFrame:
    """Load and concatenate parquets, return only strict WEC+DEC-pass rows.

    Strict pass means both ``wec_slack_min > 0`` and ``dec_slack_min > 0``.
    Requires ``ok == True``.
    """
    parts: list[pd.DataFrame] = []
    for p in parquet_paths:
        parts.append(pd.read_parquet(Path(p)))
    df = pd.concat(parts, ignore_index=True)
    ok = df[df["ok"] == True]  # noqa: E712 - parquet bool column
    strict = ok[(ok["wec_slack_min"] > 0) & (ok["dec_slack_min"] > 0)].copy()
    return strict


def grid_axes(df: pd.DataFrame, params: tuple[str, ...] = PARAM_AXES) -> dict[str, np.ndarray]:
    """Return sorted unique values per axis (the grid coordinates)."""
    return {p: np.array(sorted(df[p].unique())) for p in params}


def grid_indices(df: pd.DataFrame, axes: dict[str, np.ndarray]) -> np.ndarray:
    """Boolean N-D mask over the parameter lattice; True where strict-pass."""
    shape = tuple(len(axes[p]) for p in axes)
    mask = np.zeros(shape, dtype=bool)
    coord_to_idx = {p: {v: i for i, v in enumerate(axes[p])} for p in axes}
    for row in df[list(axes)].itertuples(index=False):
        idx = tuple(coord_to_idx[p][getattr(row, p)] for p in axes)
        mask[idx] = True
    return mask


# ---------------------------------------------------------------------------
# Connectivity
# ---------------------------------------------------------------------------

def connected_components(mask: np.ndarray, connectivity: int = 1) -> tuple[np.ndarray, int]:
    """Label connected components in the boolean mask.

    connectivity = 1: 4-connected (only orthogonal neighbours)
    connectivity = mask.ndim: full neighbour connectivity (incl. diagonals)
    """
    structure = ndimage.generate_binary_structure(mask.ndim, connectivity)
    labels, n = ndimage.label(mask, structure=structure)
    return labels, int(n)


def component_summary(
    df: pd.DataFrame,
    labels: np.ndarray,
    axes: dict[str, np.ndarray],
) -> pd.DataFrame:
    """One row per connected component with size and parameter ranges."""
    coord_to_idx = {p: {v: i for i, v in enumerate(axes[p])} for p in axes}
    rows = []
    for comp_id in range(1, labels.max() + 1):
        members = []
        for row in df[list(axes) + ["dec_slack_min", "wec_slack_min", "central_N_max"]].itertuples(index=False):
            idx = tuple(coord_to_idx[p][getattr(row, p)] for p in axes)
            if labels[idx] == comp_id:
                members.append(row)
        if not members:
            continue
        rec: dict = {"component_id": comp_id, "size": len(members)}
        for p in axes:
            vals = [getattr(m, p) for m in members]
            rec[f"{p}_min"] = float(min(vals))
            rec[f"{p}_max"] = float(max(vals))
        slacks = [m.dec_slack_min for m in members]
        rec["dec_slack_min_min"] = float(min(slacks))
        rec["dec_slack_min_max"] = float(max(slacks))
        Ns = [m.central_N_max for m in members]
        rec["central_N_max_min"] = float(min(Ns))
        rec["central_N_max_max"] = float(max(Ns))
        rows.append(rec)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Boundary extraction
# ---------------------------------------------------------------------------

def boundary_cells(mask: np.ndarray, connectivity: int = 1) -> np.ndarray:
    """Boolean mask of cells inside the region adjacent to outside.

    A cell is a boundary cell if it is True (in the region) AND has at least
    one (orthogonal) neighbour that is False or off-grid.
    """
    structure = ndimage.generate_binary_structure(mask.ndim, connectivity)
    # Erode the mask: surviving cells have all neighbours True (i.e. interior).
    interior = ndimage.binary_erosion(mask, structure=structure, border_value=0)
    return mask & ~interior


def chebyshev_distance_to_boundary(mask: np.ndarray) -> np.ndarray:
    """For each True cell, the minimum lattice (Chebyshev) distance to a False cell.

    Boundary cells have distance 1; deep-interior cells have larger distance.
    Returns 0 for non-region cells.
    """
    inverted = ~mask
    dt = ndimage.distance_transform_cdt(~inverted, metric="chessboard")
    return dt


# ---------------------------------------------------------------------------
# 2-D projections + plots
# ---------------------------------------------------------------------------

def project_2d(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    value: str = "dec_slack_min",
    agg: str = "max",
    fill_value: float = np.nan,
) -> pd.DataFrame:
    """Pivot table: rows = y-axis values, cols = x-axis values, cell = agg(value)."""
    return df.pivot_table(
        index=y_axis,
        columns=x_axis,
        values=value,
        aggfunc=agg,
        fill_value=fill_value,
    )


def _imshow_table(ax, table: pd.DataFrame, title: str, cmap: str, vmin=None, vmax=None) -> None:
    """Imshow a pivot table with axis labels."""
    arr = table.values
    im = ax.imshow(
        arr,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        interpolation="nearest",
        vmin=vmin,
        vmax=vmax,
    )
    ax.set_xticks(range(len(table.columns)))
    ax.set_xticklabels([f"{v:g}" for v in table.columns], rotation=45, fontsize=7)
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels([f"{v:g}" for v in table.index], fontsize=7)
    ax.set_xlabel(table.columns.name, fontsize=8)
    ax.set_ylabel(table.index.name, fontsize=8)
    ax.set_title(title, fontsize=8)
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)


def plot_pairwise(
    df: pd.DataFrame,
    params: tuple[str, ...],
    out_path: Path,
    value: str = "dec_slack_min",
    agg: str = "max",
    title_suffix: str = "",
) -> None:
    """Save an N×N grid of pairwise 2-D projections.

    Diagonal cells: 1-D histograms of strict-pass count vs that axis.
    Off-diagonal: 2-D projection (agg(value) over the marginalised axes).
    """
    n = len(params)
    fig, axes = plt.subplots(n, n, figsize=(2.4 * n, 2.4 * n))
    if value == "_count":
        # Special: count strict-pass points, not aggregate of a value column.
        for i, py in enumerate(params):
            for j, px in enumerate(params):
                ax = axes[i, j]
                if i == j:
                    counts = df[py].value_counts().sort_index()
                    ax.bar(range(len(counts)), counts.values)
                    ax.set_xticks(range(len(counts)))
                    ax.set_xticklabels([f"{v:g}" for v in counts.index], rotation=45, fontsize=7)
                    ax.set_title(f"{py} count", fontsize=8)
                else:
                    table = df.pivot_table(
                        index=py, columns=px, values="dec_slack_min", aggfunc="count", fill_value=0
                    )
                    _imshow_table(ax, table, f"{py} vs {px}{title_suffix}", "viridis")
    else:
        # Find global vmin/vmax for consistent colourbar scaling.
        all_tables = []
        for py in params:
            for px in params:
                if py == px:
                    continue
                all_tables.append(project_2d(df, px, py, value=value, agg=agg))
        flat = np.concatenate([t.values.ravel() for t in all_tables])
        flat = flat[np.isfinite(flat)]
        vmin = float(np.nanmin(flat)) if len(flat) else None
        vmax = float(np.nanmax(flat)) if len(flat) else None

        for i, py in enumerate(params):
            for j, px in enumerate(params):
                ax = axes[i, j]
                if i == j:
                    counts = df[py].value_counts().sort_index()
                    ax.bar(range(len(counts)), counts.values)
                    ax.set_xticks(range(len(counts)))
                    ax.set_xticklabels([f"{v:g}" for v in counts.index], rotation=45, fontsize=7)
                    ax.set_title(f"{py} hist", fontsize=8)
                else:
                    table = project_2d(df, px, py, value=value, agg=agg)
                    _imshow_table(ax, table, f"{py} vs {px}", "RdYlGn", vmin=vmin, vmax=vmax)

    fig.suptitle(f"Pairwise projection: {agg}({value}){title_suffix}", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def plot_boundary_2d(
    df_strict: pd.DataFrame,
    mask: np.ndarray,
    bdry_mask: np.ndarray,
    axes: dict[str, np.ndarray],
    out_path: Path,
) -> None:
    """Show interior vs boundary cells in 2-D pair projections.

    For each pair (px, py), aggregates the higher-dim mask by max-presence and
    overlays interior (filled) and boundary (hatched) cells.
    """
    params = list(axes)
    n = len(params)
    interior_mask = mask & ~bdry_mask
    fig, ax_grid = plt.subplots(n, n, figsize=(2.4 * n, 2.4 * n))

    for i, py in enumerate(params):
        for j, px in enumerate(params):
            ax = ax_grid[i, j]
            if i == j:
                counts_int = df_strict[py].value_counts().sort_index()
                ax.bar(range(len(counts_int)), counts_int.values)
                ax.set_xticks(range(len(counts_int)))
                ax.set_xticklabels([f"{v:g}" for v in counts_int.index], rotation=45, fontsize=7)
                ax.set_title(f"{py}", fontsize=8)
                continue
            # Reduce the N-D mask to the (py, px) plane by max over other axes.
            other_axes = tuple(k for k, p in enumerate(params) if p != px and p != py)
            interior_2d = interior_mask.any(axis=other_axes)
            bdry_2d = bdry_mask.any(axis=other_axes)
            # Make sure (py, px) ordering matches the imshow rows/cols.
            iy = params.index(py)
            ix = params.index(px)
            if iy < ix:
                interior_2d = interior_2d.T
                bdry_2d = bdry_2d.T
            # Each 2-D projected cell can be:
            #   0 = empty (no strict-pass point in this (px, py) slab)
            #   1 = interior-only (some interior cell projects here, no boundary)
            #   2 = boundary-only (only boundary cells project here)
            #   3 = mixed (both interior and boundary cells project here)
            display = np.zeros_like(interior_2d, dtype=int)
            int_only = interior_2d & ~bdry_2d
            bdry_only = bdry_2d & ~interior_2d
            mixed = interior_2d & bdry_2d
            display[int_only] = 1
            display[bdry_only] = 2
            display[mixed] = 3
            cmap = matplotlib.colors.ListedColormap(["#ffffff", "#1f77b4", "#d62728", "#9467bd"])
            ax.imshow(display, origin="lower", aspect="auto", cmap=cmap, vmin=0, vmax=3, interpolation="nearest")
            ax.set_xticks(range(len(axes[px])))
            ax.set_xticklabels([f"{v:g}" for v in axes[px]], rotation=45, fontsize=7)
            ax.set_yticks(range(len(axes[py])))
            ax.set_yticklabels([f"{v:g}" for v in axes[py]], fontsize=7)
            ax.set_xlabel(px, fontsize=8)
            ax.set_ylabel(py, fontsize=8)
            ax.set_title(f"{py} vs {px}", fontsize=8)

    fig.suptitle(
        "Strict WEC+DEC pass region in 2-D projection.\n"
        "White = empty,  blue = interior-only,  red = boundary-only,  purple = mixed.",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def plot_slack_vs_distance(
    df_strict: pd.DataFrame,
    mask: np.ndarray,
    axes: dict[str, np.ndarray],
    out_path: Path,
) -> None:
    """Scatter dec_slack_min vs Chebyshev lattice distance to boundary."""
    dt = chebyshev_distance_to_boundary(mask)
    coord_to_idx = {p: {v: i for i, v in enumerate(axes[p])} for p in axes}

    distances = []
    slacks = []
    wecs = []
    for row in df_strict[list(axes) + ["dec_slack_min", "wec_slack_min"]].itertuples(index=False):
        idx = tuple(coord_to_idx[p][getattr(row, p)] for p in axes)
        d = int(dt[idx])
        if d == 0:
            continue  # not in mask -- shouldn't happen for strict-pass rows
        distances.append(d)
        slacks.append(row.dec_slack_min)
        wecs.append(row.wec_slack_min)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    distances = np.array(distances)
    slacks = np.array(slacks)
    wecs = np.array(wecs)

    # Box plot of dec_slack vs distance (the "smoothness" check).
    unique_d = sorted(set(distances))
    data_by_d = [slacks[distances == d] for d in unique_d]
    ax1.boxplot(data_by_d, positions=unique_d, widths=0.6, showfliers=True)
    ax1.set_xlabel("Lattice distance to boundary")
    ax1.set_ylabel("dec_slack_min")
    ax1.set_title("DEC slack vs distance (does slack vanish smoothly?)")
    ax1.axhline(0, color="red", linewidth=0.5, linestyle="--")
    ax1.grid(True, alpha=0.3)

    data_by_d_w = [wecs[distances == d] for d in unique_d]
    ax2.boxplot(data_by_d_w, positions=unique_d, widths=0.6, showfliers=True)
    ax2.set_xlabel("Lattice distance to boundary")
    ax2.set_ylabel("wec_slack_min")
    ax2.set_title("WEC slack vs distance")
    ax2.axhline(0, color="red", linewidth=0.5, linestyle="--")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Symmetry / dimensionless invariant probes
# ---------------------------------------------------------------------------

def symmetry_probe(df: pd.DataFrame) -> dict:
    """Test for clean dimensionless invariants.

    Strategy: for each candidate ratio R = f(params), compute the strict-pass
    set's spread of R; if much narrower than non-pass set's R, the ratio is
    a "control parameter" of the passing region.

    Returns a dict with one entry per candidate ratio:
        {ratio_name: {"pass_mean": ..., "pass_std": ..., "compare_std": ...,
                      "spread_ratio": pass_std / compare_std}}
    spread_ratio < 0.5 is suggestive; < 0.2 is strong evidence of an invariant.
    """
    candidates = {
        "r_over_m0":     ("r", "m0", lambda d: d["r"] / d["m0"]),
        "r_over_sigma":  ("r", "sigma", lambda d: d["r"] / d["sigma"]),
        "r_over_sqrt_sigma": ("r", "sigma", lambda d: d["r"] / np.sqrt(d["sigma"])),
        "a_over_m0":     ("a", "m0", lambda d: d["a"] / d["m0"]),
        "ell_over_r":    ("ell", "r", lambda d: d["ell"] / d["r"]),
        "sigma_over_r2": ("sigma", "r", lambda d: d["sigma"] / (d["r"] ** 2)),
        "m0_minus_a":    ("m0", "a", lambda d: d["m0"] - d["a"]),
        "m0_plus_a":     ("m0", "a", lambda d: d["m0"] + d["a"]),
    }
    results: dict[str, dict] = {}
    for name, (_p1, _p2, fn) in candidates.items():
        try:
            vals = fn(df)
            valid = vals[np.isfinite(vals)]
            if len(valid) < 2:
                continue
            mean = float(valid.mean())
            std = float(valid.std())
            range_v = float(valid.max() - valid.min())
            results[name] = {
                "pass_mean": mean,
                "pass_std": std,
                "pass_range": range_v,
                "pass_min": float(valid.min()),
                "pass_max": float(valid.max()),
                "n_unique": int(len(set(np.round(valid, 6)))),
                "spread_normalized": std / abs(mean) if mean != 0 else float("nan"),
            }
        except Exception as exc:  # pragma: no cover - defensive
            results[name] = {"error": str(exc)}
    return results


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main(parquet_paths: list[Path], out_dir: Path) -> dict:
    """Full pipeline: load, analyse, plot, return summary dict."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ----- Load data -----
    strict = load_strict_pass(parquet_paths)
    n_strict = len(strict)

    # Identify which axes have variation (>= 2 unique values).
    full_axes = {p: np.array(sorted(strict[p].unique())) for p in PARAM_AXES}
    active_params = tuple(p for p in PARAM_AXES if len(full_axes[p]) >= 2)
    if len(active_params) < 2:
        raise SystemExit(
            f"Strict-pass set spans <2 axes ({active_params}); cannot do connectivity."
        )
    axes = {p: full_axes[p] for p in active_params}

    # ----- Build mask -----
    mask = grid_indices(strict, axes)

    # ----- Connectivity -----
    labels_4c, n_4c = connected_components(mask, connectivity=1)
    labels_full, n_full = connected_components(mask, connectivity=mask.ndim)
    csum_4c = component_summary(strict, labels_4c, axes)

    # ----- Boundary -----
    bdry = boundary_cells(mask, connectivity=1)
    n_bdry = int(bdry.sum())
    n_interior = int(mask.sum() - n_bdry)

    # Save the boundary cells as a CSV for inspection.
    bdry_records = []
    coord_idx_to_val = {p: list(axes[p]) for p in axes}
    for idx in zip(*np.where(bdry)):
        rec = {p: float(coord_idx_to_val[p][i]) for p, i in zip(axes, idx)}
        bdry_records.append(rec)
    pd.DataFrame(bdry_records).to_csv(out_dir / "boundary_cells.csv", index=False)
    csum_4c.to_csv(out_dir / "component_summary.csv", index=False)

    # ----- Symmetry probe -----
    sym = symmetry_probe(strict)
    with open(out_dir / "symmetry_probe.json", "w") as fh:
        json.dump(sym, fh, indent=2)

    # ----- Plots -----
    plot_pairwise(
        strict,
        active_params,
        out_dir / "pairwise_pass_count.png",
        value="_count",
        title_suffix=" (strict WEC+DEC pass count)",
    )
    plot_pairwise(
        strict,
        active_params,
        out_dir / "pairwise_dec_slack.png",
        value="dec_slack_min",
        agg="max",
        title_suffix=" (max DEC slack)",
    )
    plot_boundary_2d(strict, mask, bdry, axes, out_dir / "boundary_cells.png")
    plot_slack_vs_distance(strict, mask, axes, out_dir / "slack_vs_distance.png")

    # ----- Summary -----
    summary = {
        "n_strict_pass": n_strict,
        "active_params": list(active_params),
        "axes_extents": {p: [float(axes[p][0]), float(axes[p][-1])] for p in axes},
        "axes_n": {p: int(len(axes[p])) for p in axes},
        "mask_filled_cells": int(mask.sum()),
        "mask_total_cells": int(mask.size),
        "fill_fraction": float(mask.sum() / mask.size),
        "n_components_4connected": n_4c,
        "n_components_fullconnected": n_full,
        "n_boundary_cells": n_bdry,
        "n_interior_cells": n_interior,
        "boundary_fraction": float(n_bdry / mask.sum()) if mask.sum() else 0.0,
        "components": csum_4c.to_dict(orient="records"),
        "symmetry_probe": sym,
    }

    with open(out_dir / "summary.json", "w") as fh:
        json.dump(summary, fh, indent=2)

    return summary


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "parquets",
        nargs="+",
        type=Path,
        help="One or more sweep result parquet files.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Directory to write figures, CSVs, and summary.json.",
    )
    args = parser.parse_args(argv)

    summary = main(args.parquets, args.out_dir)
    print(f"\n=== Summary ===")
    print(f"Strict pass:          {summary['n_strict_pass']}")
    print(f"Active params:        {summary['active_params']}")
    print(f"Mask fill:            {summary['mask_filled_cells']} / {summary['mask_total_cells']} "
          f"({100 * summary['fill_fraction']:.1f}%)")
    print(f"Components (4-conn):  {summary['n_components_4connected']}")
    print(f"Components (full):    {summary['n_components_fullconnected']}")
    print(f"Boundary cells:       {summary['n_boundary_cells']} "
          f"({100 * summary['boundary_fraction']:.1f}% of region)")
    print(f"Interior cells:       {summary['n_interior_cells']}")
    print()
    print(f"Files written to {args.out_dir}/:")
    for f in sorted(args.out_dir.iterdir()):
        print(f"  {f.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
