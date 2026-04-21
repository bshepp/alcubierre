"""Source-matter classification of FH stress-energy per Bobrick-Martire 2021.

Implements ROADMAP Task 2D.9. Re-evaluates the FH spatial stress tensor S_ij
at a small set of representative strict-pass points, computes:

  - the full principal-pressure triple (p1, p2, p3) per cell (eigvalsh of S_ij)
  - the static Killing vector norm g_tt = -alpha^2 + |N|^2 = -1 + |N|^2
  - the Bobrick-Martire 2021 four-class assignment per cell, based on whether
    xi = d/dt is timelike (g_tt < 0) or spacelike (g_tt > 0)
  - the isotropy diagnostics: anisotropy ratio (p_max - p_min) / |p_mean|,
    p_min sign, and a Hawking-Ellis Type assignment per cell (Type I if
    rho is a non-degenerate timelike eigenvalue, etc. -- approximated here
    via the spatial eigenvalues only since the FH alpha=1 keeps T^0_0 in
    a simple closed form).

For the FH ansatz at strict pass:
  - alpha = 1 (unit lapse), |N|^2 ranges from ~0 at the passenger zone to
    ~225 at the wall, so g_tt = -1 + |N|^2 ranges from -1 to +224.
  - The static Killing vector xi = d/dt is timelike ONLY in the single
    passenger cell. Everywhere else it is spacelike. This places FH in a
    region not covered by any of B-M's four classes (see notes).

CLI:

    python -m hf_jobs.analysis.fell_heisenberg_matter \\
        --output fell_heisenberg_matter \\
        [--npts 65] [--n-points 8]

Outputs:
    fell_heisenberg_matter/<point_id>/eigenvalues.npz   (p1,p2,p3, gtt, Nmag)
    fell_heisenberg_matter/<point_id>/slice_plots.png   (z=0 slices)
    fell_heisenberg_matter/summary.json                  (per-point + global)
    fell_heisenberg_matter/leaderboard.csv               (one row per point)
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hf_jobs.sweeps.fell_heisenberg import (
    adm_stress_energy,
    fd_grad4,
    phi_FH_smooth,
)


# Canonical winner from FELL_HEISENBERG_SWEEP_NOTES.md section 1.1.
CANONICAL_ANCHOR = dict(V=1.5, sigma=10.0, m0=3.0, a=0.05, ell=4.0, r=9.0, Pi=0.25, L=12.0)


def _select_representative_points(
    parquet_path: Path, n_points: int = 8
) -> list[dict]:
    """Pick a small representative set of strict-pass points from the parquet.

    Strategy: include the canonical anchor (if present) plus n_points-1
    spread across (V, r) ranges to capture geometric diversity.
    """
    df = pd.read_parquet(parquet_path)
    strict = df[(df.wec_slack_min >= 0) & (df.dec_slack_min >= 0) & df.ok].copy()

    selected: list[dict] = []

    # Canonical anchor.
    anch = strict[
        (strict.V.between(1.4, 1.6))
        & (strict.sigma.between(9.99, 10.01))
        & (strict.m0.between(2.99, 3.01))
        & (strict.a.between(0.04, 0.06))
        & (strict.ell.between(3.99, 4.01))
        & (strict.r.between(8.99, 9.01))
    ]
    if len(anch) > 0:
        d = anch.iloc[0].to_dict()
        d["_label"] = "canonical_anchor"
        selected.append(d)

    # Stratified sample: bin by V and r.
    remaining = n_points - len(selected)
    if remaining > 0:
        bins = strict.assign(
            V_bin=pd.cut(strict.V, bins=4),
            r_bin=pd.cut(strict.r, bins=4),
        )
        groups = list(bins.groupby(["V_bin", "r_bin"], observed=True))
        groups_sorted = sorted(groups, key=lambda gv: -len(gv[1]))
        i = 0
        while len(selected) < n_points and i < len(groups_sorted):
            (vb, rb), grp = groups_sorted[i]
            row = grp.iloc[len(grp) // 2].to_dict()
            label = f"V{row['V']:.2f}_r{row['r']:.2f}"
            already = any(s["_label"] == label for s in selected)
            if not already:
                row["_label"] = label
                selected.append(row)
            i += 1

    # Strip _bin columns + restrict to the keys evaluate() needs.
    keys = ["V", "sigma", "m0", "a", "ell", "r", "Pi", "L", "_label"]
    return [{k: pt[k] for k in keys if k in pt} for pt in selected]


@dataclass
class MatterDiagnostics:
    """Per-point classification summary."""
    label: str
    V: float
    sigma: float
    m0: float
    a: float
    ell: float
    r: float
    Pi: float
    L: float
    Npts: int
    # Stress-energy diagnostics (interior cells only; stride-6 from each face).
    rho_min: float
    rho_max: float
    rho_pos_fraction: float
    p1_min: float; p1_max: float
    p2_min: float; p2_max: float
    p3_min: float; p3_max: float
    # Anisotropy diagnostics
    anisotropy_max: float          # max over cells of (p3-p1)/|rho|
    anisotropy_median: float       # median of same
    isotropic_fraction: float      # fraction of cells where (p3-p1)/|rho| < 0.05
    # Bobrick-Martire static-Killing norm classification
    gtt_min: float                 # min of g_tt = -1 + |N|^2
    gtt_max: float
    BM_timelike_fraction: float    # fraction of box where xi is timelike (g_tt<0)
    BM_spacelike_fraction: float   # fraction where xi is spacelike (g_tt>0)
    BM_class_assignment: str       # see _classify_BM
    # Hawking-Ellis approximation: tally of cells where p_min has each sign
    HE_TypeI_like_fraction: float  # cells where rho > 0 and p_max - p_min < |rho|
                                    # (a Type-I-friendly indicator, not a rigorous
                                    # eigenvector-decomposition classification)


def _classify_BM(g_tt_inside: np.ndarray, g_tt_outside: np.ndarray) -> str:
    """Heuristic B-M four-class assignment based on g_tt sign in inner vs outer.

    Inner = central single passenger cell (per Task 2D.6).
    Outer = box-edge cells (proxy for asymptotic infinity).

    Returns one of: 'I', 'II', 'III', 'IV', or 'OUTSIDE_BM_TAXONOMY' if none fits.
    """
    in_TL = bool(np.all(g_tt_inside < 0))
    in_SL = bool(np.all(g_tt_inside > 0))
    out_TL = bool(np.all(g_tt_outside < 0))
    out_SL = bool(np.all(g_tt_outside >= 0))

    if in_TL and out_TL:
        return "I (mild subluminal)"
    if in_SL and out_SL:
        return "II (mild superluminal)"
    if in_TL and out_SL:
        return "III (extreme superluminal)"
    if in_SL and out_TL:
        return "IV (extreme subluminal)"
    return "OUTSIDE_BM_TAXONOMY (mixed g_tt sign at inner or outer)"


def evaluate_point(point: dict, Npts: int) -> tuple[MatterDiagnostics, dict]:
    """Compute the full eigenvalue + classification diagnostics for one point.

    Returns (diagnostics, raw_arrays) where raw_arrays has ``p1, p2, p3,
    rho_full, gtt, Nmag, xs`` for slicing/plotting.
    """
    L = float(point["L"])
    Pi = float(point.get("Pi", 0.25))
    xs = np.linspace(-L, L, Npts)
    h = float(xs[1] - xs[0])
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")

    phi = phi_FH_smooth(
        X, Y, Z,
        Pi=Pi, r=float(point["r"]), V=float(point["V"]),
        sigma=float(point["sigma"]), m0=float(point["m0"]),
        a=float(point["a"]), ell=float(point["ell"]),
    )
    rho_full, _, S_full = adm_stress_energy(phi, h)

    # Shift magnitude and static-Killing g_tt = -alpha^2 + |N|^2 = -1 + |N|^2.
    grads = [fd_grad4(phi, h, axis=ax) for ax in range(3)]
    Nmag2 = grads[0] ** 2 + grads[1] ** 2 + grads[2] ** 2
    Nmag = np.sqrt(Nmag2)
    gtt = -1.0 + Nmag2

    # Stride-6 interior to match the sweep's interior masking.
    interior = (slice(6, -6),) * 3
    rho_int = rho_full[interior]
    S_int = S_full.transpose(2, 3, 4, 0, 1)[interior]
    S_flat = S_int.reshape(-1, 3, 3)
    evals = np.linalg.eigvalsh(S_flat)  # sorted ascending: (p1, p2, p3)
    p1 = evals[:, 0].reshape(rho_int.shape)
    p2 = evals[:, 1].reshape(rho_int.shape)
    p3 = evals[:, 2].reshape(rho_int.shape)

    # Anisotropy.
    rho_safe = np.where(np.abs(rho_int) > 1e-12, np.abs(rho_int), np.nan)
    aniso = (p3 - p1) / rho_safe
    aniso_finite = aniso[np.isfinite(aniso)]
    anis_max = float(np.nanmax(aniso)) if aniso_finite.size > 0 else float("nan")
    anis_med = float(np.nanmedian(aniso)) if aniso_finite.size > 0 else float("nan")
    iso_frac = float(np.mean(aniso_finite < 0.05)) if aniso_finite.size > 0 else float("nan")

    # B-M classification.
    centre = tuple(s // 2 for s in gtt.shape)
    g_in = gtt[centre]
    g_out_edges = np.concatenate([
        gtt[0, :, :].ravel(),
        gtt[-1, :, :].ravel(),
        gtt[:, 0, :].ravel(),
        gtt[:, -1, :].ravel(),
        gtt[:, :, 0].ravel(),
        gtt[:, :, -1].ravel(),
    ])
    bm_class = _classify_BM(np.array([g_in]), g_out_edges)

    # Hawking-Ellis Type-I-like indicator (approximation; see docstring).
    HE_typeI_like = (rho_int > 0) & ((p3 - p1) < np.abs(rho_int))

    diag = MatterDiagnostics(
        label=str(point.get("_label", "unknown")),
        V=float(point["V"]), sigma=float(point["sigma"]), m0=float(point["m0"]),
        a=float(point["a"]), ell=float(point["ell"]), r=float(point["r"]),
        Pi=Pi, L=L, Npts=Npts,
        rho_min=float(rho_int.min()), rho_max=float(rho_int.max()),
        rho_pos_fraction=float(np.mean(rho_int > 0)),
        p1_min=float(p1.min()), p1_max=float(p1.max()),
        p2_min=float(p2.min()), p2_max=float(p2.max()),
        p3_min=float(p3.min()), p3_max=float(p3.max()),
        anisotropy_max=anis_max,
        anisotropy_median=anis_med,
        isotropic_fraction=iso_frac,
        gtt_min=float(gtt.min()), gtt_max=float(gtt.max()),
        BM_timelike_fraction=float(np.mean(gtt < 0)),
        BM_spacelike_fraction=float(np.mean(gtt > 0)),
        BM_class_assignment=bm_class,
        HE_TypeI_like_fraction=float(np.mean(HE_typeI_like)),
    )
    raw = dict(p1=p1, p2=p2, p3=p3, rho=rho_int, gtt=gtt, Nmag=Nmag, xs=xs, h=h)
    return diag, raw


def plot_slices(diag: MatterDiagnostics, raw: dict, out_path: Path) -> None:
    """Save 2x3 z=0 slice plots: rho, p1, p3, anisotropy, |N|, g_tt."""
    p1, p3, rho = raw["p1"], raw["p3"], raw["rho"]
    Nmag, gtt = raw["Nmag"], raw["gtt"]
    # Interior z=0 slice (stride-6 inset already applied to p1/p3/rho)
    nz = p1.shape[2]
    sl = nz // 2
    rho_s = rho[:, :, sl]
    p1_s = p1[:, :, sl]
    p3_s = p3[:, :, sl]
    aniso_s = (p3_s - p1_s) / np.where(np.abs(rho_s) > 1e-12, np.abs(rho_s), np.nan)
    # gtt + Nmag are defined on the full grid (Npts), not stride-6
    nz_full = gtt.shape[2]
    sl_full = nz_full // 2
    Nmag_s = Nmag[:, :, sl_full]
    gtt_s = gtt[:, :, sl_full]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for ax, data, title in zip(
        axes.ravel(),
        [rho_s, p1_s, p3_s, aniso_s, Nmag_s, gtt_s],
        [r"$\rho_E$", r"$p_1=p_{\min}$", r"$p_3=p_{\max}$",
         r"$(p_3-p_1)/|\rho|$", r"$|\vec N|$", r"$g_{tt}=-1+|\vec N|^2$"],
    ):
        im = ax.imshow(data.T, origin="lower", cmap="RdBu_r")
        ax.set_title(title)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle(
        f"FH matter diagnostics @ {diag.label}: "
        f"V={diag.V}, sigma={diag.sigma}, m0={diag.m0}, "
        f"a={diag.a}, ell={diag.ell}, r={diag.r}\n"
        f"BM class: {diag.BM_class_assignment}",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=110)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--parquet", type=Path,
                        default=Path("sweeps_remote/full-20260420T022727/fell_heisenberg_20260420T022809.parquet"),
                        help="Strict-pass parquet to draw representative points from")
    parser.add_argument("--output", type=Path, default=Path("fell_heisenberg_matter"),
                        help="Output directory (default fell_heisenberg_matter/)")
    parser.add_argument("--npts", type=int, default=65,
                        help="Grid resolution (default 65, matching the sweep)")
    parser.add_argument("--n-points", type=int, default=8,
                        help="Number of representative points to evaluate")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    points = _select_representative_points(args.parquet, n_points=args.n_points)
    print(f"[matter] selected {len(points)} representative points")

    diagnostics: list[MatterDiagnostics] = []
    for pt in points:
        label = pt["_label"]
        print(f"[matter] evaluating {label}: V={pt['V']:.2f}, r={pt['r']:.2f}, "
              f"sigma={pt['sigma']:.2f}, m0={pt['m0']:.2f}, a={pt['a']:.3f}, ell={pt['ell']:.2f}")
        diag, raw = evaluate_point(pt, Npts=args.npts)
        diagnostics.append(diag)
        sub_dir = args.output / label.replace("/", "_")
        sub_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(sub_dir / "eigenvalues.npz",
                            p1=raw["p1"], p2=raw["p2"], p3=raw["p3"],
                            rho=raw["rho"], gtt=raw["gtt"], Nmag=raw["Nmag"],
                            xs=raw["xs"])
        plot_slices(diag, raw, sub_dir / "slice_plots.png")
        print(f"  -> rho range [{diag.rho_min:.3g}, {diag.rho_max:.3g}], "
              f"BM class: {diag.BM_class_assignment}, "
              f"timelike fraction: {diag.BM_timelike_fraction:.4f}")

    leaderboard = pd.DataFrame([asdict(d) for d in diagnostics])
    leaderboard.to_csv(args.output / "leaderboard.csv", index=False)
    summary = {
        "n_points": len(diagnostics),
        "Npts": args.npts,
        "BM_classes_seen": sorted({d.BM_class_assignment for d in diagnostics}),
        "all_outside_BM_taxonomy": all(
            "OUTSIDE_BM_TAXONOMY" in d.BM_class_assignment for d in diagnostics
        ),
        "any_isotropic": any(d.isotropic_fraction > 0.5 for d in diagnostics),
        "global_BM_timelike_fraction": {
            "min": min(d.BM_timelike_fraction for d in diagnostics),
            "median": float(np.median([d.BM_timelike_fraction for d in diagnostics])),
            "max": max(d.BM_timelike_fraction for d in diagnostics),
        },
        "points": [asdict(d) for d in diagnostics],
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2))
    print(f"[matter] wrote {args.output / 'leaderboard.csv'}")
    print(f"[matter] wrote {args.output / 'summary.json'}")
    print(f"[matter] BM classes seen: {summary['BM_classes_seen']}")


if __name__ == "__main__":
    main()
